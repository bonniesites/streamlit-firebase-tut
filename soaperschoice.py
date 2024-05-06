import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_prices():
    url = "https://www.soaperschoice.com/product-list/base-unit-of-measure=sc-1x7lb/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = {}
        # Find all product price elements
        price_elements = soup.find_all("span", class_="price")
        for element in price_elements:
            # Extract the product name and price
            product_name = element.find_previous("h3").text.strip()
            price = element.text.strip()
            prices[product_name] = price
        return prices
    else:
        st.error("Failed to retrieve prices.")

def main():
    st.title("Product Prices")

    # Get prices
    prices = get_prices()

    if prices:
        # Display prices
        st.subheader("Prices:")
        for product_name, price in prices.items():
            st.write(f"- {product_name}: {price}")

        # Display date retrieved
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"\nPrices retrieved on: {current_date}")

if __name__ == "__main__":
    main()
