from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

# init packing function
packer = Packer()
#  init bin
box = Bin('example1', 5.6875, 10.75, 15.0, 70.0)
packer.add_bin(box)
#  add item
packer.add_item(Item('50g [powder 1]', 3.9370, 1.9685, 1.9685, 1,'red'))
packer.add_item(Item('50g [powder 2]', 3.9370, 1.9685, 1.9685, 2,'blue'))
packer.add_item(Item('50g [powder 3]', 3.9370, 1.9685, 1.9685, 3,'gray'))
packer.add_item(Item('50g [powder 4]', 3.9370, 1.9685, 1.9685, 3,'orange'))
packer.add_item(Item('50g [powder 5]', 3.9370, 1.9685, 1.9685, 3,'lawngreen'))
packer.add_item(Item('50g [powder 6]', 3.9370, 1.9685, 1.9685, 3,'purple'))
packer.add_item(Item('50g [powder 7]', 5.1240, 1.1350, 1.5435, 3,'yellow'))
packer.add_item(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 4,'pink'))
packer.add_item(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 5,'brown'))
packer.add_item(Item('250g [powder 10]', 7.8740, 3.9370, 1.9685, 6,'cyan'))
packer.add_item(Item('250g [powder 11]', 7.8740, 3.9370, 1.9685, 7,'olive'))
packer.add_item(Item('250g [powder 12]', 7.8740, 3.9370, 1.9685, 8,'darkgreen'))
packer.add_item(Item('250g [powder 13]', 7.8740, 3.9370, 1.9685, 9,'orange'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=False,fix_depth=True,number_of_decimals=0)

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