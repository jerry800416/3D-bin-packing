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
# try Bin('Bin', 5, 1, 6, 100), you can find different results.
box = Bin('Bin', 4, 3, 3, 100,0)
#  add item
# Item('item name', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.add_bin(box)
packer.add_item(Item('Box-1', (3, 2, 2), 1, 1, False, True, 'yellow'))
packer.add_item(Item('Box-2', (3, 2, 2), 1, 1, False, True, 'pink'))
packer.add_item(Item('Box-3', (3, 1, 2), 1, 1, False, True, 'brown'))
packer.add_item(Item('Box-4', (2, 2, 1), 1, 1, False, True, 'cyan'))
# packer.add_item(Item('Box-5', (2, 1, 3), 1, 1, False, True, 'olive'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

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
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
painter.plotBoxAndItems()