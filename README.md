3D Bin Packing
====

3D Bin Packing improvements based on [this repository](https://github.com/enzoruiz/3dbinpacking). 

<img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/3.jpeg" width="600"/>

## OutLine
- [3D Bin Packing](#3d-bin-packing)
  - [OutLine](#outline)
  - [Improvement](#improvement)
  - [How to use](#how-to-use)
  - [Example](#example)
      - [Simple example](#simple-example)
      - [example0](#example0)
      - [example1](#example1)
      - [example2](#example2)
      - [example3](#example3)
      - [example4](#example4)
      - [example5](#example5)
      - [example6](#example6)
      - [example7](#example7)
  - [Issue](#issue)
  - [Bug](#bug)
  - [History](#history)
  - [Reference](#reference)
  - [License](#license)



## Improvement
1. **fix item float :**
    * `[fix_point = False/True] type bool` The original packaging method did not consider the gravity problem. After the packaging was completed, there were items floating in the air, which greatly reduced the space utilization of the box. I solved this problem and improved the boxing rate.

    Original packaging  |  Used fix point
    :-------------------------:|:-------------------------:
    <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/1.jpg" width="400"/>  |  <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/2.jpg" width="400"/>

2. **Item bearing problem :**
    * `[loadbear = X] type int` The original method did not consider the problem of project load-bearing, because load-bearing involves the structure, I used the priority to sort the projects with higher load-bearing capacity.The higher the number, the higher the priority.

3. **Item need to pack :**
    * `[level = X] type int` The priority can be set to sort which items should be packaged first, to ensure that these items will be packaged in bin.The lower the number, the higher the priority.

4. **Items can be placed upside down or not :**
    * `[updown = False/True] type bool` True means the item can be placed upside down.

5. **Make a set of items :** 
    * `[binding = [(orange,apple),(computer,hat,watch)]] type tuple in list` The number of items in the set must be the same in the bin.
    * eg. `binding = [(orange,apple),(computer,hat,watch)]`.

6. **Container coner :**
    * `[corner = X] type int` Set the size of container corner, the unit is cm, color is black.

    <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/7.jpeg" width="600"/>

7. **Paint picture :** 
    * `[painter.plotBoxAndItems()]` Draw pictures.

8. **Calculate gravity distribution :**
    * `print("gravity distribution : ",bin.gravity) ` Divide the bin into four equal parts, and calculate the weight ratio of the equal parts. Ideally, the weight ratio of each equal part tends to be close.

9. **Add the order of placing items :**
    * `put_type = 0 or 1 (0 : general & 1 : open top)` Added the order of placing items. There are two placement methods. Set the bin to open top or general, and the returned results are sorted according to this method.

10. **Mixed cube and cylinder :** 
    * `typeof = cube or cylinder`  mixed with cube and cylinder .

    <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/4.jpeg" width="600"/>

11. **Check stability on item :**
    * If you want to use this function,`fix_point = True` and `check_stable=True` and `0 < support_surface_ratio <= 1 `.
    * Rule :
      1. Define a support ratio(support_surface_ratio), if the ratio below the support surface does not exceed this ratio, compare the next rule.
      2. If there is no support under any of the bottom four vertices of the item, then remove the item.

    ! check stable  |  check stable
    :-------------------------:|:-------------------------:
    <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/5.JPG" width="400"/>  |  <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/6.JPG" width="400"/>

12. **distribute items :**
    * If you have multiple boxes, you can change distribute_items to achieve different packaging purposes.
    * Rule :
      1. distribute_items=True , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full or all the items are packed.
      2. distribute_items=False, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.
    
    img |  distribute_items | ! distribute_items
    :-------------------------:|:-------------------------:|:-------------------------:
    Bin1 | <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/8.JPG" width="400"/>  |  <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/8.JPG" width="400"/> 
    Bin2 | <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/9.JPG" width="400"/>  |  <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/10.JPG" width="400"/> 

13. **Write part number on item :**
    * Check **Painting** in [how to use](#how-to-use).
    * In order to better distinguish each item, I write part no in the middle of the item, but if I do this, it will be blocked by the color, so it is best to set the alpha value to about 0.2.

    <img src="https://github.com/jerry800416/3dbinpacking/blob/master/img/11.jpeg" width="600"/>

## How to use

**Init bin :** 
```python
box1 = Bin(
    partno='Bin',         # partno / PN of item (unique value)
    WHD=(589,243,259),    # (width , height , depth)
    max_weight=28080,     # box can bear the weight
    corner=15             # container coner
    put_type= 1           # add the order of placing items
)
```

**Init item :** 
```python
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

**Init packer :**
```python
packer = Packer()          # packer init
```

**Add bin and items to packer : ~~(Warning : You can only add one bin,but you can add many items.)~~ Now you can add multiple bins/boxes,plz check example7.**
```python
packer.addBin(box1)       # adding bins to packer
packer.addItem(item1)     # adding items to packer
```

**Start pack items :** 
```python
packer.pack(
    bigger_first=True,                 # bigger item first.
    fix_point=True,                    # fix item float problem.
    binding=[('server','cabint')],     # make a set of items.
    distribute_items=True,             # If multiple bin, to distribute or not.
    check_stable=True,                 # check stability on item.
    support_surface_ratio=0.75,        # set support surface ratio.
    number_of_decimals=0
)
```

**Results :**
```python
packer.bins              # get bin of packer
packer.bin[i].items      # get fitted items in bin
packer.unfit_items       # get unfitted items 
```

**Painting :**
```python
for b in packer :
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.2,         # set item alpha
        write_num=True,    # open/close write part number 
        fontsize=10        # control write_num fontsize
    )
fig.show() 
```

## Example

#### Simple example
```python
from py3dbp import Packer, Bin, Item
import time

start = time.time()

# init packing function
packer = Packer()

#  init bin
box = Bin('example',(30, 10, 15), 99,0)
packer.addBin(box)

#  add item
packer.addItem(Item('test1', 'test','cube',(9, 8, 7), 1, 1, 100, True,'red'))
packer.addItem(Item('test2', 'test','cube',(4, 25, 1), 1, 1, 100, True,'blue'))
packer.addItem(Item('test3', 'test','cube',(2, 13, 5), 1, 1, 100, True,'gray'))
packer.addItem(Item('test4', 'test','cube',(7, 5, 4), 1, 1, 100, True,'orange'))
packer.addItem(Item('test5', 'test','cube',(10, 5, 2), 1, 1, 100, True,'lawngreen'))

# calculate packing 
packer.pack(
    bigger_first=True,
    fix_point=True,
    distribute_items=True,
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# paint the results
for b in packer :
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.2,         
        write_num=True,   
        fontsize=10        
    )
fig.show()
```
#### example0
* This example can be used to compare the `fix_point` function with and without the `fix_point` function.

#### example1
* This example is used to demonstrate the mixed packing of cube and cylinder.

#### example2
* This case is used to demonstrate an example of a packing complex situation.

#### example3
* This example is used to demonstrate that the algorithm does not optimize.

#### example4
* This example can be used to test large batch calculation time and binding functions.

#### example5
* Check stability on item - first rule
* Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule.

#### example6
* Check stability on item - second rule
* If there is no support under any of the bottom four vertices of the item, then remove the item.

#### example7
* If you have multiple boxes, you can change `distribute_items` to achieve different packaging purposes.
* `distribute_items=True` , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full  or all the items are packed.
* `distribute_items=False`, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.


## Issue
* Optimizing using GA or PSO...


## Bug
* Make set of items funcn crash.


## History 

* 20230621 Add a rule to check item stability.
* 20230621 Fix issue : there can only creat one bin.
* 20230628 Modify `Readme.md`.
* 20230629 Fix issue : can not write anything on cube.

## Reference

* [Optimizing three-dimensional bin packing through simulation](https://github.com/jerry800416/3dbinpacking/blob/master/reference/OPTIMIZING%20THREE-DIMENSIONAL%20BIN%20PACKING%20THROUGH%20SIMULATION.pdf)
* https://github.com/enzoruiz/3dbinpacking
* https://github.com/nmingotti/3dbinpacking


## License

[MIT](https://github.com/jerry800416/3dbinpacking/blob/master/LICENSE)