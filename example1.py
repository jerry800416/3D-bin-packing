from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

# init packing function
packer = Packer()
#  init bin
box = Bin('example1', (5.6875, 10.75, 15.0), 70.0,0)
packer.add_bin(box)
#  add item
packer.add_item(Item('50g [powder 1]', 'test',(3.9370, 1.9685, 1.9685), 1,1,100,True,'red'))
packer.add_item(Item('50g [powder 2]', 'test',(3.9370, 1.9685, 1.9685), 2,1,100,True,'blue'))
packer.add_item(Item('50g [powder 3]', 'test',(3.9370, 1.9685, 1.9685), 3,1,100,True,'gray'))
packer.add_item(Item('50g [powder 4]', 'test',(3.9370, 1.9685, 1.9685), 3,1,100,True,'orange'))
packer.add_item(Item('50g [powder 5]', 'test',(3.9370, 1.9685, 1.9685), 3,1,100,True,'lawngreen'))
packer.add_item(Item('50g [powder 6]', 'test',(3.9370, 1.9685, 1.9685), 3,1,100,True,'purple'))
packer.add_item(Item('50g [powder 7]', 'test',(5.1240, 1.1350, 1.5435), 3,1,100,True,'yellow'))
packer.add_item(Item('250g [powder 8]', 'test',(7.8740, 3.9370, 1.9685), 4,1,100,True,'pink'))
packer.add_item(Item('250g [powder 9]', 'test',(7.8740, 3.9370, 1.9685), 5,1,100,True,'brown'))
packer.add_item(Item('250g [powder 10]', 'test',(7.8740, 3.9370, 1.9685), 6,1,100,True,'cyan'))
packer.add_item(Item('250g [powder 11]', 'test',(7.8740, 3.9370, 1.9685), 7,1,100,True,'olive'))
packer.add_item(Item('250g [powder 12]', 'test',(7.8740, 3.9370, 1.9685), 8,1,100,True,'darkgreen'))
packer.add_item(Item('250g [powder 13]', 'test',(7.8740, 3.9370, 1.9685), 9,1,100,True,'orange'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

# print result
b = packer.bins[0]
volume = b.width * b.height * b.depth
print(":::::::::::", b.string())

print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''
for item in b.items:
    print("name : ",item.name)
    print("color : ",item.color)
    print("position : ",item.position)
    print("rotation type : ",item.rotation_type)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_t += float(item.width) * float(item.height) * float(item.depth)
    print("***************************************************")
print("***************************************************")
print("UNFITTED ITEMS:")
for item in b.unfitted_items:
    print("name : ",item.name)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.name)
    print("***************************************************")
print("***************************************************")
print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
print('residual volumn : ', float(volume) - volume_t )
print('unpack item : ',unfitted_name)
print('unpack item volumn : ',volume_f)
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
painter.plotBoxAndItems()