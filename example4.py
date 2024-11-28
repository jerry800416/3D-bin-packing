from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This example can be used to test large batch calculation time and binding functions.

'''

# init packing function
packer = Packer(packer_id = 'Example Packer')

# Evergreen Real Container (20ft Steel Dry Cargo Container)
# Unit cm/kg
box = Bin(
    bin_id='example4',
    WHD=(589.8,243.8,259.1),
    max_weight=28080,
    corner=15,
    put_type=0
)

packer.addBin(box)

# dyson DC34 (20.5 * 11.5 * 32.2 ,1.33kg)
# 64 pcs per case ,  82 * 46 * 170 (85.12)
for i in range(15): 
    packer.addItem(Item(
        item_id='Dyson DC34 Animal',
        typeof='cube',
        WHD=(170, 82, 46), 
        weight=85.12,
        priority_level=1,
        loadbear=100,
        updown=True,
        color='#FF0000')
    )

# washing machine (85 * 60 *60 ,10 kG)
# 1 pcs per case, 85 * 60 *60 (10)
for i in range(18):
    packer.addItem(Item(
        item_id='wash',
        typeof='cube',
        WHD=(85, 60, 60), 
        weight=10,
        priority_level=1,
        loadbear=100,
        updown=True,
        color='#FFFF37'
    ))

# 42U standard cabinet (60 * 80 * 200 , 80 kg)
# one per box, 60 * 80 * 200 (80)
for i in range(15):
    packer.addItem(Item(
        item_id='Cabinet',
        typeof='cube',
        WHD=(60, 80, 200), 
        weight=80,
        priority_level=1,
        loadbear=100,
        updown=True,
        color='#842B00')
    )

# Server (70 * 100 * 30 , 20 kg) 
# one per box , 70 * 100 * 30 (20)
for i in range(42):
    packer.addItem(Item(
        item_id='Server',
        typeof='cube',
        WHD=(70, 100, 30), 
        weight=20,
        priority_level=1,
        loadbear=100,
        updown=True,
        color='#0000E3')
    )


# calculate packing
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    # binding=[('server','cabint','wash')],
    # binding=['cabint','wash','server'],
    number_of_decimals=0
)

# print result
for box in packer.bins:

    volume = box.width * box.height * box.depth
    print(":::::::::::", box.string())

    print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''

    # '''
    for item in box.items:
        print("item_id : ",item.item_id)
        print("type : ",item.item_name)
        print("color : ",item.color)
        print("position : ",item.position)
        print("rotation type : ",item.rotation_type)
        print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    print("***************************************************")
    # '''
    print("UNFITTED ITEMS:")
    for item in box.unfitted_items:
        print("item_id : ",item.item_id)
        print("type : ",item.item_name)
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
    print("gravity distribution : ",box.gravity)
    # '''
    stop = time.time()
    print('used time : ',stop - start)

    # draw results
    painter = Painter(box)
    fig = painter.plotBoxAndItems(
        title=box.bin_id,
        alpha=0.2,
        write_name=False,
        fontsize=6
    )