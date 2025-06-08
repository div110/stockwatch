

import streamlit as st
import requests

file_name = "assets.csv"
content = open(file_name)
asset_counts = {}
asset_worths = {}
asset_prices = {}
assets = []
big_data = []
url = "https://finance.yahoo.com/quote/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}
for line in content:
    line = line.strip("\n")
    assets.append(line.split(';')[0])
    asset_counts[line.split(";")[0]] = int(line.split(";")[1])
    print(asset_counts)
    print(assets)

for ticker in assets:
    print(url+ticker)
    response = requests.get(url+ticker, headers=headers)
    if response.status_code != 200:
        print("nope")
        continue
    print("all good")
    start = response.text.find('yf-ipw1h0">')+11
    end = response.text.find("<",start)
    value = float(response.text[start:end].strip())

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

print(asset_worths)

st.header("Investments")

value = 0 
for asset in asset_worths:
    value += asset_worths[asset]
print(value)

st.dataframe(big_data)
st.markdown('<h1 style="font-size: 300px; white-space: nowrap;">'+str(value)+'</h1>', unsafe_allow_html=True)
