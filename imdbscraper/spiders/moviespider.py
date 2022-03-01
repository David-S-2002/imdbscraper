import scrapy
import datetime


class MovieSpider(scrapy.Spider):
    name = "movie"
    start_urls = ["https://www.imdb.com/chart/top"]

    def parse(self, response):
        return (scrapy.Request(url=f"https://www.imdb.com{url}", callback=self.parse_movie_page) for url in response.css(".titleColumn a").xpath("@href").extract())

    def parse_movie_page(self, response):
        # keep the movie_id in the length of 6
        mid = response.url.rsplit("/", 2)[-2][0:6]
        raw_release_date = response.css(
            "section.ipc-page-section[data-testid='Details'] li[data-testid='title-details-releasedate'] ul a::text").extract_first()

        # Release date will be crawled with release country but
        # we don't want that
        trim_release_date = raw_release_date.rsplit("(", 1)[0][:-1]

        # Load string format to datetime object
        release_date_obj = datetime.datetime.strptime(
            trim_release_date, "%B %d, %Y")

        yield {
            "mid": mid,
            "name": response.css("section.ipc-page-section h1::text").extract_first(),
            "mpaa": response.css("section.ipc-page-section li:nth-child(2) a::text").extract_first(),
            "description": response.css("section.ipc-page-section span[data-testid='plot-xl']::text").extract_first().strip(),
            "release_date": release_date_obj.strftime("%m/%d/%Y"),
            "overall_rating": 0,
            "genre": [genre for genre in response.css("li[data-testid='storyline-genres'] a::text").extract()]
        }
