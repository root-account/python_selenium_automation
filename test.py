from selenium import webdriver
import re

# You need to download the google chrome driver https://sites.google.com/a/chromium.org/chromedriver/
# Provide a path to the google chrome webdriver, thats the path you downloaded it to
driver = webdriver.Chrome("/Users/Donatello/Desktop/automation_python/chromedriver")

# The URL your script must visit
driver.get("http://")


# Find the username and password fields
email_input = driver.find_element_by_id("user_login")
pass_input = driver.find_element_by_id("user_pass")
cnt_submit = driver.find_element_by_id("wp-submit")

# Fill in your login details to login
# For the script to be able to login you need to supply your login details
email_input.send_keys("WORDPRESS USERNAME")
pass_input.send_keys("WORDPRESS PASWORD")

# Submit login form
cnt_submit.click()

# Wait for page to load everything
driver.implicitly_wait(10)

# Click Media on the menu
notNow = driver.find_element_by_link_text('Media')
notNow.click()

# Open the first image
thumbnail = driver.find_element_by_class_name('thumbnail')
thumbnail.click()

def task_function():
    # Copy the name of the image form the title input box
    image_text = driver.find_element_by_xpath("//label[@data-setting='title']/input[@type='text']").get_attribute('value')

    print(image_text)

    # Remove special characters from the image name
    image_text = re.sub('[^a-zA-Z0-9 \n\.]', ' ', image_text)

    print(image_text)

    # Select the alt input box and paste the image title into it
    alt_text = driver.find_element_by_xpath("//label[@data-setting='alt']/input[@type='text']")
    alt_text.clear()
    alt_text.send_keys(image_text.title())
    driver.implicitly_wait(2)

    # Select the Description input box and paste the image title into it
    desc_text = driver.find_element_by_xpath("//label[@data-setting='description']/textarea")
    desc_text.clear()
    desc_text.send_keys(image_text.title())
    driver.implicitly_wait(2)

    # Select the Caption input box and paste the image title into it
    caption_text = driver.find_element_by_xpath("//label[@data-setting='caption']/textarea")
    caption_text.clear()
    caption_text.send_keys(image_text.title())
    driver.implicitly_wait(2)

    # Select the title input box and paste the cleaned up image title into it
    title_text = driver.find_element_by_xpath("//label[@data-setting='title']/input[@type='text']")
    title_text.clear()
    title_text.send_keys(image_text.title())
    driver.implicitly_wait(2)

    # Go to next post
    next_post = driver.find_element_by_class_name("right")
    next_post.click()

task_function()

# Find images and save all of them to a list
all_posts = driver.find_elements_by_class_name("thumbnail")

# Loop though all the posts
for single_post in all_posts:

    # Wait for the post to load
    driver.implicitly_wait(10)

    task_function()

