import re
import json
import requests
from bs4 import BeautifulSoup


def search():
    # in steam profile, go to games than copy the link
    url = "https://steamcommunity.com/id/pintipanda/games/?tab=all"

    # add the exceptions (something from the game's store page)
    exceptions = [
        "Rocket League",
        "Assassin's Creed III",
        "no longer available for sale on Steam.",
    ]

    data = requests.get(url).text
    data = re.search(r"var rgGames = (.*]);", data).group(1)
    data = json.loads(data)
    prices = []
    real_prices = []
    counter = 0
    values = 'abcdefghijklmnopqrstuvwxyz">_/'
    
    for d in data:
        print(d["name"])
        game_url = requests.get(
            "https://store.steampowered.com/app/{}/".format(d["appid"])
        ).text
        soup = BeautifulSoup(game_url, "lxml")
        price_div = str(soup.find("div", {"class": "game_purchase_action"}))
        
        # check if the game is free
        if "Free" in price_div:
            print("This is a free game")
            continue
        # check for the exceptions
        if any(exception in str(soup) for exception in exceptions):
            continue
        # get the game's current discounted value if exists
        if str(soup.find("div", {"class": "discount_final_price"})) in str(price_div):
            try:
                discount_div = str(soup.find("div", {"class": "discount_final_price"}))
                x = discount_div.find("TL")
                prices.append(
                    discount_div[x - 7 : x - 1]
                    .replace(" ", "")
                    .translate({ord(i): None for i in values})
                )
                prices_correct = " ".join(prices).replace(",", ".").split()
                print(prices_correct[counter])
                real_prices.append(float(prices_correct[counter]))
                counter += 1
                continue
            except ValueError:
                print("There is a problem. (Invalid Game)")
                counter += 1
                continue
        # get the game's current value if exists
        else:
            try:
                game_price_div = str(
                    soup.find("div", {"class": "game_purchase_price price"})
                )
                x = game_price_div.find("TL")
                prices.append(
                    game_price_div[x - 7 : x - 1]
                    .replace(" ", "")
                    .translate({ord(i): None for i in values})
                )
                prices_correct = " ".join(prices).replace(",", ".").split()
                real_prices.append(float(prices_correct[counter]))
                print(prices_correct[counter])
                counter += 1
                continue
            except ValueError:
                print("There is a problem. (Invalid Game)")
                counter += 1
                continue
    
    # calculate the total of real_prices
    total = 0
    for i in real_prices:
        try:
            total += float(i)
        except ValueError:
            continue
    print(total)


search()
