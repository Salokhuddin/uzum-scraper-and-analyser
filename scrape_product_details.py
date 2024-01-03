# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys
from selenium.webdriver.common.action_chains import ActionChains

# Scrapes details of a products from product page


def main():
    # Set options (prevents the browser from closing after opening)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # Open the browser
    print('Opening browser')
    driver = webdriver.Chrome(options=options)
    print('Opened browser')

    # Maximize the browser to fullscreen
    driver.maximize_window()
    print('Maxed browser')

    # get all the links
    products = get_links()

    # Get the product info:
    for product in products:
        product_number = product['product_number']
        link = product['link']
        driver.implicitly_wait(10)
        driver.get(link)
        save('product_details.csv', 
                        'a',
                        get_product_details(driver, link), product_number)
        remove_done_product(products, product_number)
        print(f'Success on *****{product_number}*****')
        

def remove_done_product(products, product_number):
    with open('final_links.csv', 'w') as file:
        fieldnames=['product_number', 'link', 'page_number', 'category_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products[product_number + 1:]:
            writer.writerow({'product_number': product['product_number'], 
                             'link': product['link'], 
                             'page_number': product['page_number'],
                             'category_number': product['category_number']})


# Creating a function to get product details
def get_product_details(driver, link):           
    product_name = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/h1').text
    total_sold = driver.find_element(By.CLASS_NAME, 'orders').find_element(By.TAG_NAME, 'span').text
    merchant_name = driver.find_element(By.CLASS_NAME, 'product-info-item-value.col-mbs-9.product-info-item-value--seller').text
    price = driver.find_element(By.CLASS_NAME, 'currency').text
    last_week_sale = driver.find_element(By.CLASS_NAME, 'offer-text').text
    overall_rating = driver.find_element(By.CLASS_NAME, 'rating-value').text
    number_of_reviews = driver.find_element(By.CLASS_NAME, 'reviews-info').text
    # breadcrumbs = driver.find_element(By.CLASS_NAME, 'breadcrumbs').find_elements(By.TAG_NAME, 'a')
    breadcrumb = (list(map(lambda breadcrum: breadcrum.text, 
                           driver.find_element(By.CLASS_NAME, 'breadcrumbs').find_elements(By.TAG_NAME, 'a'))))[2:]
    
    return [product_name,
            total_sold,
            merchant_name,
            price,
            last_week_sale,
            overall_rating,
            number_of_reviews,
            '/'.join(breadcrumb),
            link]


                             
            



def save(file_name, method, field_vars, product_number):
    field_names = [
        'product_name', 
        'total_sold', 
        'merchant_name', 
        'price', 
        'last_week_sale', 
        'overall_rating', 
        'number_of_reviews',
        'breadcrumb',
        'link']
    row_dict = dict(zip(field_names, field_vars))
    with open(file_name, method) as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        if product_number == 1:
            writer.writeheader()
        writer.writerow(row_dict)
        print(f'Success on saving {product_number}')


def get_links():
    links = []
    with open('test.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append({'link': row['link'], 'product_number': row['product_number']})
        return links


if __name__ == "__main__":
    main()



