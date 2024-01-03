from selenium import webdriver
from selenium.webdriver.common.by import By
import csv, time, sys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# Scrapes product_links from category links 
# number_of_product = '393,026 ta tovar'
def main():
    # Set options (prevents the browser from closing after opening)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # Open the browser
    driver = webdriver.Chrome(options=options)
    # Maximize the browser to fullscreen
    driver.maximize_window()
    category_links = get_links()
    link_head = "https://uzum.uz/uz"
    link_pager = '?currentPage='
    
    category_no = 2
    

    for category_link in category_links:
        exit_code = 0
        page_number = 1
        while True:
            driver.implicitly_wait(10)
            link = f'{link_head}{category_link}{link_pager}{page_number}'
            driver.get(link)
            # check 'I'm older than 18'   
            try:
                driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/button[2]').click()
                print('Success on 18 age')
            except Exception:
                # Record product links
                try:
                    # nav_buttons = driver.find_elements(By.CLASS_NAME, 'ui-component.ui-button.button-more')
                    title = driver.find_element(By.CLASS_NAME, 'title.title-bold').text
                    product_cards = driver.find_elements(By.CLASS_NAME, 'subtitle-item')                    
                    product_links = map(lambda product_card: product_card.get_attribute('href'), product_cards)                    
                    save(product_links, page_number, driver, category_no)
                    print(f"Success on page: {page_number} | category: {category_no}")
                    page_number += 1
                except Exception:
                    exit_code = 10000     
                    print(Exception)     
                    print(page_number)
                    break
                if exit_code == 10000:
                    break
        category_no += 1
        page_number += 1

def save(links, page_no, driver, category_no):
    with open('new_product_links1.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=['link', 'page_number', 'category_no'])
        if category_no == 1 and page_no == 1:
            writer.writeheader()
        for link in links:
            writer.writerow({'link': link, 'page_number': page_no, 'category_no': category_no})
        print(f"Success on saving page {page_no} | category: {category_no}")


def get_links():
    pass
    links = []
    with open('categories.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row['link'])
    return links

if __name__ == "__main__":
    main()