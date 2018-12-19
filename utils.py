import requests
import pandas as pd
from stringMatch import string_match

def get_beer_rec(beer_i_liked):
    beer_df = pd.read_json("https://storage.googleapis.com/beer_recommendations/beer_recommendations.json", lines=True)
    dist_list = [string_match(beer_i_liked, beer) for beer in beer_df["beer"].unique()]
    beer_match = max(enumerate(dist_list),key=lambda item:item[1])[0]
    question = beer_df["beer"][beer_match]
#     answers = [x["rec_beer"] for x in beer_df["recs"][beer_match]]
#     beer_links = [x["link"] for x in beer_df["recs"][beer_match]]
    beers_and_links = list(zip([x["rec_beer"] for x in beer_df["recs"][beer_match]],
                               [x["link"] for x in beer_df["recs"][beer_match]]))
    bot_response = ", ".join(['<a href="{link}">{beer_name}</a>'.format(beer_name=x[0], link="https://beeradvocate.com"+x[1]) for x in beers_and_links])
    return "The recommendations for <b>{beer}</b> are the following: {beer_recommendations}".format(beer=question,
                                                                                            beer_recommendations=bot_response)

def get_crypto_price(coin):
    r = requests.get("https://poloniex.com/public?command=returnTicker").json()
    return str(round(float(r.get("USDT_{coin}".format(coin=coin.upper())).get("last")),2))
