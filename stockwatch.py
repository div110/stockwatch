import time
import streamlit as st
import requests
import math
from streamlit_autorefresh import st_autorefresh

st.set_page_config(initial_sidebar_state="collapsed")

    #BUG EVERY ACTION() APPENDS CLONES

asset_counts = {}
asset_worths = {}
asset_prices = {}
assets = []
big_data = []
net_value = 0
def action():
    global asset_counts, asset_worths, asset_prices, assets, big_data, net_value
    with open("assets.csv") as content:
        url = "https://finance.yahoo.com/quote/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0.0.0 Safari/537.36"
        }

        session = requests.Session()
        session.headers.update(headers)
        for line in content:
            line = line.strip("\n")
            assets.append(line.split(';')[0])
            asset_counts[line.split(";")[0]] = float(line.split(";")[1])
            #print(asset_counts)
            #print(assets)
    for ticker in assets:
        print(url+ticker)
        response = session.get(url+ticker)
        if response.status_code != 200:
            continue
        start = response.text.find('yf-ipw1h0">')
        if start==-1:
            continue
        start+=11
        end = response.text.find("<",start)
        value = response.text[start:end].strip()
        value = value.replace(",","")
        value = float(value)

        asset_prices[ticker] = value
        asset_worths[ticker] = asset_counts[ticker] * value
        big_data.append(
            {
                "Symbol": ticker,
                "Price": value,
                "Amount": asset_counts[ticker],
                "Sum": asset_worths[ticker]
            }
        )

    net_value = 0 
    for asset in asset_worths:
        net_value += asset_worths[asset]
    net_value = round(net_value, 2)
    print(net_value)
    
    

st.header("Investments")

st.sidebar.dataframe(big_data)



with st.sidebar.form("NEW Stock"):
    new_stock = st.text_input("Yahoo Finance Symbol")
    new_stock_amount = st.number_input("Amount",step=1)
    add_button = st.form_submit_button("Add")

st.markdown(
    '<h1 style="font-size: 200px;white-space: nowrap;">'+str(net_value)+'</h1>',
    unsafe_allow_html=True
)

while True:
    action()

    print("action ended")
    

    if new_stock not in assets and (new_stock != "" and new_stock_amount >= 0):
        with open("assets.csv", 'a') as content:
            content.write(new_stock+';'+str(new_stock_amount)+'\n')



