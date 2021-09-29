from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

# init packing function
packer = Packer()
#  init bin
box = Bin('example2',(30, 10, 15), 99,0)
packer.addBin(box)
#  add item
packer.addItem(Item('test1', 'test',(9, 8, 7), 1, 1, 100, True,'red'))
packer.addItem(Item('test2', 'test',(4, 25, 1), 1, 1, 100, True,'blue'))
packer.addItem(Item('test3', 'test',(2, 13, 5), 1, 1, 100, True,'gray'))
packer.addItem(Item('test4', 'test',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test5', 'test',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test6', 'test',(6, 5, 2), 1, 1, 100, True,'purple'))
packer.addItem(Item('test7', 'test',(5, 2, 9), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test8', 'test',(10, 8, 5), 1, 1, 100, True,'pink'))
packer.addItem(Item('test9', 'test',(1, 3, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test10', 'test',(8, 4, 7), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test11', 'test',(2, 5, 3), 1, 1, 100, True,'olive'))
packer.addItem(Item('test12', 'test',(1, 9, 2), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test13', 'test',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test14', 'test',(10, 2, 1), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test15', 'test',(3, 2, 4), 1, 1, 100, True,'purple'))
packer.addItem(Item('test16', 'test',(5, 7, 8), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test17', 'test',(4, 8, 3), 1, 1, 100, True,'white'))
packer.addItem(Item('test18', 'test',(2, 11, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test19', 'test',(8, 3, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test20', 'test',(7, 4, 5), 1, 1, 100, True,'olive'))
packer.addItem(Item('test21', 'test',(2, 4, 11), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test22', 'test',(1, 3, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test23', 'test',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test24', 'test',(7, 4, 5), 1, 1, 100, True,'purple'))
packer.addItem(Item('test25', 'test',(2, 10, 3), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test26', 'test',(3, 8, 1), 1, 1, 100, True,'pink'))
packer.addItem(Item('test27', 'test',(7, 2, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test28', 'test',(8, 9, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test29', 'test',(4, 5, 10), 1, 1, 100, True,'olive'))
packer.addItem(Item('test30', 'test',(10, 10, 2), 1, 1, 100, True,'darkgreen'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=100,fix_point=True,number_of_decimals=0)

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