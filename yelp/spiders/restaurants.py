from urllib.parse import urljoin

import scrapy
from scrapy.http import Response


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    allowed_domains = ["www.yelp.com"]
    start_urls = [
        "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"
    ]

    def parse(self, response: Response, **kwargs):
        # filename = f"restaurants.html"
        # with open(filename, "wb") as f:
        #     f.write(response.body)
        # self.log(f"Saved file {filename}")
        for restaurant in response.css(".arrange__09f24__LDfbs "):
            name = restaurant.css(".css-1m051bw::attr(name)").get()
            if name is not None:
                yield {
                    "name": name,
                    "rating": float(
                        restaurant.css(
                            ".five-stars--regular__09f24__DgBNj::attr(aria-label)"
                        )
                        .get()
                        .split(" ")[0]
                    ),
                    "reviews": int(
                        restaurant.css(
                            ".border-color--default__09f24__NPAKY > .display--inline-block__09f24__fEDiJ > .css-chan6m::text"
                        ).get()
                    ),
                    "buisness_page": urljoin(
                        self.start_urls[0],
                        restaurant.css(
                            ".child__09f24__Z2_cG > .css-w8rns > a::attr(href)"
                        ).get(),
                    ),
                }
            next_page = response.css(".pagination-links__09f24__bmFj8 > div")[-1].css("a::attr(href)").get()
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
