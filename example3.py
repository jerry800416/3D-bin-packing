from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This example is used to demonstrate that the algorithm does not optimize.

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example3', (6, 1, 5), 100,0,put_type=0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
# If all item WHD=(2, 1, 3) , item can be fully packed into box, but if choose one item and modify WHD=(3, 1, 2) , item can't be fully packed into box.
packer.addItem(Item(partno='Box-1',name='test',typeof='cube', WHD=(2, 1, 3), weight=1, level=1,loadbear=100, updown=True, color='yellow'))
packer.addItem(Item(partno='Box-2',name='test',typeof='cube', WHD=(3, 1, 2), weight=1, level=1,loadbear=100, updown=True, color='pink')) # Try switching WHD=(3, 1, 2) and (2, 1, 3) to compare the results
packer.addItem(Item(partno='Box-3',name='test',typeof='cube', WHD=(2, 1, 3), weight=1,level= 1,loadbear=100, updown=True, color='brown'))
packer.addItem(Item(partno='Box-4',name='test',typeof='cube', WHD=(2, 1, 3), weight=1, level=1,loadbear=100, updown=True, color='cyan'))
packer.addItem(Item(partno='Box-5',name='test',typeof='cube', WHD=(2, 1, 3), weight=1, level=1,loadbear=100, updown=True, color='olive'))

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
    alpha=0.8,
    write_num=False,
    fontsize=10
)
fig.show()