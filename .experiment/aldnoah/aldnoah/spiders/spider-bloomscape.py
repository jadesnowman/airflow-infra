import scrapy

class PlantsSpider(scrapy.Spider):
    name = "plants"
    start_urls = [
        "https://bloomscape.com/shop/shop-all-plants/",
    ]    

    def parse(self, response):

        yield {
            "url": response.css("div.product-container a::attr(href)").getall()
        }

        for plant in response.css("div.product-container a"):

            badge = plant.css("div.product-badge::text").get()
            title = plant.css("div.product-info h2::text").get()
            size = plant.css("div.product-info div.product-info__meta::text").get()
            price = plant.css(
                    "div.product-info div.product-info__price bdi::text"
                ).get()

            yield {
                "image": {
                    "alt": plant.css("img::attr(alt)").get(),
                    "src": plant.css("img::attr(src)").get(),
                    "srcset": plant.css("img::attr(srcset)").get(),
                },
                "badge": badge,
                "title": title,
                "size": size,
                "price": price
            }
