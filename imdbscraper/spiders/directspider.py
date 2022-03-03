import scrapy


class MovieSpider(scrapy.Spider):
    name = "direct"
    start_urls = ["https://www.imdb.com/chart/top"]

    def parse(self, response):
        return (scrapy.Request(url=f"https://www.imdb.com{url}", callback=self.parse_movie_page) for url in response.css(".titleColumn a").xpath("@href").extract())

    def parse_movie_page(self, response):
        mid: str = response.url.rsplit("/", 2)[-2]

        if len(mid) == 8:
            mid = mid + "0"
        if len(mid) == 10:
            mid = mid[0:8] + "x"

        directors = [director.rsplit("/")[2] for director in response.css(
            "div[data-testid='title-pc-wide-screen'] li.ipc-metadata-list__item:nth-child(1) li a").xpath("@href").extract()]

        writers = [writer.rsplit("/")[2] for writer in response.css(
            "div[data-testid='title-pc-wide-screen'] li.ipc-metadata-list__item:nth-child(2) li a").xpath("@href").extract()]

        yield {
            "mid": mid,
            "did": list(set(directors) | set(writers)),
        }
