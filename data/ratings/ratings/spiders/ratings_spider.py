from pathlib import Path

import pandas as pd
import scrapy

from data.data import OUTPUT_DIR


#  poetry run scrapy crawl ratings -a showeid=tt2078818
# poetry run scrapy shell "https://www.imdb.com/title/tt2078818/reviews"

# https://docs.scrapy.org/en/latest/topics/practices.html
# https://stackoverflow.com/a/15618520/4198382
# For every show:
# Collect every review { user_id, show_id, rating }
# https://www.imdb.com/title/tt0944947/reviews/
# https://www.imdb.com/user/ur59092557/ratings


class RatingsSpider(scrapy.Spider):
    name = "ratings"

    def __init__(self, show_id=None, *args, **kwargs):
        super(RatingsSpider, self).__init__(*args, **kwargs)
        self.show_id = show_id
        self.start_urls = [f"https://www.imdb.com/title/{self.show_id}/reviews"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"ratings/files/{self.show_id}.csv"

        reviews = response.css(".lister-item-content")
        num_reviews = len(reviews)

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
        df.to_csv(filename, index=False)
        self.log(f"Saved file {filename}")
