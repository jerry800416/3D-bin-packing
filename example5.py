from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

Check stability on item - first rule
1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule. 

'''

# init packing function
packer = Packer( packer_id = 'Example Packer')
#  init bin 
box = Bin(WHD=(5, 4, 3), max_weight=100, bin_id='example5', corner=0, put_type=0)
#  add item
# Item('item item_id', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
packer.addItem(Item(item_id='Box-3', typeof='cube', WHD=(2, 5, 2), weight=1, priority_level=1, loadbear=100, updown=True, color='pink'))
packer.addItem(Item(item_id='Box-3', typeof='cube', WHD=(2, 3, 2), weight=1, priority_level=2, loadbear=100, updown=True, color='pink')) # Try switching WHD=(2, 2, 2) and (2, 3, 2) to compare the results
packer.addItem(Item(item_id='Box-4', typeof='cube', WHD=(5, 4, 1), weight=1, priority_level=3, loadbear=100, updown=True, color='brown'))

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
