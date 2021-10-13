from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()

# init packing function
packer = Packer()

# 長榮海運真實貨櫃(二十呎鋼製乾貨貨櫃)
# 單位 公分/公斤
box = Bin(
    partno='Bin',
    WHD=(589.8,243.8,259.1),
    max_weight=28080,
    corner=15,
    put_type=0
)
packer.addBin(box)

# 一台 dyson DC34 為20.5 * 11.5 * 32.2 (1.33kg)
# 一箱 假設為64個 , 為 82 * 46 * 170 (85.12)
for i in range(15): 
    packer.addItem(Item(
        partno='Dyson DC34 Animal{}'.format(str(i+1)),
        name='Dyson', 
        typeof='cube',
        WHD=(170, 82, 46), 
        weight=85.12,
        level=1,
        loadbear=100,
        updown=True,
        color='#FF0000')
    )

# 洗衣機 一箱一個 850 * 600 *600 (10 kG)
for i in range(18):
    packer.addItem(Item(
        partno='wash{}'.format(str(i+1)),
        name='wash',
        typeof='cube',
        WHD=(85, 60, 60), 
        weight=10,
        level=1,
        loadbear=100,
        updown=True,
        color='#FFFF37'
    ))

# 42U 標準機櫃 : 一箱一個
for i in range(15):
    packer.addItem(Item(
        partno='Cabinet{}'.format(str(i+1)),
        name='cabint',
        typeof='cube',
        WHD=(60, 80, 200), 
        weight=80,
        level=1,
        loadbear=100,
        updown=True,
        color='#842B00')
    )

# 伺服器 : 一箱一個
for i in range(42):
    packer.addItem(Item(
        partno='Server{}'.format(str(i+1)),
        name='server',
        typeof='cube',
        WHD=(70, 100, 30), 
        weight=20,
        level=1,
        loadbear=100,
        updown=True,
        color='#0000E3')
    )


# calculate packing
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    # binding=[('server','cabint','wash')],
    binding=['cabint','wash','server'],
    number_of_decimals=0
)

# print result
box = packer.bins[0]
volume = box.width * box.height * box.depth
print(":::::::::::", box.string())

print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''

# '''
for item in box.items:
    print("partno : ",item.partno)
    print("type : ",item.name)
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
    print("partno : ",item.partno)
    print("type : ",item.name)
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
print("gravity distribution : ",box.gravity)
# '''
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(box)
painter.plotBoxAndItems()