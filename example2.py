from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This case is used to demonstrate an example of a packing complex situation.

'''

# init packing function
packer = Packer(packer_id = 'Example Packer')
#  init bin
box = Bin((30, 10, 15), 99, bin_id='example2', corner=0, put_type=1)
packer.addBin(box)
#  add item
packer.addItem(Item((9, 8, 7), 1, 1, True, 'red', 100, 'test1', 'test', 'cube'))
packer.addItem(Item((4, 25, 1), 1, 1, True, 'blue', 100, 'test2', 'test', 'cube'))
packer.addItem(Item((2, 13, 5), 1, 1, True, 'gray', 100, 'test3', 'test', 'cube'))
packer.addItem(Item((7, 5, 4), 1, 1, True, 'orange', 100, 'test4', 'test', 'cube'))
packer.addItem(Item((10, 5, 2), 1, 1, True, 'lawngreen', 100, 'test5', 'test', 'cube'))
packer.addItem(Item((6, 5, 2), 1, 1, True, 'purple', 100, 'test6', 'test', 'cube'))
packer.addItem(Item((5, 2, 9), 1, 1, True, 'yellow', 100, 'test7', 'test', 'cube'))
packer.addItem(Item((10, 8, 5), 1, 1, True, 'pink', 100, 'test8', 'test', 'cube'))
packer.addItem(Item((1, 3, 5), 1, 1, True, 'brown', 100, 'test9', 'test', 'cube'))
packer.addItem(Item((8, 4, 7), 1, 1, True, 'cyan', 100, 'test10', 'test', 'cube'))
packer.addItem(Item((2, 5, 3), 1, 1, True, 'olive', 100, 'test11', 'test', 'cube'))
packer.addItem(Item((1, 9, 2), 1, 1, True, 'darkgreen', 100, 'test12', 'test', 'cube'))
packer.addItem(Item((7, 5, 4), 1, 1, True, 'orange', 100, 'test13', 'test', 'cube'))
packer.addItem(Item((10, 2, 1), 1, 1, True, 'lawngreen', 100, 'test14', 'test', 'cube'))
packer.addItem(Item((3, 2, 4), 1, 1, True, 'purple', 100, 'test15', 'test', 'cube'))
packer.addItem(Item((5, 7, 8), 1, 1, True, 'yellow', 100, 'test16', 'test', 'cube'))
packer.addItem(Item((4, 8, 3), 1, 1, True, 'white', 100, 'test17', 'test', 'cube'))
packer.addItem(Item((2, 11, 5), 1, 1, True, 'brown', 100, 'test18', 'test', 'cube'))
packer.addItem(Item((8, 3, 5), 1, 1, True, 'cyan', 100, 'test19', 'test', 'cube'))
packer.addItem(Item((7, 4, 5), 1, 1, True, 'olive', 100, 'test20', 'test', 'cube'))
packer.addItem(Item((2, 4, 11), 1, 1, True, 'darkgreen', 100, 'test21', 'test', 'cube'))
packer.addItem(Item((1, 3, 4), 1, 1, True, 'orange', 100, 'test22', 'test', 'cube'))
packer.addItem(Item((10, 5, 2), 1, 1, True, 'lawngreen', 100, 'test23', 'test', 'cube'))
packer.addItem(Item((7, 4, 5), 1, 1, True, 'purple', 100, 'test24', 'test', 'cube'))
packer.addItem(Item((2, 10, 3), 1, 1, True, 'yellow', 100, 'test25', 'test', 'cube'))
packer.addItem(Item((3, 8, 1), 1, 1, True, 'pink', 100, 'test26', 'test', 'cube'))
packer.addItem(Item((7, 2, 5), 1, 1, True, 'brown', 100, 'test27', 'test', 'cube'))
packer.addItem(Item((8, 9, 5), 1, 1, True, 'cyan', 100, 'test28', 'test', 'cube'))
packer.addItem(Item((4, 5, 10), 1, 1, True, 'olive', 100, 'test29', 'test', 'cube'))
packer.addItem(Item((10, 10, 2), 1, 1, True, 'darkgreen', 100, 'test30', 'test', 'cube'))

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
    print("item_id : ",item.item_id)
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
    print("item_id : ",item.item_id)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.item_id)
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
    title=b.bin_id,
    alpha=0.8,
    write_name=False,
    fontsize=10
)