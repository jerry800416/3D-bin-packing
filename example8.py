from py3dbp import Packer, Bin, Item, Painter

# Creation of the default packer
packer = Packer(packer_id='packer1')

# Creation of bin and items without specifying the packer
bin1 = Bin(WHD=(100, 100, 100), bin_id='bin1')
item1 = Item(WHD=(10, 10, 10), item_id='item1')
item2 = Item(WHD=(20, 20, 20), item_id='item2')

# Adding the bin and items to the packer
packer.addBin(bin1)
packer.addItem(item1)
packer.addItem(item2)

# Executing the packing
packer.pack()

# Example with multiple packers (necessary to specify the packer)

# Creation of the packers
packer1 = Packer(packer_id='packer1')
packer2 = Packer(packer_id='packer2')

# Creation of bin and items specifying the packer
bin1 = Bin(WHD=(100, 100, 100), bin_id='bin1', packer=packer1)
bin2 = Bin(WHD=(200, 200, 200), bin_id='bin2', packer=packer2)

item1 = Item(WHD=(10, 10, 10), item_id='item1', packer=packer1)
item2 = Item(WHD=(20, 20, 20), item_id='item2', packer=packer2)

# Adding the bins and items to their respective packers
packer1.addBin(bin1)
packer1.addItem(item1)

packer2.addBin(bin2)
packer2.addItem(item2)

# Executing the packing for each packer
packer1.pack()
packer2.pack()

# draw results for each packer
for packer in [packer1, packer2]:
    for b in packer.bins:
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.bin_id,
            alpha=0.8,
            write_name=False,
            fontsize=10
        )