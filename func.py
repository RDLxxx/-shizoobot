import requests
import time
import hmac
import hashlib
from bs4 import BeautifulSoup

def generate_signature(secret_key, message):
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()


def analyze():
    API_KEY = 'apibitget' # huiget
    SECRET_KEY = 'apibitget' # huiget
    PASSPHRASE = 'apibitget' # huiget


    urlalt = "https://blockchaincenter.net/altcoin-season-index/" # Parsing Blyat
    response = requests.get(urlalt)
    soup = BeautifulSoup(response.text, 'html.parser')

    index_element = soup.find("div", style=lambda value: value and "font-size:88px" in value and "color:#345C99" in value)
    index_value_alt = index_element.text if index_element else "N/A"

    timestamp = str(int(time.time() * 1000))
    message = timestamp + "GET" + "/api/mix/v1/market/ratio" + "?symbol=BTCUSDT_UMCBL&period=1H"
    signature = generate_signature(SECRET_KEY, message)

    hb = {
        "Content-Type": "application/json",
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE
    }
    url_fng = "https://api.alternative.me/fng/" # free api
    fngresponse = requests.get(url_fng)
    fng = fngresponse.json()
    index_value_fng = fng["data"][0]["value"]

    urlgecko = "https://api.coingecko.com/api/v3/global" # free api
    gresponse = requests.get(urlgecko)
    gecko = gresponse.json()
    btc_dominance = gecko["data"]["market_cap_percentage"]["btc"]
    total_market_cap = gecko["data"]["total_market_cap"]["usd"]

    url = "https://api.bitget.com/api/spot/v1/market/ticker"
    pb = {"symbol": "BTCUSDT_SPBL"}
    pe = {"symbol": "ETHUSDT_SPBL"}
    px = {"symbol": "XRPUSDT_SPBL"}

    btc = requests.get(url, headers=hb, params=pb).json()["data"]
    eth = requests.get(url, headers=hb, params=pe).json()["data"]
    xrp = requests.get(url, headers=hb, params=px).json()["data"]

    urlgt = "https://api.geckoterminal.com/api/v2/networks/ton/pools/EQBJNKIIuskkvRxd5EHdfpNTtqbJoJWVbt7NI0WTeQ_2VJE3" # free api
    rgt = requests.get(urlgt)
    dgv = rgt.json()
    govnoprice = dgv['data']['attributes']['base_token_price_usd']

    urlton = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd" # free api
    responseton = requests.get(urlton)
    priceton = responseton.json()["the-open-network"]["usd"]

    result = (f"BTC ~{btc['buyOne']}$\nETH ~{eth['buyOne']}$\nXRP ~{xrp['buyOne']}$\nGOVNO ~{round(float(govnoprice), 3)}$\nTON ~{round(float(priceton), 3)}$\n-----------------------\n"
              f"Индекс страха и жадности — {index_value_fng}\nИндекс альт-сезона — ~{index_value_alt} (+-2%)\n"
              f"Доминация Bitcoin — ~{round(float(btc_dominance), 2)}% (+-2%)\nОбщая рыночная капитализация — ~{total_market_cap:,.2f}$\n"
              f"Минимум BTC за 24h — {btc['low24h']}$, Максимум BTC за 24h {btc['high24h']}$")
    return result