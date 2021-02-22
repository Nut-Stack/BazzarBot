#Created by Nut-Stack

import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style, axis
import pyttsx3
import threading

plt.style.use("dark_background")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', .8)
engine.setProperty('rate', 250)

fig = plt.figure()

ax1 = fig.add_subplot(2,3,1)
ax2 = fig.add_subplot(2,3,2)
ax3 = fig.add_subplot(2,3,3)
ax4 = fig.add_subplot(2,3,4)
ax5 = fig.add_subplot(2,3,5)
ax6 = fig.add_subplot(2,3,6)

item = input("What item?")
item_title = item.replace("_"," ")
item_list = item_title.split(" ")
for i in range(len(item_list)):
    item_list[i] = item_list[i].capitalize()
item_title = " ".join(item_list)
fig.canvas.set_window_title(item_title)

selll = []
buyy = []
marginn = []
buy_orderss = []
sell_orderss = []
ys = []
def text_to_speech(BUY,SELL,MARGIN):
    while True:
        if len(BUY) > 2:
            if BUY[-1] > BUY[-2]:
                engine.say("Buy increase {}".format(abs(round(BUY[-2]-BUY[-1],1))))
        if len(BUY) > 2:
            if BUY[-1] < BUY[-2]:
                engine.say("Buy decrease {}".format(abs(round(BUY[-2]-BUY[-1],1))))
        if len(SELL) > 2:
            if SELL[-1] > SELL[-2]:
                engine.say("Sell increase {}".format(abs(round(SELL[-2]-SELL[-1],1))))
        if len(SELL) > 2:
            if SELL[-1] < SELL[-2]:
                engine.say("Sell decrease {}".format(abs(round(SELL[-2]-SELL[-1],1))))
        if len(MARGIN) > 2:
            if MARGIN[-1] <.011:
                engine.say("Margin is lower than 1!")
        engine.runAndWait()


def animate(i):
    data = requests.get("https://api.hypixel.net/skyblock/bazaar?key=#####&name=#######").json()
    products = (data["products"])
    buy_summary = (products.get(item).get("buy_summary"))
    sell_price = buy_summary[0].get('pricePerUnit')
    orders_buy = buy_summary[0].get('orders')
    amount_buy = buy_summary[0].get('amount')

    sell_summary = (products.get(item).get("sell_summary"))
    buy_price = sell_summary[0].get('pricePerUnit')
    orders_sell = sell_summary[0].get('orders')
    amount_sell = sell_summary[0].get('amount')

    difference = (sell_price - buy_price)/(buy_price)
    selll.append(sell_price)
    buyy.append(buy_price)
    marginn.append(difference)
    buy_orderss.append(amount_buy)
    sell_orderss.append(amount_sell)

    ys.append(i)

    if len(ys) > 300:
        ys.remove(ys[0])
        selll.remove(selll[0])
        buyy.remove(buyy[0])
        marginn.remove(marginn[0])
        buy_orderss.remove(buy_orderss[0])
        sell_orderss.remove(sell_orderss[0])

    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()

    ax1.set_title("Selling Price")
    ax2.set_title("Buying Price")
    ax3.set_title("Margin")
    ax4.set_title("Orders Sell")
    ax5.set_title("Orders Buy")
    ax6.set_title("Buy & Sell")

    ax1.plot(ys, selll, color = 'r', label = sell_price)
    ax2.plot(ys, buyy, color = 'g', label = buy_price)
    ax3.plot(ys, marginn, color = "b", label = difference)
    ax4.plot(ys, buy_orderss, color = "r", label = amount_buy)
    ax5.plot(ys, sell_orderss, color = "g", label = amount_sell)
    ax6.plot(ys, selll, color = 'r', label = sell_price)
    ax6.plot(ys, buyy, color = 'g', label = buy_price)

    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper left")
    ax3.legend(loc = "upper left")
    ax4.legend(loc = "upper left")
    ax5.legend(loc = "upper left")
    ax6.legend(loc = "upper left")

T = threading.Thread(target = text_to_speech, args = (buyy,selll,marginn))
T.daemon = False
T.start()

ani = animation.FuncAnimation(fig,animate,interval=800)
plt.show()

