from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

'''
# Packing Priority level
0 : None
1 : Must have
2~3 
'''
# init packing function
packer = Packer()
#  init bin 
box = Bin('Bin', (5, 5, 5), 100,0,0)
#  add item
# Item('item name', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
packer.addItem(Item(name='Box-1',typeof='test', WHD=(5, 1, 5), weight=1, level=1,loadbear=100, updown=True, color='yellow'))
packer.addItem(Item(name='Box-2',typeof='test', WHD=(1, 4, 5), weight=1, level=2,loadbear=100, updown=True, color='pink'))
packer.addItem(Item(name='Box-3',typeof='test', WHD=(1, 1, 5), weight=1,level= 4,loadbear=100, updown=True, color='brown'))
packer.addItem(Item(name='Box-4',typeof='test', WHD=(3, 3, 5), weight=1, level=3,loadbear=100, updown=True, color='cyan'))
# packer.addItem(Item(name='Box-5',typeof='test', WHD=(4, 2, 5), weight=1, level=1,loadbear=100, updown=True, color='olive'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

# put order
packer.putOrder()

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
print("gravity distribution : ",b.gravity)
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
painter.plotBoxAndItems()