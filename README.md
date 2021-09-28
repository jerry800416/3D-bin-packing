3D Bin Packing
====

3D Bin Packing improvements based on [this repository](https://github.com/enzoruiz/3dbinpacking). 

## improvement
1. fix item float on air :
    - ```[fix_point = False/True]``` The original packaging method did not consider the gravity problem. After the packaging was completed, there were items floating in the air, which greatly reduced the space utilization of the box. I solved this problem and improved the boxing rate.

2. Item bearing problem :
    - ```[loadbear = X]``` 
The original method did not consider the problem of project load-bearing, because load-bearing involves the structure, I used the priority to sort the projects with higher load-bearing capacity.The higher the number, the higher the priority.

3. Item need to pack :
    - ```[level = X]``` The priority can be set to sort which items should be packaged first, to ensure that these items will be packaged in bin.The lower the number, the higher the priority.

4. Items can be placed upside down or not :
    - ```[updown = False/True]``` True means the item can be placed upside down.

5. Complete set of items : 
    - ```[binding = [(orange,apple),(computer,hat,watch)]]``` Set of items can be set (ex. binding = [(orange,apple),(computer,hat,watch)]).

6. Container coner : 
    - ```[corner = X]``` Set the size of container corner, the unit is cm.

7. draw picture : 
    - ```[painter.plotBoxAndItems()]``` draw pictures.

## How to use

init bin : 
```
box1 = Bin(
    name='Bin',           # name / PN of item (unique value)
    WHD=(589,243,259),    # (width , height , depth)
    max_weight=28080,     # box can bear the weight
    corner=15             # container coner
    )
```
init item : 
```
item1 = Item(
        name='testItem',   # name / PN of item (unique value)
        typeof='wash',     # type of item
        WHD=(85, 60, 60),  # (width , height , depth)
        weight=10,         # item weight
        level=1,           # priority (Item need to pack)
        loadbear=100,      # Item bearing
        updown=True,       # Item bearing
        color='#FFFF37'    # set item color , you also can use color='red' 
    )
```
init packer : 
```
packer = Packer()          # packer init
```
add bin and items to packer : 
```
packer.add_bin(box1)       # adding bins to packer
packer.add_item(item1)     # adding items to packer
```
start pack items : 
```
packer.pack(
    bigger_first=True,                 # bigger item first
    fix_point=True,                    # fix item float problem
    binding=[('server','cabint')],     # Complete set of items
)
```
After packing:
```
packer.bins[0]              # get bin of packer
my_bin.items                # get fitted items in bin
my_bin.unfitted_items       # get unfitted items 
```

## Example
```

from py3dbp import Packer, Bin, Item
import time

start = time.time()

# init packing function
packer = Packer()

#  init bin
box = Bin('example2',(30, 10, 15), 99,0)
packer.add_bin(box)

#  add item
packer.add_item(Item('test1', 'test',(9, 8, 7), 1, 1, 100, True,'red'))
packer.add_item(Item('test2', 'test',(4, 25, 1), 1, 1, 100, True,'blue'))
packer.add_item(Item('test3', 'test',(2, 13, 5), 1, 1, 100, True,'gray'))
packer.add_item(Item('test4', 'test',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.add_item(Item('test5', 'test',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.add_item(Item('test6', 'test',(6, 5, 2), 1, 1, 100, True,'purple'))
packer.add_item(Item('test7', 'test',(5, 2, 9), 1, 1, 100, True,'yellow'))
packer.add_item(Item('test8', 'test',(10, 8, 5), 1, 1, 100, True,'pink'))
packer.add_item(Item('test9', 'test',(1, 3, 5), 1, 1, 100, True,'brown'))
packer.add_item(Item('test10', 'test',(8, 4, 7), 1, 1, 100, True,'cyan'))
packer.add_item(Item('test11', 'test',(2, 5, 3), 1, 1, 100, True,'olive'))
packer.add_item(Item('test12', 'test',(1, 9, 2), 1, 1, 100, True,'darkgreen'))
packer.add_item(Item('test13', 'test',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.add_item(Item('test14', 'test',(10, 2, 1), 1, 1, 100, True,'lawngreen'))
packer.add_item(Item('test15', 'test',(3, 2, 4), 1, 1, 100, True,'purple'))
packer.add_item(Item('test16', 'test',(5, 7, 8), 1, 1, 100, True,'yellow'))
packer.add_item(Item('test17', 'test',(4, 8, 3), 1, 1, 100, True,'white'))
packer.add_item(Item('test18', 'test',(2, 11, 5), 1, 1, 100, True,'brown'))
packer.add_item(Item('test19', 'test',(8, 3, 5), 1, 1, 100, True,'cyan'))
packer.add_item(Item('test20', 'test',(7, 4, 5), 1, 1, 100, True,'olive'))
packer.add_item(Item('test21', 'test',(2, 4, 11), 1, 1, 100, True,'darkgreen'))
packer.add_item(Item('test22', 'test',(1, 3, 4), 1, 1, 100, True,'orange'))
packer.add_item(Item('test23', 'test',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.add_item(Item('test24', 'test',(7, 4, 5), 1, 1, 100, True,'purple'))
packer.add_item(Item('test25', 'test',(2, 10, 3), 1, 1, 100, True,'yellow'))
packer.add_item(Item('test26', 'test',(3, 8, 1), 1, 1, 100, True,'pink'))
packer.add_item(Item('test27', 'test',(7, 2, 5), 1, 1, 100, True,'brown'))
packer.add_item(Item('test28', 'test',(8, 9, 5), 1, 1, 100, True,'cyan'))
packer.add_item(Item('test29', 'test',(4, 5, 10), 1, 1, 100, True,'olive'))
packer.add_item(Item('test30', 'test',(10, 10, 2), 1, 1, 100, True,'darkgreen'))

# calculate packing 
packer.pack(bigger_first=True,distribute_items=100,fix_point=True,number_of_decimals=0)

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

```

## Reference

* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d
* [Optimizing three-dimensional bin packing through simulation](reference/OPTIMIZING THREE-DIMENSIONAL BIN PACKING THROUGH SIMULATION.pdf)
* https://github.com/enzoruiz/3dbinpacking
* https://github.com/nmingotti/3dbinpacking
