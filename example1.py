from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This example is used to demonstrate the mixed packing of cube and cylinder.

'''

# init packing function
packer = Packer()
#  init bin
box = Bin('example1', (5.6875, 10.75, 15.0), 70.0,0,0)
packer.addBin(box)
#  add item
packer.addItem(Item('50g [powder 1]', 'test','cube',(2, 2, 4), 1,1,100,True,'red'))
packer.addItem(Item('50g [powder 2]', 'test','cube',(2, 2, 4), 2,1,100,True,'blue'))
packer.addItem(Item('50g [powder 3]', 'test','cube',(2, 2, 4), 3,1,100,True,'gray'))
packer.addItem(Item('50g [powder 4]', 'test','cube',(2, 2, 4), 3,1,100,True,'orange'))
packer.addItem(Item('50g [powder 5]', 'test','cylinder',(2, 2, 4), 3,1,100,True,'lawngreen'))
packer.addItem(Item('50g [powder 6]', 'test','cylinder',(2, 2, 4), 3,1,100,True,'purple'))
packer.addItem(Item('50g [powder 7]', 'test','cylinder',(1, 1, 5), 3,1,100,True,'yellow'))
packer.addItem(Item('250g [powder 8]', 'test','cylinder',(4, 4, 2), 4,1,100,True,'pink'))
packer.addItem(Item('250g [powder 9]', 'test','cylinder',(4, 4, 2), 5,1,100,True,'brown'))
packer.addItem(Item('250g [powder 10]', 'test','cube',(4, 4, 2), 6,1,100,True,'cyan'))
packer.addItem(Item('250g [powder 11]', 'test','cylinder',(4, 4, 2), 7,1,100,True,'olive'))
packer.addItem(Item('250g [powder 12]', 'test','cylinder',(4, 4, 2), 8,1,100,True,'darkgreen'))
packer.addItem(Item('250g [powder 13]', 'test','cube',(4, 4, 2), 9,1,100,True,'orange'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=False,
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
    alpha=0.2,
    write_num=False,
    fontsize=5
)
fig.show()