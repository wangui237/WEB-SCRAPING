import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = 'https://www.jumia.co.ke/flash-sales/'

response = requests.get(url)
print(f"Status Code: {response.status_code}")


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    
    products_section = soup.find_all('div', class_='Phones and tablets')  

    
    data = []
    for product in products_section:
        name = product.find('h2', class_='Mobile phones').text.strip() if product.find('h2', class_='Mobile phones') else 'N/A'
        brand = product.find('div', class_='OPPO').text.strip() if product.find('div', class_='OPPO') else 'N/A'
        price = product.find('div', class_='12,708').text.strip() if product.find('div', class_='`12708') else 'N/A'
        discount = product.find('span', class_='26%').text.strip() if product.find('span', class_='26%') else 'N/A'
        reviews = product.find('span', class_='review-count').text.strip() if product.find('span', class_='review-count') else '0'
        rating = product.find('div', class_='rating').text.strip() if product.find('div', class_='rating') else '0'

        
        rating = float(re.search(r'\d+(\.\d+)?', rating).group()) if rating != '0' else 0

        data.append({
            'Product Name': name,
            'Brand Name': brand,
            'Price (Ksh)': price,
            'Discount (%)': discount,
            'Total Number of Reviews': reviews,
            'Product Rating (out of 5)': rating
        })

    
    df = pd.DataFrame(data)
    df.to_csv('jumia_flash_sales.csv', index=False)
    print("Data saved to jumia_flash_sales.csv")

else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")

