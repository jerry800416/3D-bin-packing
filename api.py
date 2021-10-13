
import flask, json
from py3dbp import Packer, Bin, Item
from flask_cors import cross_origin

# init flask
app = flask.Flask(__name__)


# a simple page that says hello
@app.route('/')
@cross_origin()
def hello():

    hello_world = '''
    welcome to 3D packing prob API_1.0
    '''
    return hello_world


# add person api
@app.route("/showdemo", methods=["GET"])
@cross_origin()
def mkResultAPI():
    '''
    '''
    # init packer and mk box and item
    packer,box = makeBoxAndItem()
    # calculate packing
    packer.pack(bigger_first=True,distribute_items=False,fix_point=True,binding=[],
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

    # for unitem in box
    # make response
    res = {"Success": False}
    if flask.request.method == "GET":
        res["Success"] = True
        res["data"] = {
            "box" : box_r,
            "fitItem" : fitItem,
            "unfitItem": unfitItem
        }
    print(len(res["data"]["unfitItem"]))
    
    return flask.jsonify(res)


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


def makeBoxAndItem():
    ''' '''
    # init packer , bin
    packer = Packer()
    # 長榮海運真實貨櫃(二十呎鋼製乾貨貨櫃) 單位 公分/公斤
    box = Bin(partno='Bin',WHD=(590,244,260),max_weight=28080,corner=15)
    packer.addBin(box)

    # 一台 dyson DC34 為20.5 * 11.5 * 32.2 (1.33kg)
    # 一箱 假設為64個 , 為 82 * 46 * 170 (85.12)
    for i in range(7): 
        packer.addItem(Item(
            partno='Dyson DC34 Animal{}'.format(str(i+1)),
            name='Dyson', 
            typeof='cylinder',
            WHD=(170, 82, 46), 
            weight=85.12,
            level=1,
            loadbear=100,
            updown=True,
            color='#FF0000')
        )
    
    # 洗衣機 一箱一個 850 * 600 *600 (10 kG)
    for i in range(18):
        packer.addItem(Item(
            partno='wash{}'.format(str(i+1)),
            name='wash',
            typeof='cube',
            WHD=(85, 60, 60), 
            weight=10,
            level=1,
            loadbear=100,
            updown=True,
            color='#FFFF37'
        ))

    # 42U 標準機櫃 : 一箱一個
    for i in range(15):
        packer.addItem(Item(
            partno='Cabinet{}'.format(str(i+1)),
            name='cabint',
            typeof='cube',
            WHD=(60, 80, 200), 
            weight=80,
            level=1,
            loadbear=100,
            updown=True,
            color='#842B00')
        )

    # 伺服器 : 一箱一個
    for i in range(42):
        packer.addItem(Item(
            partno='Server{}'.format(str(i+1)),
            name='server', 
            typeof='cube',
            WHD=(70, 100, 30), 
            weight=20,
            level=1,
            loadbear=100,
            updown=True,
            color='#0000E3')
        )
    
    
    return packer,box




if __name__ == "__main__":

    # start the web server
    print("* Starting web service...")
    app.run(host = '0.0.0.0',port = 5050,debug=True)