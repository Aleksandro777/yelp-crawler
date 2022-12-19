import scrapy
from scrapy.http import Response


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
        "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"
    ]
    headers = {
        "user-agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }

    def parse(self, response: Response, **kwargs):

        for link in response.css(".css-1agk4wl a::attr(href)"):
            yield response.follow(link, callback=self.parse_restaurant)

            next_page = (
                response.css(".pagination-links__09f24__bmFj8 > div")[-1]
                .css("a::attr(href)")
                .get()
            )
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_restaurant(self, response: Response):

        yield {
            "name": response.css("h1.css-1se8maq::text").get(),
            "raiting": float(
                response.css(".five-stars__09f24__mBKym::attr(aria-label)")
                .get()
                .split(" ")[0]
            ),
            "reviews_number": int(
                response.css(
                    ".arrange-unit__09f24__rqHTg > .css-1fdy0l5 > .css-1m051bw::text"
                )
                .get()
                .split(" ")[0]
            ),
            "buisness_page": response.request.url,
            "business_website": response.css(
                "div.css-1vhakgw > div.arrange__09f24__LDfbs > "
                "div.arrange-unit__09f24__rqHTg > .css-1p9ibgf > a.css-1um3nx::text"
            ).get(),
            "reviews": self.parse_reviews(response),
        }

    def parse_reviews(self, response: Response):
        name_list = response.css("span.fs-block > a.css-1m051bw::text").getall()[:5]
        location_list = response.css(
            ".responsive-hidden-small__09f24__qQFtj > div.border-color--default__09f24__NPAKY > span.css-qgunke::text"
        ).getall()[1:6]
        date_list = response.css(
            ".margin-t1__09f24__w96jn > .arrange__09f24__LDfbs > div.arrange-unit__09f24__rqHTg > span.css-chan6m::text"
        ).getall()[:5]
        review = {}
        review_list = []
        for i in range(5):
            review["reviewer_name"] = name_list[i]
            review["reviewer_location"] = location_list[i]
            review["review_date"] = date_list[i]
            review_list.append(review)
            review = {}

        return review_list
