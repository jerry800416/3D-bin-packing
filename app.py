from py3dbp import Packer, Bin, Item, Painter
import streamlit as st
import matplotlib.pyplot as plt
import random
import csv

st.set_page_config(page_title="Streamlit App", page_icon=":smiley:")

uploaded_file = st.file_uploader("Choose a file")


COLORS = ["yellow", "olive", "pink", "brown", "red",
          "blue", "green", "purple", "orange", "gray"]
# Initialize variables to store bins and items
bins = []
bin_size = -1
items = []
item_size = 0
counter = 0

if uploaded_file is not None:
    # Use uploaded file content instead of hardcoded path
    uploaded_data = uploaded_file.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(uploaded_data)
    # Iterate through the rows and parse bins and items
    for row in csv_reader:
        # Check if the row is empty
        if not any(row):
            continue

        # If there is a single number in the row, it represents the number of bins or items
        if row[1] == "":
            num = int(row[0].strip('\ufeff'))
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

    # calculate packing
    packer.pack(
        bigger_first=True,
        distribute_items=True,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=0
    )

    # put order
    packer.putOrder()

    output = "***************************************************\n"
    for idx, b in enumerate(packer.bins):
        output += f"** {b.string()} **\n"
        output += "***************************************************\n"
        output += "FITTED ITEMS:\n"
        output += "***************************************************\n"
        volume = b.width * b.height * b.depth
        volume_t = 0
        volume_f = 0
        unfitted_name = ''
        for item in b.items:
            output += f"partno : {item.partno}\n"
            output += f"position : {item.position}\n"
            output += f"W*H*D : {item.width} * {item.height} * {item.depth}\n"
            output += f"volume : {float(item.width) * float(item.height) * float(item.depth)}\n"
            volume_t += float(item.width) * \
                float(item.height) * float(item.depth)
            output += "***************************************************\n"

        output += f'space utilization : {round(volume_t / float(volume) * 100, 2)}%\n'
        output += f'residual volume : {float(volume) - volume_t}\n'
        output += "***************************************************\n"
        # draw results
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.8,
            write_num=False,
            fontsize=10
        )

    output += "***************************************************\n"
    output += "UNFITTED ITEMS:\n"
    for item in packer.unfit_items:
        output += "***************************************************\n"
        output += f"partno : {item.partno}\n"
        output += f"W*H*D : {item.width} * {item.height} * {item.depth}\n"
        output += f"volume : {float(item.width) * float(item.height) * float(item.depth)}\n"
        volume_f += float(item.width) * \
            float(item.height) * float(item.depth)
        unfitted_name += f'{item.partno},'
        output += "***************************************************\n"
    output += "***************************************************\n"
    output += f'unpacked items : {unfitted_name}\n'
    output += f'unpacked items volume : {volume_f}\n'

    # Print the entire output
    print(output)

    st.title("Streamlit App")
    st.pyplot(fig)
