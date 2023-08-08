import time
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


def get_item_total(elm):
    item_total = elm.find_element(By.CLASS_NAME, "summary_subtotal_label").text
    item_total_price_string = item_total.replace("Item total: $", "")
    prices = float(item_total_price_string)
    return (prices)


def get_tax_item(elm1):
    tax = elm1.find_element(By.CLASS_NAME, "summary_tax_label").text
    tax_price_string = tax.replace("Tax: $", "")
    price_tax = float(tax_price_string)
    return (price_tax)


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

# TC007 As a USer , I can add to cart the products
driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
driver.find_element(By.XPATH, "//span[text()='Your Cart']").is_displayed()
items = driver.find_element(By.XPATH, "//div[text()='Sauce Labs Backpack']").text
actual_items = "Sauce Labs Backpack"
if items == actual_items:
    print("List Cart Product Passed")
else:
    print("List Cart Product Failed")

# TC008 As a USer , I can checkout the cart
driver.find_element(By.ID, "checkout").click()
firstName = driver.find_element(By.ID, "first-name").send_keys("Randy")
driver.find_element(By.ID, "last-name").send_keys("Pangalila")
driver.find_element(By.ID, "postal-code").send_keys("123763")
driver.find_element(By.ID, "continue").click()
driver.get("https://www.saucedemo.com/checkout-step-two.html")
title_checkout = driver.find_element(By.CLASS_NAME, "title").text
act_title_checkout = "Checkout: Overview"
if title_checkout == act_title_checkout:
    print("Checkout overview Passed")
else:
    print("Checkout overview Failed")

# TC009 As a user, I can see the price total
item_total = get_item_total(driver)
item_tax = get_tax_item(driver)
finaltotal = item_total + item_tax
exp_price_total = "Total: $" + str(finaltotal)
act_price_total = driver.find_element(By.CLASS_NAME, "summary_info_label.summary_total_label").text
if exp_price_total == act_price_total:
    print("Value Price Total Passed")
else:
    print("Value Price Total Failed")
driver.find_element(By.ID, "finish").click()
# time.sleep(2000)
driver.get("https://www.saucedemo.com/checkout-complete.html")
driver.find_element(By.XPATH, "//span[text()='Checkout: Complete!']").is_displayed()
driver.find_element(By.XPATH, "//h2[text()='Thank you for your order!']").is_displayed()
driver.find_element(By.ID, "back-to-products").click()


# T010 As a user, I want to remove the items
driver.find_element(By.XPATH, "//span[text()='Products']").is_displayed()
driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket").click()
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
driver.find_element(By.XPATH, "//span[text()='Your Cart']").is_displayed()
driver.find_element(By.ID, "remove-sauce-labs-fleece-jacket").click()
driver.find_element(By.CLASS_NAME, "removed_cart_item").is_displayed()
driver.find_element(By.ID,"continue-shopping").click()

#T011 As a user, I can Access burger menu Swag Labs
driver.find_element(By.ID, "react-burger-menu-btn").click()
driver.find_element(By.ID, "inventory_sidebar_link").is_displayed()
driver.find_element(By.ID, "about_sidebar_link").is_displayed()
driver.find_element(By.ID, "logout_sidebar_link").is_displayed()
driver.find_element(By.ID, "reset_sidebar_link").is_displayed()
print("Burger Menu Passed")

# T012 As a user, I can Access About from Burger Menu
time.sleep(2)
driver.find_element(By.ID, "about_sidebar_link").click()
time.sleep(2)
driver.find_element(By.XPATH, "//p[text()='The world relies on your code. Test on thousands of different device, browser, and OS configurations–anywhere, any time.']").is_displayed()
driver.quit()

#T013 As a user, I can Logout the web
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.saucedemo.com/")
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
time.sleep(2)
driver.find_element(By.ID, "react-burger-menu-btn").click()
time.sleep(2)
driver.find_element(By.ID, "logout_sidebar_link").is_displayed()
driver.find_element(By.ID, "logout_sidebar_link").click()
driver.find_element(By.CLASS_NAME,"login_logo").is_displayed()
actual_logout = driver.find_element(By.CLASS_NAME,"login_logo").text
expected_logout = "Swag Labs"
if expected_logout == actual_logout:
    print("Logout Passed")
else:
    print("Logout Failed")

driver.quit()




