from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This case is used to demonstrate an example of a packing complex situation.

'''

# init packing function
packer = Packer()
#  init bin
box = Bin('example2',(30, 10, 15), 99,0,1)
packer.addBin(box)
#  add item
packer.addItem(Item('test1', 'test','cube',(9, 8, 7), 1, 1, 100, True,'red'))
packer.addItem(Item('test2', 'test','cube',(4, 25, 1), 1, 1, 100, True,'blue'))
packer.addItem(Item('test3', 'test','cube',(2, 13, 5), 1, 1, 100, True,'gray'))
packer.addItem(Item('test4', 'test','cube',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test5', 'test','cube',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test6', 'test','cube',(6, 5, 2), 1, 1, 100, True,'purple'))
packer.addItem(Item('test7', 'test','cube',(5, 2, 9), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test8', 'test','cube',(10, 8, 5), 1, 1, 100, True,'pink'))
packer.addItem(Item('test9', 'test','cube',(1, 3, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test10', 'test','cube',(8, 4, 7), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test11', 'test','cube',(2, 5, 3), 1, 1, 100, True,'olive'))
packer.addItem(Item('test12', 'test','cube',(1, 9, 2), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test13', 'test','cube',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test14', 'test','cube',(10, 2, 1), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test15', 'test','cube',(3, 2, 4), 1, 1, 100, True,'purple'))
packer.addItem(Item('test16', 'test','cube',(5, 7, 8), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test17', 'test','cube',(4, 8, 3), 1, 1, 100, True,'white'))
packer.addItem(Item('test18', 'test','cube',(2, 11, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test19', 'test','cube',(8, 3, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test20', 'test','cube',(7, 4, 5), 1, 1, 100, True,'olive'))
packer.addItem(Item('test21', 'test','cube',(2, 4, 11), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test22', 'test','cube',(1, 3, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test23', 'test','cube',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test24', 'test','cube',(7, 4, 5), 1, 1, 100, True,'purple'))
packer.addItem(Item('test25', 'test','cube',(2, 10, 3), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test26', 'test','cube',(3, 8, 1), 1, 1, 100, True,'pink'))
packer.addItem(Item('test27', 'test','cube',(7, 2, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test28', 'test','cube',(8, 9, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test29', 'test','cube',(4, 5, 10), 1, 1, 100, True,'olive'))
packer.addItem(Item('test30', 'test','cube',(10, 10, 2), 1, 1, 100, True,'darkgreen'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=100,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# print result
b = packer.bins[0]
volume = b.width * b.height * b.depth
print(":::::::::::", b.string())

print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''
for item in b.items:
    print("partno : ",item.partno)
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
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.partno)
    print("***************************************************")
print("***************************************************")
print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
print('residual volumn : ', float(volume) - volume_t )
print('unpack item : ',unfitted_name)
print('unpack item volumn : ',volume_f)
print("gravity distribution : ",b.gravity)
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
fig = painter.plotBoxAndItems(
    title=b.partno,
    alpha=0.8,
    write_num=False,
    fontsize=10
)
fig.show()