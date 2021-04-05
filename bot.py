import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style, axis
import pyttsx3
import threading

item = input("What item?")
plt.style.use("dark_background")



fig = plt.figure()

ax1 = fig.add_subplot(3,3,1)
ax2 = fig.add_subplot(3,3,2)
ax3 = fig.add_subplot(3,3,3)
ax4 = fig.add_subplot(3,3,4)
ax5 = fig.add_subplot(3,3,5)
ax6 = fig.add_subplot(3,3,6)
ax7 = fig.add_subplot(3,3,7)
ax8 = fig.add_subplot(3,3,8)
ax9 = fig.add_subplot(3,3,9)

item = item.upper()
item = item.replace(" ","_")

item_title = item.replace("_"," ")
item_list = item_title.split(" ")
for i in range(len(item_list)):
    item_list[i] = item_list[i].capitalize()
item_title = " ".join(item_list)
fig.canvas.set_window_title(item_title)

selll = []
buyy = []
marginn = []
acutal_profits = []
buy_orderss = []
sell_orderss = []
num_of_people_ask = []
num_of_people_bid = []
ys = []

tax_rate = 0.022

def text_to_speech(BUY,SELL,MARGIN):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('volume', .8)
    engine.setProperty('rate', 250)

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
            if MARGIN[-1] < 0:
                engine.say("Margin is negative")
        engine.runAndWait()



def animate(i):
    data = requests.get("https://api.hypixel.net/skyblock/bazaar?key=###USEYOUROWNKEYNERD###&name=###USEYOUROWNNAMENERD###").json()
    products = (data["products"])
    buy_summary = (products.get(item).get("buy_summary"))
    ask = buy_summary[0].get('pricePerUnit')
    orders_buy = buy_summary[0].get('orders')
    amount_buy = buy_summary[0].get('amount')

    sell_summary = (products.get(item).get("sell_summary"))
    bid = sell_summary[0].get('pricePerUnit')
    orders_sell = sell_summary[0].get('orders')
    amount_sell = sell_summary[0].get('amount')

    difference = round(((ask - (ask * tax_rate)) - bid)/(bid), 4)
    acutal_profit = round(ask - (ask * tax_rate) - bid, 1)
    selll.append(ask)
    buyy.append(bid)
    marginn.append(difference)
    acutal_profits.append(acutal_profit)
    num_of_people_bid.append(orders_buy)
    num_of_people_ask.append(orders_sell)
    buy_orderss.append(amount_buy)
    sell_orderss.append(amount_sell)

    ys.append(i)

    if len(ys) > 400:
        ys.remove(ys[0])
        selll.remove(selll[0])
        buyy.remove(buyy[0])
        marginn.remove(marginn[0])
        buy_orderss.remove(buy_orderss[0])
        sell_orderss.remove(sell_orderss[0])
        num_of_people_ask.remove(num_of_people_ask[0])
        num_of_people_bid.remove(num_of_people_bid[0])
        acutal_profits.remove(acutal_profits[0])

    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()
    ax7.clear()
    ax8.clear()
    ax9.clear()

    ax1.set_title("Bid")
    ax2.set_title("Ask")
    ax3.set_title("Bid Ask Spread")
    ax4.set_title("Bid on Top")
    ax5.set_title("Ask on Bottom")
    ax6.set_title("Margin %")
    ax7.set_title("Num of People Bid")
    ax8.set_title("Num of People Ask")
    ax9.set_title("Profit per One Flip")

    ax1.plot(ys, buyy, color = 'g', label = bid)
    ax2.plot(ys, selll, color = 'r', label = ask)
    ax3.plot(ys, selll, color = 'r', label = ask)
    ax3.plot(ys, buyy, color = 'g', label = bid)
    ax4.plot(ys, sell_orderss, color = "g", label = amount_sell)
    ax5.plot(ys, buy_orderss, color = "r", label = amount_buy)
    ax6.plot(ys, marginn, color = "b", label = difference)
    ax7.plot(ys, num_of_people_ask, color = 'g', label = orders_sell)
    ax8.plot(ys, num_of_people_bid, color = 'r', label = orders_buy)
    ax9.plot(ys, acutal_profits, color = 'b', label = acutal_profit)


    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper left")
    ax3.legend(loc = "upper left")
    ax4.legend(loc = "upper left")
    ax5.legend(loc = "upper left")
    ax6.legend(loc = "upper left")
    ax7.legend(loc = "upper left")
    ax8.legend(loc = "upper left")
    ax9.legend(loc = "upper left")
T = threading.Thread(target = text_to_speech, args = (buyy,selll,marginn))
T.daemon = False
T.start()

ani = animation.FuncAnimation(fig,animate,interval=700)
plt.show()

