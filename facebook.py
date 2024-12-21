from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from chrome_profile import create_chrome
import pandas as pd
import os
import time

class FacebookBot:
    def __init__(self, group_url):
        self.driver = create_chrome()
        self.driver.get(group_url)
        print("Bot is running...")

    def post_image_with_caption(self, image_folder, caption_file):
        # Post images with captions from a CSV file
        data = pd.read_csv(caption_file)
        for index, row in data.iterrows():
            image_name = row['image_name']
            caption = row['caption']

            # Wait for the group page to load
            time.sleep(3)


            # Wait for the post button using the text "Photo/video"
            post_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Photo/video']"))
            )
            post_button.click()
            time.sleep(10)  # Wait for the post to complete
            

            # Wait for the "Write something..." box to be clickable
            caption_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="dialog"] div[role="textbox"]'))
            )
            caption_box.click()
            time.sleep(1)

            # Add the caption
            caption_box.send_keys(caption)
            time.sleep(2)

            # Add the image
            image_path = os.path.join(image_folder, image_name)
            image_upload = self.driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"] input[type="file"]')
            image_upload.send_keys(image_path)
            time.sleep(3)  # Wait for the image to upload

            # Post it in the group
            post_button = self.driver.find_element(By.XPATH, "//div[@aria-label='Post']")
            post_button.click()
            time.sleep(10)  # Wait for the post to complete

# Example usage
if __name__ == "__main__":
    group_url = "https://www.facebook.com/groups/339050817509088"  # Directly using the Facebook group URL

    bot = FacebookBot(group_url)

    # To post image with caption from a CSV file
    image_folder = r"D:\My Work\Automation\FB GRP POST\images"
    caption_file = r"D:\My Work\Automation\FB GRP POST\image_captions.csv"
    bot.post_image_with_caption(image_folder, caption_file)

    input("Press Enter to exit...")
