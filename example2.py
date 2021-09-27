from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

# init packing function
packer = Packer()
#  init bin
box = Bin('example2',30, 10, 15, 99,0)
packer.add_bin(box)
#  add item
packer.add_item(Item('test1', (9, 8, 7), 1, 1, False, True,'red'))
packer.add_item(Item('test2', (4, 25, 1), 1, 1, False, True,'blue'))
packer.add_item(Item('test3', (2, 13, 5), 1, 1, False, True,'gray'))
packer.add_item(Item('test4', (7, 5, 4), 1, 1, False, True,'orange'))
packer.add_item(Item('test5', (10, 5, 2), 1, 1, False, True,'lawngreen'))
packer.add_item(Item('test6', (6, 5, 2), 1, 1, False, True,'purple'))
packer.add_item(Item('test7', (5, 2, 9), 1, 1, False, True,'yellow'))
packer.add_item(Item('test8', (10, 8, 5), 1, 1, False, True,'pink'))
packer.add_item(Item('test9', (1, 3, 5), 1, 1, False, True,'brown')) #TODO
packer.add_item(Item('test10', (8, 4, 7), 1, 1, False, True,'cyan'))
packer.add_item(Item('test11', (2, 5, 3), 1, 1, False, True,'olive'))
packer.add_item(Item('test12', (1, 9, 2), 1, 1, False, True,'darkgreen'))
packer.add_item(Item('test13', (7, 5, 4), 1, 1, False, True,'orange'))
packer.add_item(Item('test14', (10, 2, 1), 1, 1, False, True,'lawngreen'))
packer.add_item(Item('test15', (3, 2, 4), 1, 1, False, True,'purple'))
packer.add_item(Item('test16', (5, 7, 8), 1, 1, False, True,'yellow'))
packer.add_item(Item('test17', (4, 8, 3), 1, 1, False, True,'white'))
packer.add_item(Item('test18', (2, 11, 5), 1, 1, False, True,'brown'))
packer.add_item(Item('test19', (8, 3, 5), 1, 1, False, True,'cyan'))
packer.add_item(Item('test20', (7, 4, 5), 1, 1, False, True,'olive'))
packer.add_item(Item('test21', (2, 4, 11), 1, 1, False, True,'darkgreen'))
packer.add_item(Item('test22', (1, 3, 4), 1, 1, False, True,'orange'))
packer.add_item(Item('test23', (10, 5, 2), 1, 1, False, True,'lawngreen'))
packer.add_item(Item('test24', (7, 4, 5), 1, 1, False, True,'purple'))
packer.add_item(Item('test25', (2, 10, 3), 1, 1, False, True,'yellow'))
packer.add_item(Item('test26',(3, 8, 1), 1, 1, False, True,'pink'))
packer.add_item(Item('test27', (7, 2, 5), 1, 1, False, True,'brown'))
packer.add_item(Item('test28', (8, 9, 5), 1, 1, False, True,'cyan'))
packer.add_item(Item('test29', (4, 5, 10), 1, 1, False, True,'olive'))
packer.add_item(Item('test30', (10, 10, 2), 1, 1, False, True,'darkgreen'))

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