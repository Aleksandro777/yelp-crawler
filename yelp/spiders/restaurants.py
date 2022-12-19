from urllib.parse import urljoin

import scrapy
from scrapy.http import Response


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"

    start_urls = [
        "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"
    ]

    def parse(self, response: Response, **kwargs):

        for link in response.css(".css-1agk4wl a::attr(href)"):
            yield response.follow(link, callback=self.parse_restaurant)

            next_page = response.css(".pagination-links__09f24__bmFj8 > div")[-1].css("a::attr(href)").get()
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_restaurant(self, response: Response, **kwargs):
        yield {
            "name": response.css("h1.css-1se8maq::text").get(),
            "raiting": float(response.css(".five-stars__09f24__mBKym::attr(aria-label)").get().split(" ")[0]),
            "reviews": int(response.css(".arrange-unit__09f24__rqHTg > .css-1fdy0l5 > .css-1m051bw::text").get().split(" ")[0]),
            "buisness_page": response.request.url,
            "Business_website": response.css("div.css-1vhakgw > div.arrange__09f24__LDfbs > div.arrange-unit__09f24__rqHTg > .css-1p9ibgf > a.css-1um3nx::text").get()
        }


