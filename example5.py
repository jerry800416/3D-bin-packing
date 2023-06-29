from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

Check stability on item - first rule
1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule. 

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example5', (5, 4, 3), 100,0,0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
packer.addItem(Item(partno='Box-3', name='test', typeof='cube', WHD=(2, 5, 2), weight=1, level=1,loadbear=100, updown=True, color='pink'))
packer.addItem(Item(partno='Box-3', name='test', typeof='cube', WHD=(2, 3, 2), weight=1, level=2,loadbear=100, updown=True, color='pink')) # Try switching WHD=(2, 2, 2) and (2, 3, 2) to compare the results
packer.addItem(Item(partno='Box-4', name='test', typeof='cube', WHD=(5, 4, 1), weight=1,level=3,loadbear=100, updown=True, color='brown'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# put order
packer.putOrder()

# print result
for b in packer.bins:
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