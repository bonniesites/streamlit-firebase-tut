import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
import time

# Function to scrape Amazon product information
def scrape_amazon_product(url):
    # url = 'view-source:' + url
    # # Send a GET request to the Amazon product page
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # html_content = response.text
    # Initialize a Chrome webdriver (you'll need to download chromedriver executable:
    # https://sites.google.com/a/chromium.org/chromedriver/)
    driver = webdriver.Chrome()        
    # Load the webpage
    driver.get(url)
    # Wait for the captcha image to load (adjust sleep time as needed)
    time.sleep(2)
    # Locate the captcha image element
    captcha_image_element = driver.find_element_by_xpath("//img[@id='auth-captcha-image']")
    st.write(f'captcha_text:  {captcha_text}')
    # Extract the URL of the captcha image
    captcha_image_url = captcha_image_element.get_attribute("src")
    # Download the captcha image
    captcha_image_data = requests.get(captcha_image_url).content
    with open("captcha_image.png", "wb") as f:
        f.write(captcha_image_data)
    # Use OCR (Tesseract) to extract text from the captcha image
    captcha_text = pytesseract.image_to_string(Image.open("captcha_image.png"))
    st.write(f'captcha_text:  {captcha_text}')
    # Enter the extracted text into the captcha text input field
    captcha_input_element = driver.find_element_by_xpath("//input[@id='captchacharacters']")
    captcha_input_element.send_keys(captcha_text)
    # Submit the form to validate the captcha
    submit_button = driver.find_element_by_xpath("//button[@type='submit']")
    st.write(f'captcha_text:  {captcha_text}')
    print(f'captcha_text:  {captcha_text}')
    submit_button.click()
    # Get the HTML content
    soup = driver.page_source
    # st.write(f'soup: {soup}')
    st.write(f'soup: {soup}')
    # Close the webdriver
    driver.quit()
    # Extract product information from the page
    title = soup.find('span', {'id': 'productTitle'}).text.strip()
    description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
    unit_description = soup.find('span', {'class': 'a-text-bold'}).text.strip()
    number_of_units = soup.find('span', {'class': 'a-dropdown-prompt'}).text.strip()
    price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()    
    return {
        'title': title,
        'description': description,
        'unit_description': unit_description,
        'number_of_units': number_of_units,
        'price': price
    }

# Function to connect to MongoDB and insert product information
def insert_to_mongodb(product_info):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['amazon_products']
    collection = db['products']
    # Insert product information into MongoDB
    product_info['date_checked'] = datetime.now()
    collection.insert_one(product_info)
    st.success('Product information inserted into MongoDB successfully!')

# Function to calculate price per unit
def calculate_price_per_unit(price, number_of_units):
    # Implement your logic to calculate price per unit here
    return price

# Main Streamlit app
st.title('Amazon Product Scraper')

# Input field for the Amazon product URL
url = st.text_input('Enter Amazon product URL:')
if st.button('Scrape Product Info'):
    if url:
        # Scrape product information
        product_info = scrape_amazon_product(url)

        # Insert product information into MongoDB
        insert_to_mongodb(product_info)

# Display products from MongoDB
st.subheader('Products in MongoDB:')
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['amazon_products']
collection = db['products']

# Fetch products from MongoDB
products = collection.find({})
for product in products:
    # Calculate price per unit
    price_per_unit = calculate_price_per_unit(product['price'], product['number_of_units'])

    # Display product information
    st.write(f"**Title:** {product['title']}")
    st.write(f"**Description:** {product['description']}")
    st.write(f"**Unit Description:** {product['unit_description']}")
    st.write(f"**Number of Units:** {product['number_of_units']}")
    st.write(f"**Price:** {product['price']}")
    st.write(f"**Date Checked:** {product['date_checked']}")
    st.write(f"**Price per Unit:** {price_per_unit}")
    st.write('---')
