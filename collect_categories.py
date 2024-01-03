from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')

# Open the browser
driver = webdriver.Chrome(options=options)
# Maximize the browser
driver.maximize_window()
parent_category_name = ''
main_categories = [
                    {'link': 'https://uzum.uz/uz/category/barcha-toifalar-1',
                    'name': 'Main Page'}
]

def main(main_categories, depth=0):
    for category in main_categories:
        name = category['name']
        link = category['link']
        driver.implicitly_wait(10)
        driver.get(link)
        child_categories = get_details()
        if child_categories[0]['name'] != name and not check_siblings(name, child_categories):
            print(child_categories[0]['name'])
            save(depth, child_categories, parent_category_link=link)
            main(child_categories, depth + 1)

def check_siblings(name, child_categories):
    list(map(lambda cat: cat['name'], child_categories))
    for category in list(map(lambda cat: cat['name'], child_categories)):
        if name == category:
            return True




def get_details():
    categories_panel = driver.find_element(By.CLASS_NAME, 'hug.category-list.category-list--child').find_elements(By.TAG_NAME, 'li')
    names_and_links = []
    for category in categories_panel:
        name = category.text.strip()            
        link = category.find_element(By.TAG_NAME, 'a').get_attribute('href')
        names_and_links.append({'name': name, 'link': link})
    return names_and_links


def save(depth, categories, parent_category_link=''):
    if parent_category_link == main_categories[0]['link']:
        file_name = 'main_categories.csv'
    else:
        file_name = f'{depth}_categories.csv'
    with open(file_name, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=['link', 'name', 'parent_category_link'])

        # Check file size to determine if header row is needed or not
        if os.stat(file_name).st_size == 0:
            writer.writeheader()
        for category in categories:
            parent_category_link = parent_category_link.replace('https://uzum.uz/uz', '').strip()
            writer.writerow({'link': category['link'].strip(), 
                             'name': category['name'].strip(), 
                             'parent_category_name': parent_category_link})
            print(f'Saved: {category["name"]} of {parent_category_link}')
       

if __name__ == '__main__':
    main(main_categories)










