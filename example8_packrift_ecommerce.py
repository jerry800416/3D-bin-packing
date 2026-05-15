from py3dbp import Packer, Bin, Item


"""
Packrift ecommerce cartonization example.

The carton and order dimensions below are a compact static copy of the public
Packrift cartonization solver fixtures:
https://packrift.github.io/packaging-optimization-benchmark-corpus/cartonization-solver-fixtures.html

Units are inches and pounds. The example intentionally avoids network access so
it can run the same way as the other examples in this repository.
"""


def add_packrift_cartons(packer):
    # 24x10x8 Packrift long corrugated carton, SKU 24108.
    packer.addBin(Bin(partno="Packrift-24108", WHD=(24, 10, 8), max_weight=70))
    # 40x20x20 Packrift bulk shipping carton, SKU 402020.
    packer.addBin(Bin(partno="Packrift-402020", WHD=(40, 20, 20), max_weight=120))


def add_demo_order(packer):
    order_lines = [
        ("demo-small", (7.5, 4.5, 3.5), 1),
        ("demo-flat", (15.0, 7.0, 2.5), 2),
        ("demo-long", (21.0, 8.5, 5.0), 1),
    ]
    colors = ["red", "blue", "green", "orange"]
    item_number = 1
    for sku, whd, quantity in order_lines:
        for copy_number in range(quantity):
            packer.addItem(Item(
                partno=f"{sku}-{copy_number + 1}",
                name=sku,
                typeof="cube",
                WHD=whd,
                weight=1,
                level=item_number,
                loadbear=100,
                updown=True,
                color=colors[(item_number - 1) % len(colors)]))
            item_number += 1


def main():
    packer = Packer()
    add_packrift_cartons(packer)
    add_demo_order(packer)

    packer.pack(
        bigger_first=False,
        distribute_items=True,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=2)

    print("Packrift ecommerce cartonization example")
    print("Source: Packrift public solver fixtures")
    print(f"Packed bins: {len([box for box in packer.bins if box.items])}")
    print(f"Unfit items: {len(packer.unfit_items)}")

    for box in packer.bins:
        used_volume = sum(float(item.getVolume()) for item in box.items)
        utilization = used_volume / float(box.getVolume()) * 100
        print(f"\n{box.partno}: {len(box.items)} items, {utilization:.1f}% volume utilization")
        for item in box.items:
            print(
                f"  - {item.partno} {item.width}x{item.height}x{item.depth}"
                f" at {item.position}")


if __name__ == "__main__":
    main()
