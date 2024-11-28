from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''

This example is used to demonstrate the mixed packing of cube and cylinder.

'''

# init packing function
packer = Packer(packer_id='Example Packer')
# init bin
box = Bin(WHD=(5.6875, 8, 10.0), max_weight=700.0, bin_id='example1')
packer.addBin(box)
# add items
packer.addItem(Item(WHD=(2, 2, 4), weight=10, priority_level=1, updown=True, color='red', loadbear=7.5, item_id='10kg/7.5kg/Prio1', item_name='test', typeof='cube'))
packer.addItem(Item(WHD=(2, 2, 4), weight=8, priority_level=1, updown=True, color='blue', loadbear=7.5, item_id='8kg/7.5kg/Prio1', item_name='test', typeof='cube'))
packer.addItem(Item(WHD=(2, 2, 4), weight=8, priority_level=2, updown=True, color='gray', loadbear=4, item_id='8kg/4kg/Prio2', item_name='test', typeof='cube'))
packer.addItem(Item(WHD=(2, 2, 3), weight=3.5, priority_level=1, updown=True, color='orange', loadbear=2, item_id='3.5kg/2kg/Prio1', item_name='test', typeof='cube'))
packer.addItem(Item(WHD=(3, 2, 4), weight=9, priority_level=1, updown=True, color='lawngreen', loadbear=8, item_id='9kg/8kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(3, 2, 4), weight=8, priority_level=2, updown=True, color='purple', loadbear=8, item_id='8kg/8kg/Prio2', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(3, 1, 5), weight=9, priority_level=1, updown=True, color='yellow', loadbear=8, item_id='9kg/8kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(4, 4, 2), weight=3, priority_level=1, updown=True, color='pink', loadbear=2, item_id='3kg/2kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(4, 4, 2), weight=3, priority_level=1, updown=True, color='brown', loadbear=2.5, item_id='3kg/2.5kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(4, 4, 2), weight=11, priority_level=1, updown=True, color='cyan', loadbear=10, item_id='11kg/10kg/Prio1', item_name='test', typeof='cube'))
packer.addItem(Item(WHD=(2, 2, 2), weight=1.5, priority_level=1, updown=True, color='olive', loadbear=1.5, item_id='1.5kg/1.5kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(2, 2, 1), weight=2, priority_level=1, updown=True, color='darkgreen', loadbear=2, item_id='2kg/2kg/Prio1', item_name='test', typeof='cylinder'))
packer.addItem(Item(WHD=(5, 2, 2), weight=2.5, priority_level=1, updown=True, color='orange', loadbear=1, item_id='2.5kg/1kg/Prio1', item_name='test', typeof='cube'))

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
    print("item_id : ", item.item_id)
    print("color : ", item.color)
    print("position : ", item.position)
    print("rotation type : ", item.rotation_type)
    print("W*H*D : ", str(item.width) + '*' + str(item.height) + '*' + str(item.depth))
    print("volume : ", float(item.width) * float(item.height) * float(item.depth))
    print("weight : ", float(item.weight))
    volume_t += float(item.width) * float(item.height) * float(item.depth)
    print("***************************************************")
print("***************************************************")
print("UNFITTED ITEMS:")
for item in b.unfitted_items:
    print("item_id : ", item.item_id)
    print("color : ", item.color)
    print("W*H*D : ", str(item.width) + '*' + str(item.height) + '*' + str(item.depth))
    print("volume : ", float(item.width) * float(item.height) * float(item.depth))
    print("weight : ", float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.item_id)
    print("***************************************************")
print("***************************************************")
print('space utilization : {}%'.format(round(volume_t / float(volume) * 100, 2)))
print('residual volume : ', float(volume) - volume_t)
print('unpack item : ', unfitted_name)
print('unpack item volume : ', volume_f)
print("gravity distribution : ", b.gravity)
stop = time.time()
print('used time : ', stop - start)

# draw results
painter = Painter(b)
fig = painter.plotBoxAndItems(
    title=b.bin_id,
    alpha=0.2,
    write_name=True,
    fontsize=10
)
