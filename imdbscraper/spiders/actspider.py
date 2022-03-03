import scrapy


class ActSpider(scrapy.Spider):
    name = "act"
    start_urls = ["https://www.imdb.com/chart/top"]

    def parse(self, response):
        return (scrapy.Request(url=f"https://www.imdb.com{url}", callback=self.parse_movie_page) for url in response.css(".titleColumn a").xpath("@href").extract())

    def parse_movie_page(self, response):
        mid: str = response.url.rsplit("/", 2)[-2]

        if len(mid) == 8:
            mid = mid + "0"
        if len(mid) == 10:
            mid = mid[0:8] + "x"

        actors = [director.rsplit("/")[2][0:9] for director in response.css(
            "div[data-testid='title-pc-wide-screen'] li.ipc-metadata-list__item:nth-child(3) li a").xpath("@href").extract()]

        yield {
            "mid": mid,
            "aid": actors,
        }
