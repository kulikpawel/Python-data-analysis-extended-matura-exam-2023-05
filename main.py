"""
Extended Matura exam in computer science in Poland, May 2023
The fruits.txt file contains information about fruit deliveries to the processing plant in the period from
01/05/2020 to 30/09/2020.
Each line contains: delivery date (dd.mm.yyyy), number of kilograms delivered
raspberries, number of kilograms of strawberries delivered and number of kilograms delivered
currants, separated by a tab character.
Deliveries were made every day during the mentioned period.
Example
date        raspberry_delivery strawberry_delivery currant_delivery
01.05.2020          211             281                 88
02.05.2020          393             313                 83
03.05.2020          389             315                 104
04.05.2020          308             221                 119
Using available IT tools, provide answers to the following questions
tasks.

Exercise 1.1
For each month of the processing plant's operation (May to September), prepare a summary of the numbers
kilograms of raspberries delivered, the number of kilograms of strawberries delivered and the number
delivered kilograms of currants.
Create a column chart based on the prepared list. Remember to make it legible
description of the chart (title, legend, axis descriptions: on the X axis - names of months, on the Y axis - number
kilograms).

Exercise 1.2
Determine the number of days on which the most of the three types of fruit were delivered currants.

Information for tasks 1.3 and 1.4
The processing plant produces jams: raspberry-strawberry, raspberry-currant and strawberry-currant
(always in a 1:1 fruit ratio and using maximum amount of fruit available). Deciding what jam there
will be on a given day produced depends on the amount of fruit in the processing plant.
Fruits are delivered to the processing plant in the morning, before production begins. Of the day only one
type of jam is produced. The fruits that are available are used for production most in the processing
plant (for the data in the fruits.txt file there is no case when quantity different fruits is the same).
Fruit not used for production is stored in cold storage until the next day. The next day a decision
is made about production for this one day based on the total amount of fruit remaining from the
previous day and delivered in the morning.

Example:
If 211 kg of raspberries, 281 kg of strawberries and 88 kg of currants were delivered on May 1, 2020, then in this
On this day, raspberry and strawberry jam will be produced. Used for production there will be 211 kg of raspberries
and 211 kg of strawberries. The rest of the strawberries and all the currants will be there stored in cold storage
until the next day.
After delivery on May 2, 2020 (393 kg of raspberries, 313 kg of strawberries and 83 kg of currants) in the processing plant
there will be 393 kg of raspberries, 383 kg of strawberries and 171 kg of currants, which means it will be produced again
raspberry-strawberry jam.
After taking into account the production cycle described above and the data saved in the file fruits.txt provide answers
to the following tasks.

Exercise 1.3
Specify how many times jam was produced in the period from May 1, 2020 to September 30, 2020 particular types.

Exercise 1.4

To produce 1 kg of two-fruit jam, you need 1 kg of each fruit.
Specify how many kilograms of jam of each type were produced in the period from May 1, 2020 to
30/09/2020.

Exercise 1.5
Determine the length of the longest sequence of consecutive days in which raspberry supplies increased, i.e.
On each subsequent day, more kilograms of raspberries were delivered than on the previous day. Pass it
the date when this sequence started and the date when it ended.
Example:
For raspberry supplies (in kg): 287, 287, 298, 429, 417, 384,
the longest sequence of days in which deliveries increased is 3.

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("Data/fruits.txt", sep = "\t")

new_date = []
for x in df["date"]:
    d = x.split(".")
    new_date.append(d[2] + "-" + d[1] + "-" + d[0])
deliveries = {"raspberries": [0, 0, 0, 0, 0], "strawberries": [0, 0, 0, 0, 0], "currants": [0, 0, 0, 0, 0]}
for i in range(len(df)):
    d = df.iloc[i]["date"].split(".")
    deliveries["raspberries"][int(d[1]) - 5] += df.iloc[i]["raspberry_delivery"]
    deliveries["strawberries"][int(d[1]) - 5] += df.iloc[i]["strawberry_delivery"]
    deliveries["currants"][int(d[1]) - 5] += df.iloc[i]["currant_delivery"]
print("Exercise 1.1")
print(" "*22, "05   ", "06    ", "07   ", "08    ", "09   ")
print("Raspberry delivery  : ", deliveries["raspberries"])
print("Strawberry delivery : ", deliveries["strawberries"])
print("Currant delivery    : ", deliveries["currants"])
#bar width
barWidth = 0.2
fig = plt.subplots(figsize=(12, 8))
#Position of the bar on the X axis
br1 = np.arange(len(deliveries["raspberries"]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
plt.bar(br1,deliveries["raspberries"], color="r", width=barWidth, edgecolor="gray", label="Raspberries")
plt.bar(br2,deliveries["strawberries"], color="g", width=barWidth, edgecolor="gray", label="Strawberries")
plt.bar(br3,deliveries["currants"], color="b", width=barWidth, edgecolor="gray", label="Currants")
plt.xlabel("Months", fontweight="bold", fontsize=15)
plt.ylabel("Number of kilograms delivered", fontweight="bold", fontsize=15)
plt.xticks([r + barWidth for r in range(len(deliveries["raspberries"]))],
            ['May', 'June', 'July', 'August', 'September'])
plt.title("List of fruit deliveries from May to September in 2020", fontweight="bold", fontsize=20)
plt.legend()
plt.show()
stock_state = {"raspberries": [], "strawberries": [], "currants": []}
max_currants = 0
for i in range(len(df)):
    if df.iloc[i]["raspberry_delivery"] < df.iloc[i]["currant_delivery"] and df.iloc[i]["strawberry_delivery"] < df.iloc[i]["currant_delivery"]:
        max_currants += 1
print("1.2. Number of days in which, of the three types of fruit, the most currants were delivered: ", max_currants)
production = {"ras_str": [], "ras_cur": [], "str_cur": []}
stock_state["raspberries"].append(df.iloc[0]["raspberry_delivery"])
stock_state["currants"].append(df.iloc[0]["currant_delivery"])
stock_state["strawberries"].append(df.iloc[0]["strawberry_delivery"])
for i in range(len(df)):
    #least raspberries, currant and strawberry jam
    if stock_state["raspberries"][i] < stock_state["currants"][i] and stock_state["raspberries"][i] < stock_state["strawberries"][i]:
        production["ras_str"].append(0)
        production["ras_cur"].append(0)
        minimum = min(stock_state["strawberries"][i], stock_state["currants"][i])
        production["str_cur"].append(minimum)
        if i < len(df) - 1:  #storing fruit for the next day
            stock_state["raspberries"].append(df.iloc[i + 1]["raspberry_delivery"] + stock_state["raspberries"][i])
            stock_state["currants"].append(df.iloc[i + 1]["currant_delivery"] - minimum + stock_state["currants"][i])
            stock_state["strawberries"].append(df.iloc[i + 1]["strawberry_delivery"] - minimum + stock_state["strawberries"][i])
    #least strawberries, raspberry and currant jam
    if stock_state["strawberries"][i] < stock_state["currants"][i] and stock_state["strawberries"][i] < stock_state["raspberries"][i]:
        production["str_cur"].append(0)
        production["ras_str"].append(0)
        minimum = min(stock_state["raspberries"][i], stock_state["currants"][i])
        production["ras_cur"].append(minimum)
        if i < len(df) - 1:  #storing fruit for the next day
            stock_state["strawberries"].append(df.iloc[i + 1]["strawberry_delivery"] + stock_state["strawberries"][i])
            stock_state["raspberries"].append(df.iloc[i + 1]["raspberry_delivery"] - minimum + stock_state["raspberries"][i])
            stock_state["currants"].append(df.iloc[i + 1]["currant_delivery"] - minimum + stock_state["currants"][i])
    # least currants, raspberry and strawberry jam
    if stock_state["currants"][i] < stock_state["raspberries"][i] and stock_state["currants"][i] < stock_state["strawberries"][i]:
        production["str_cur"].append(0)
        production["ras_cur"].append(0)
        minimum = min(stock_state["raspberries"][i], stock_state["strawberries"][i])
        production["ras_str"].append(minimum)
        if i < len(df) - 1:  #storing fruit for the next day
            stock_state["currants"].append(df.iloc[i + 1]["currant_delivery"] + stock_state["currants"][i])
            stock_state["raspberries"].append(df.iloc[i + 1]["raspberry_delivery"] - minimum + stock_state["raspberries"][i])
            stock_state["strawberries"].append(df.iloc[i + 1]["strawberry_delivery"] - minimum + stock_state["strawberries"][i])
str_cur = 0
sum_str_cur = 0
for i in production["str_cur"]:
    if i>0:
        str_cur += 1
        sum_str_cur += i
ras_str = 0
sum_ras_str = 0
for i in production["ras_str"]:
    if i>0:
        ras_str += 1
        sum_ras_str += i
ras_cur = 0
sum_ras_cur = 0
for i in production["ras_cur"]:
    if i>0:
        ras_cur += 1
        sum_ras_cur += i
print("Exercise 1.3")
print("Strawberry and currant jam was produced   : ", str_cur, "times.")
print("Raspberry and strawberry jam was produced : ", ras_str, "times.")
print("Raspberry and currant jam was produced    : ", ras_cur, "times.")
print("Exercise 1.4")
print("Quantity produced strawberry and currant jam   : ", sum_str_cur)
print("Quantity produced raspberry and currant jam    : ", sum_ras_cur)
print("Quantity produced raspberry and strawberry jam : ", sum_ras_str)

print("Exercise 1.5 - Old high school exam (5.3)")
max_len = 1
beginning = 0
l = 1
p = 0
for i in range(1, len(df)):
    if df.iloc[i]["raspberry_delivery"] > df.iloc[i - 1]["raspberry_delivery"]:
        l += 1
        if l > max_len:
            max_len = l
            beginning = p
    else:
        p = i
        l = 1
print("""The longest string of consecutive days in which the raspberry deliveries grew begins """, df.iloc[beginning]["date"], " and lasts until ", df.iloc[beginning + max_len - 1]["date"], "(", max_len, " days ).")








