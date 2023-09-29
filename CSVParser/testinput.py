import random
import csv

from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

COLORS = ["yellow", "olive", "pink", "brown", "red", "blue", "green", "purple", "orange", "gray"]
# Initialize variables to store bins and items
bins = []
bin_size = -1
items = []
item_size = 0
counter = 0

with open('testval2.csv', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Iterate through the rows and parse bins and items
    for row in csv_reader:
        # Check if the row is empty
        if not any(row):
            continue

        # If there is a single number in the row, it represents the number of bins or items
        if row[1] == "":
            num = int(row[0])
            if bin_size == -1:
                bin_size = num
                counter = bin_size
            else:
                item_size = num
        else:
            a = row[0]
            b = row[1]
            values = tuple(int(val) for val in row if val)
            if counter > 0:
                bins.append(values)
                counter -= 1
            else:
                items.append(values)

# init packing function
packer = Packer()
#  init bin
for i in range(len(bins)):
    box = Bin('Bin{}'.format(str(i+1)), bins[i], 100, 0, 0)
    packer.addBin(box)

#  add item
for i in range(len(items)):
    packer.addItem(Item(
        partno='Box-{}'.format(str(i+1)),
        name='test{}'.format(str(i+1)),
        typeof='cube',
        WHD=items[i],
        weight=1,
        level=1,
        loadbear=100,
        updown=True,
        color=random.choice(COLORS)
        )
    )
# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
# packer.addItem(Item(partno='Box-1', name='test1', typeof='cube', WHD=(5, 4, 1), weight=1, level=1,loadbear=100, updown=True, color='yellow'))
# packer.addItem(Item(partno='Box-2', name='test2', typeof='cube', WHD=(1, 2, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-3', name='test3', typeof='cube', WHD=(1, 2, 3), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-4', name='test4', typeof='cube', WHD=(1, 2, 2), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-5', name='test5', typeof='cube', WHD=(1, 2, 3), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-6', name='test6', typeof='cube', WHD=(1, 2, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-7', name='test7', typeof='cube', WHD=(1, 2, 2), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-8', name='test8', typeof='cube', WHD=(1, 2, 3), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-9', name='test9', typeof='cube', WHD=(1, 2, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-10', name='test10', typeof='cube', WHD=(1, 2, 3), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-11', name='test11', typeof='cube', WHD=(1, 2, 2), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-12', name='test12', typeof='cube', WHD=(5, 4, 1), weight=1, level=1,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-13', name='test13', typeof='cube', WHD=(1, 1, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-14', name='test14', typeof='cube', WHD=(1, 2, 1), weight=1, level=1,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-15', name='test15', typeof='cube', WHD=(1, 2, 1), weight=1, level=1,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-16', name='test16', typeof='cube', WHD=(1, 1, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-17', name='test17', typeof='cube', WHD=(1, 1, 4), weight=1, level=1,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-18', name='test18', typeof='cube', WHD=(5, 4, 2), weight=1, level=1,loadbear=100, updown=True, color='brown'))

# calculate packing
packer.pack(
    bigger_first=True,
    # Change distribute_items=False to compare the packing situation in multiple boxes of different capacities.
    distribute_items=True,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# put order
packer.putOrder()

# print result
print("***************************************************")
for idx,b in enumerate(packer.bins) :
    print("**", b.string(), "**")
    print("***************************************************")
    print("FITTED ITEMS:")
    print("***************************************************")
    volume = b.width * b.height * b.depth
    volume_t = 0
    volume_f = 0
    unfitted_name = ''
    for item in b.items:
        print("partno : ",item.partno)
        print("color : ",item.color)
        print("position : ",item.position)
        print("rotation type : ",item.rotation_type)
        print("W*H*D : ",str(item.width) +' * '+ str(item.height) +' * '+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")

    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
    print('residual volumn : ', float(volume) - volume_t )
    print("gravity distribution : ",b.gravity)
    print("***************************************************")
    # draw results
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.8,
        write_num=False,
        fontsize=10
    )

print("***************************************************")
print("UNFITTED ITEMS:")
for item in packer.unfit_items:
    print("***************************************************")
    print('name : ',item.name)
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +' * '+ str(item.height) +' * '+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.partno)
    print("***************************************************")
print("***************************************************")
print('unpack item : ',unfitted_name)
print('unpack item volumn : ',volume_f)

stop = time.time()
print('used time : ',stop - start)

fig.show()