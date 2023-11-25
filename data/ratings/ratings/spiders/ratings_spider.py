from pathlib import Path
from time import sleep

import pandas as pd
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import TextResponse


#  poetry run scrapy crawl ratings -a show_id=tt2078818
#  poetry run scrapy crawl ratings -a show_id=tt0944947 # Game of Thrones
#  poetry run scrapy shell "https://www.imdb.com/title/tt2078818/reviews"


class RatingsSpider(scrapy.Spider):
    name = "ratings"

    custom_settings = {"COOKIES_ENABLED": False, "DOWNLOAD_DELAY": 2}

    def __init__(self, show_id=None, *args, **kwargs):
        super(RatingsSpider, self).__init__(*args, **kwargs)
        self.show_id = show_id
        self.driver = webdriver.Chrome()
        self.url = f"https://www.imdb.com/title/{self.show_id}/reviews?sort=reviewVolume&dir=desc&ratingFilter=0"
        self.filename = f"ratings/files/{self.show_id}.csv"

    def start_requests(self):
        # TODO: read list of ids

        print(f"Locating {self.url}")

        self.driver.get(self.url)
        self.load_all_reviews()

        body = self.driver.page_source.encode("utf-8")
        response = TextResponse(url=self.url, body=body, encoding="utf-8")

        self.parse(response)
        self.driver.quit()

    def parse(self, response):
        self.parse_show_page(response)

    def parse_show_page(self, response):
        reviews = response.css(".lister-item-content")
        num_reviews = len(reviews)

        print(f"Found review count={num_reviews}")

        rows = []

        for i in range(0, num_reviews):
            show_id = self.show_id
            rating = (
                response.css(".rating-other-user-rating")
                .xpath(
                    '//div[@class="lister-item-content"]//span[@class="rating-other-user-rating"]/span[1]/text()'
                )[i]
                .get()
            )

            user_href = (
                response.css(".display-name-link")
                .xpath('//span[@class="display-name-link"]/a/@href')[i]
                .get()
            )
            split_user_href = user_href.split("/")
            user_id = split_user_href[-2]

            rows.append({"show_id": show_id, "user_id": user_id, "rating": rating})

        df = pd.DataFrame(rows)
        df.to_csv(self.filename, index=False)
        self.log(f"Saved file {self.filename}")

    def load_all_reviews(self):
        more_reviews_iter = 0
        has_more_reviews = self.has_load_more()

        print(f"has_more_reviews={has_more_reviews}")

        while has_more_reviews is True and more_reviews_iter < 50:
            print(f"More reviews found on iter={more_reviews_iter}, loading more...")
            self.click_load_more()
            sleep(2)
            has_more_reviews = self.has_load_more()
            more_reviews_iter += 1

    def click_load_more(self):
        try:
            # Find and click the "Load More" button
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[text()='Load More']")
                )
            )

            load_more_button.click()

            # Wait for the button text to re-appear in the DOM after clicking
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//button[text()='Load More']"), "Load More"
                )
            )
        except Exception as e:
            print(f"Error: {e}")

    def has_load_more(self):
        try:
            load_more_buttons = WebDriverWait(self.driver, 10).until(
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
