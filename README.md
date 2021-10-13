3D Bin Packing
====

3D Bin Packing improvements based on [this repository](https://github.com/enzoruiz/3dbinpacking). 

<img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/3.jpeg" width="600"/>

## improvement
1. fix item float :
    - ```[fix_point = False/True] type bool``` The original packaging method did not consider the gravity problem. After the packaging was completed, there were items floating in the air, which greatly reduced the space utilization of the box. I solved this problem and improved the boxing rate.

Original packaging  |  Used fix point
:-------------------------:|:-------------------------:
<img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/1.jpg" width="400"/>  |  <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/2.jpg" width="400"/>

2. Item bearing problem :
    - ```[loadbear = X] type int``` 
The original method did not consider the problem of project load-bearing, because load-bearing involves the structure, I used the priority to sort the projects with higher load-bearing capacity.The higher the number, the higher the priority.

3. Item need to pack :
    - ```[level = X] type int``` The priority can be set to sort which items should be packaged first, to ensure that these items will be packaged in bin.The lower the number, the higher the priority.

4. Items can be placed upside down or not :
    - ```[updown = False/True] type bool``` True means the item can be placed upside down.

5. Make a set of items : 
    - ```[binding = [(orange,apple),(computer,hat,watch)]] type tuple in list``` The number of items in the set must be the same in the bin(ex. binding = [(orange,apple),(computer,hat,watch)]).

6. Container coner : 
    - ```[corner = X] type int``` Set the size of container corner, the unit is cm.

7. Draw picture : 
    - ```[painter.plotBoxAndItems()]``` Draw pictures.

8. Calculate gravity distribution :
    - ```print("gravity distribution : ",bin.gravity) ``` Divide the bin into four equal parts, and calculate the weight ratio of the equal parts. Ideally, the weight ratio of each equal part tends to be close.

9. Add the order of placing items :
    - ```put_type=0 or 1 (0 : general & 1 : open top)``` Added the order of placing items. There are two placement methods. Set the bin to open top or general, and the returned results are sorted according to this method.

10. Mixed cube and cylinder : 
    - ```typeof=cube or cylinder ``` mixed with cube and cylinder .

<img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/4.jpeg" width="600"/>

## How to use

Init bin : 
```
box1 = Bin(
    partno='Bin',         # partno / PN of item (unique value)
    WHD=(589,243,259),    # (width , height , depth)
    max_weight=28080,     # box can bear the weight
    corner=15             # container coner
    put_type= 1           # add the order of placing items
    )
```
Init item : 
```
item1 = Item(
        partno='testItem', # partno / PN of item (unique value)
        name='wash',       # type of item
        typeof='cube',     # cube or cylinder
        WHD=(85, 60, 60),  # (width , height , depth)
        weight=10,         # item weight
        level=1,           # priority (Item need to pack)
        loadbear=100,      # item bearing
        updown=True,       # item fall down or not
        color='#FFFF37'    # set item color , you also can use color='red' or color='r'
    )
```
Init packer : 
```
packer = Packer()          # packer init
```
Add bin and items to packer : (Warning : You can only add one bin,but you can add many items.)
```
packer.addBin(box1)       # adding bins to packer
packer.addItem(item1)     # adding items to packer
```
Start pack items : 
```
packer.pack(
    bigger_first=True,                 # bigger item first
    fix_point=True,                    # fix item float problem
    binding=[('server','cabint')],     # make a set of items
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
packer.addBin(box)

#  add item
packer.addItem(Item('test1', 'test','cube',(9, 8, 7), 1, 1, 100, True,'red'))
packer.addItem(Item('test2', 'test','cube',(4, 25, 1), 1, 1, 100, True,'blue'))
packer.addItem(Item('test3', 'test','cube',(2, 13, 5), 1, 1, 100, True,'gray'))
packer.addItem(Item('test4', 'test','cube',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test5', 'test','cube',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test6', 'test','cube',(6, 5, 2), 1, 1, 100, True,'purple'))
packer.addItem(Item('test7', 'test','cube',(5, 2, 9), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test8', 'test','cube',(10, 8, 5), 1, 1, 100, True,'pink'))
packer.addItem(Item('test9', 'test','cube',(1, 3, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test10', 'test','cube',(8, 4, 7), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test11', 'test','cube',(2, 5, 3), 1, 1, 100, True,'olive'))
packer.addItem(Item('test12', 'test','cube',(1, 9, 2), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test13', 'test','cube',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test14', 'test','cube',(10, 2, 1), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test15', 'test','cube',(3, 2, 4), 1, 1, 100, True,'purple'))
packer.addItem(Item('test16', 'test','cube',(5, 7, 8), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test17', 'test','cube',(4, 8, 3), 1, 1, 100, True,'white'))
packer.addItem(Item('test18', 'test','cube',(2, 11, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test19', 'test','cube',(8, 3, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test20', 'test','cube',(7, 4, 5), 1, 1, 100, True,'olive'))
packer.addItem(Item('test21', 'test','cube',(2, 4, 11), 1, 1, 100, True,'darkgreen'))
packer.addItem(Item('test22', 'test','cube',(1, 3, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test23', 'test','cube',(10, 5, 2), 1, 1, 100, True,'lawngreen'))
packer.addItem(Item('test24', 'test','cube',(7, 4, 5), 1, 1, 100, True,'purple'))
packer.addItem(Item('test25', 'test','cube',(2, 10, 3), 1, 1, 100, True,'yellow'))
packer.addItem(Item('test26', 'test','cube',(3, 8, 1), 1, 1, 100, True,'pink'))
packer.addItem(Item('test27', 'test','cube',(7, 2, 5), 1, 1, 100, True,'brown'))
packer.addItem(Item('test28', 'test','cube',(8, 9, 5), 1, 1, 100, True,'cyan'))
packer.addItem(Item('test29', 'test','cube',(4, 5, 10), 1, 1, 100, True,'olive'))
packer.addItem(Item('test30', 'test','cube',(10, 10, 2), 1, 1, 100, True,'darkgreen'))

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
painter.plotBoxAndItems()

```

## Reference

* [Optimizing three-dimensional bin packing through simulation](https://github.com/jerry800416/3dbinpacking/blob/master/reference/OPTIMIZING%20THREE-DIMENSIONAL%20BIN%20PACKING%20THROUGH%20SIMULATION.pdf)
* https://github.com/enzoruiz/3dbinpacking
* https://github.com/nmingotti/3dbinpacking


## License

[MIT](https://github.com/jerry800416/3dbinpacking/blob/master/LICENSE)