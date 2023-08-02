from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_inventory_names(params):
    inventory_names = []  # A-Z
    elements = params.find_element(By.CLASS_NAME, "inventory_list")
    elements_item = elements.find_elements(By.CLASS_NAME, "inventory_item")
    for item in elements_item:
        inventory_item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text

        inventory_names.append(inventory_item_name)
    return inventory_names


def get_inventory_price(params):
    inventory_price = []  # A-Z
    elements = params.find_element(By.CLASS_NAME, "inventory_list")
    elements_items = elements.find_elements(By.CLASS_NAME, "inventory_item")
    for item in elements_items:
        inventory_item_price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        price_string = inventory_item_price.replace("$", "")
        price = float(price_string)
        inventory_price.append(price)
    return inventory_price

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.saucedemo.com/")


# TC001 As a user I can Login to the Swag Labs
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

act_title = driver.title
exp_title = "Swag Labs"
if act_title == exp_title:
    print("Login Test Passed")
else:
    print("Login Test Failed")


# TC002 As a User I can see the details of product
driver.find_element(By.ID, "item_4_title_link").click()
actDetailsProd = driver.find_element(By.XPATH, "//div[text()='Sauce Labs Backpack']").text
# print(actDetailsProd)
expDetailsProd = "Sauce Labs Backpack"

if actDetailsProd == expDetailsProd:
    print("Details Product Passed")
else:
    print("Details Product Failed")


# TC003 As a User I can back to the list products
driver.find_element(By.ID, "back-to-products").click()

actProducts = driver.find_element(By.XPATH, "//span[contains(text(),'Products')]").text
expProducts = "Products"

if actProducts == expProducts:
    print("List Product Passed")
else:
    print("List Product Failed")


# TC004 As a USer , I can filter the products from Z to A
driver.find_element(By.CLASS_NAME, "product_sort_container").click()
driver.find_element(By.CSS_SELECTOR, "option[value='az']").click()

init_item_names = get_inventory_names(driver)

driver.find_element(By.CLASS_NAME, "product_sort_container").click()
driver.find_element(By.CSS_SELECTOR, "option[value='za']").click()

sorted_item_names = get_inventory_names(driver)

if sorted_item_names == sorted(init_item_names, reverse=True):
    print("Sort List Product Passed")
else:
    print("Sort List Product Failed")


# TC005 As a USer , I can filter the products from low price to high price
driver.find_element(By.CLASS_NAME, "product_sort_container").click()
driver.find_element(By.CSS_SELECTOR, "option[value='lohi']").click()

init_item_price = get_inventory_price(driver)
sorted_items_price = get_inventory_price(driver)
if sorted_items_price == sorted(init_item_price):
    print("Sort Low price Product Passed")
else:
    print("Sort Low price Failed")


# TC006 As a USer , I can filter the products from high price to low price
driver.find_element(By.CLASS_NAME, "product_sort_container").click()
driver.find_element(By.CSS_SELECTOR, "option[value='hilo']").click()

init_item_price = get_inventory_price(driver)
sorted_items_price = sorted(init_item_price, reverse=True)
if sorted_items_price == sorted(init_item_price, reverse=True):
    print("Sort high price Product Passed")
else:
    print("Sort high price Failed")


driver.close()
