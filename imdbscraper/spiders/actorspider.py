import scrapy
import datetime
import pathlib
import json


class ActorSpider(scrapy.Spider):
    def generate_start_urls():
        path = pathlib.Path(__file__).parent
        filepath = (path / "../../acts.json").resolve()
        output = []

        with open(filepath) as json_file:
            data = json.load(json_file)
            for each in data:
                output.append(
                    f"https://www.imdb.com/name/{each['aid']}/?ref_=nmls_hd")

        return set(output)

    name = "actor"
    start_urls = list(generate_start_urls())

    # def parse(self, response):

    # return (scrapy.Request(url=f"https://www.imdb.com{url}?ref_=nmls_hd", callback=self.parse_director_page) for url in response.css(".lister-list .lister-item-header a").xpath("@href").extract())

    def parse(self, response):
        actor_id: str = response.url.rsplit("/", 2)[-2][0:9]
        name: str = response.css(
            "td.name-overview-widget__section span::text").extract_first()

        if name is None:
            name = response.css(
                ".header .itemprop::text").extract_first()
        name = name.rsplit(" ")

        birth_date = response.css("time::attr('datetime')").extract_first()
        birth_date_obj = None

        try:
            birth_date_obj = datetime.datetime.strptime(
                birth_date, "%Y-%m-%d") if birth_date is not None else datetime.datetime.strptime(
                "1970-01-01", "%Y-%m-%d")
        except:
            birth_date_obj = datetime.datetime.strptime(
                "1970-01-01", "%Y-%m-%d")

        gender = [x for x in response.css(
            "#name-job-categories a").xpath("@href").extract()]

        if "#actor" in gender:
            gender = "0"
        elif "#actress" in gender:
            gender = "1"
        else:
            gender = "null"

        birth_place_info: str = response.css(
            "#name-born-info a:nth-child(3)::text").extract_first()

        if birth_place_info is None:
            birth_place_info = response.css(
                "#name-born-info a::text").extract_first()

        birth_place_info = birth_place_info.rsplit(
            ", ") if birth_place_info is not None else None

        birth_country = birth_place_info[-1] if birth_place_info is not None else "unknown"
        birth_city = birth_place_info[-2] if (birth_place_info and len(
            birth_place_info) > 1) else "unknown"

        item = {
            "aid": actor_id,
            "fname": name[0],
            "lname": name[1] if len(name) > 1 else " ",
            "birth_date": birth_date_obj.strftime("%Y-%m-%d") if birth_date_obj is not None else "none",
            "birth_country": birth_country,
            "birth_city": birth_city,
            "overall_rating": 0,
            "gender": gender
        }
        yield response.follow(
            url=f"{response.url.rsplit('?')[0]}bio?ref_=nm_ql_1", callback=self.parse_actor_description, meta={"item": item})

    def parse_actor_description(self, response):
        item = response.meta["item"]
        description = response.css(".soda.odd p::text").extract_first()
        item["description"] = description.strip()

        yield item
