
import flask, json, random
from py3dbp import Packer, Bin, Item
from flask_cors import cross_origin

# init flask
app = flask.Flask(__name__)

# load data
with open('widadvance.json',encoding='utf-8') as f:
    alldata = json.load(f)

# a simple page that says hello
@app.route('/')
@cross_origin()
def hello():

    hello_world = '''
    welcome to 3D packing prob API_1.1 <br>
    <br>
    <br>
    update 1.1  : <br>

    Added stability rule : <br>
    1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule.<br>
    2. If there is no support under any vertices of the bottom of the item, then fit = False.<br>


    '''
    return hello_world


# get all item and box information
@app.route("/getAllData", methods=["POST","GET"])
@cross_origin()
def getAllItemAndBoxAPI():
    ''' get all item and box information '''
    if flask.request.method == "POST":
        alldata["Success"] = True
        return flask.jsonify(alldata)
    else :
        return {"Success": False,"Reason":"can't use GET"}


# cal packing 
@app.route("/calPacking", methods=["POST"])
@cross_origin()
def mkResultAPI():
    '''
    '''
    res = {"Success": False}
    if flask.request.method == "POST":
        q= eval(flask.request.data.decode('utf-8'))
        if 'box' in q.keys() and 'item' in q.keys() and 'binding' in q.keys():
            try :
                packer,box,binding = getBoxAndItem(q)
            except :
                res["Reason"] = "input data err"
                return res
            try :
                # calculate packing
                packer.pack(bigger_first=True,distribute_items=False,fix_point=True,binding=binding,
                number_of_decimals=0)
                box = packer.bins[0]
                # make box dict
                box_r = makeDictBox(box)
                # make item dict
                fitItem,unfitItem = [],[]
                for item in box.items:
                    fitItem.append(makeDictItem(item))
                
                for item in box.unfitted_items:
                    unfitItem.append(makeDictItem(item))

                # for unfitem in box
                # make response
                res["Success"] = True
                res["data"] = {
                    "box" : box_r,
                    "fitItem" : fitItem,
                    "unfitItem": unfitItem
                }
                # print(len(res["data"]["unfitItem"]))
                return res
            except Exception as e:
                res['Reason'] = 'cal packing err'
                return res
        else :
            res['Reason'] = 'box or item not in input data'
            return res
    else :
        res['Reason'] = 'method not POST'
        return res


def makeDictBox(box):
    position = (int(box.width)/2,int(box.height)/2,int(box.depth)/2)
    r = {
            "partNumber" : box.partno,
            "position" : position,
            "WHD" : (int(box.width),int(box.height),int(box.depth)),
            "weight" : int(box.max_weight),
            "gravity" : box.gravity
        }
    return [r]


def makeDictItem(item):
    ''' '''

    if item.rotation_type == 0:
        pos = (int(item.position[0]) + int(item.width)//2,int(item.position[1])+ int(item.height)//2,int(item.position[2])+ int(item.depth)//2)
        whd = (int(item.width),int(item.height),int(item.depth))
    elif item.rotation_type == 1:
        pos = (int(item.position[0])+ int(item.height)//2,int(item.position[1]) + int(item.width)//2,int(item.position[2])+ int(item.depth)//2)
        whd = (int(item.height),int(item.width),int(item.depth))
    elif item.rotation_type == 2:
        pos = (int(item.position[0])+ int(item.height)//2,int(item.position[1])+ int(item.depth)//2,int(item.position[2]) + int(item.width)//2)
        whd = (int(item.height),int(item.depth),int(item.width))
    elif item.rotation_type == 3:
        pos = (int(item.position[0])+ int(item.depth)//2,int(item.position[1])+ int(item.height)//2,int(item.position[2]) + int(item.width)//2)
        whd = (int(item.depth),int(item.height),int(item.width))
    elif item.rotation_type == 4:
        pos = (int(item.position[0])+ int(item.depth)//2,int(item.position[1]) + int(item.width)//2,int(item.position[2])+ int(item.height)//2)
        whd = (int(item.depth),int(item.width),int(item.height))
    elif item.rotation_type == 5:
        pos = (int(item.position[0]) + int(item.width)//2,int(item.position[1])+ int(item.depth)//2,int(item.position[2])+ int(item.height)//2)
        whd = (int(item.width),int(item.depth),int(item.height))
    
    r = {
        "partNumber" : item.partno,
        "name" : item.name,
        "type" : item.typeof,
        "color" : item.color,
        "position" : pos,
        "rotationType" : item.rotation_type,
        "WHD" : whd,
        "weight" : int(item.weight)
    }

    return r


def getBoxAndItem(data):
    ''' '''
    # init packer
    packer = Packer()
    # get bin data
    box_data = data["box"][0]
    box = Bin(
        partno=box_data['name'],
        WHD=box_data['WHD'],
        max_weight=box_data['weight'],
        corner=box_data['coner'],
        put_type=box_data['openTop'][0]
        )
    packer.addBin(box)
    # get item data  TODO
    item_data = data["item"]
    color_dict = {
        1:'red',
        2:'yellow',
        3:'blue',
        4:'green',
        5:'purple',
        6:'brown',
        7:'orange'
    }
    for i in item_data :
        for j in range(i['count']) :
            packer.addItem(Item(
            partno = i['name']+'-{}'.format(str(j+1)),
            name = i['name'],
            typeof = 'cylinder' if i['type'] == 2 else 'cube',
            WHD = i['WHD'], 
            weight = i['weight'],
            level = 1 if i['level'] == 1 else 2,
            loadbear = i['loadbear'],
            updown = bool(i['updown']),
            color = randColor(i['color']))
        )
    binding_data = data['binding']
    binding = []
    if len(binding_data) != 0:
        for i in binding_data :
            binding.append(tuple(i))

    return packer,box,binding


def randColor(s):
    ''' '''
    random.seed(s)
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    return color



if __name__ == "__main__":
    '''
    1. get all item
    2. return choose item
    3. return result
    '''

    # start the web server
    print("* Starting web service...")
    app.run(host = '0.0.0.0',port = 5050,debug=True)