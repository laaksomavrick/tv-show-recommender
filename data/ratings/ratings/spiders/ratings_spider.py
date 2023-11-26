from pathlib import Path
from time import sleep

import pandas as pd
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import TextResponse

#  poetry run scrapy crawl ratings -a show_ids=...


class RatingsSpider(scrapy.Spider):
    name = "ratings"

    custom_settings = {"COOKIES_ENABLED": False, "DOWNLOAD_DELAY": 2}

    def __init__(self, show_ids=None, *args, **kwargs):
        super(RatingsSpider, self).__init__(*args, **kwargs)
        self.show_ids = show_ids.split(",")
        self.driver = webdriver.Chrome()

    def start_requests(self):
        for show_id in self.show_ids:
            print(f"Scraping show_id={show_id}")

            url = f"https://www.imdb.com/title/{show_id}/reviews?sort=reviewVolume&dir=desc&ratingFilter=0"

            print(f"Locating {url}")

            self.driver.get(url)
            self.load_all_reviews()

            body = self.driver.page_source.encode("utf-8")
            response = TextResponse(url=url, body=body, encoding="utf-8")

            self.parse(show_id, response)
            sleep(0.25)

        self.driver.quit()

    def parse(self, show_id, response):
        filename = f"ratings/files/{show_id}.csv"
        lister_item_content = response.css(".lister-item-content")
        num_reviews = len(lister_item_content)

        print(f"Found review count={num_reviews}")

        rows = []

        for lister_item in lister_item_content:
            print(f"Processing lister_item for show_id={show_id}")
            maybe_rating = lister_item.css("span.rating-other-user-rating").css(
                "span::text"
            )

            if len(maybe_rating) < 3:
                continue

            rating = maybe_rating[2].get()
            user_href = lister_item.css(".display-name-link").css("::attr(href)").get()

            if user_href is None:
                continue

            split_user_href = user_href.split("/")
            user_id = split_user_href[-2]

            print(f"Appending show_id={show_id} user_id={user_id} rating={rating}")
            rows.append({"show_id": show_id, "user_id": user_id, "rating": rating})

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        self.log(f"Saved file {filename}")

    def load_all_reviews(self):
        more_reviews_iter = 0
        has_more_reviews = self.has_load_more()

        print(f"has_more_reviews={has_more_reviews}")

        while has_more_reviews is True and more_reviews_iter < 50:
            print(f"More reviews found on iter={more_reviews_iter}, loading more...")
            self.click_load_more()
            sleep(0.5)
            has_more_reviews = self.has_load_more()
            more_reviews_iter += 1

    def click_load_more(self):
        try:
            load_more_button = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[text()='Load More']")
                )
            )

            load_more_button.click()

            WebDriverWait(self.driver, 2).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//button[text()='Load More']"), "Load More"
                )
            )
        except Exception as e:
            print(f"Error: {e}")

    def has_load_more(self):
        try:
            load_more_buttons = WebDriverWait(self.driver, 1).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[text()='Load More']")
                )
            )

            if len(load_more_buttons) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False
