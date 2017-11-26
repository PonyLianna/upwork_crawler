from bs4 import BeautifulSoup
import requests
import psycopg2
import time
import random
import configuration as config


class Page:
    # information to start with
    # id - thing that correcting database
    # page - page thing
    # user_agent - making POST that simulates browser and hide our bot
    id = 0
    page = 1
    user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x8664) AppleWebKit/537.36 (KHTML like Gecko) " +
                                "Ubuntu Chromium/28.0.1500.52 Chrome/28.0.1500.52 Safari/537.36"}

    def __init__(self):
        # on initialisation create new WWW and start processing with our Class
        # parse_everything - supermethod
        print("Page: {0}".format(self.page))
        self.www = "https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/t/1/"
        self.parse_everything()

    def next_page(self):
        # next_page every page passed
        # print Page "N"
        self.page += 1
        self.www = "https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/t/1/?page=%s" % str(self.page)
        print("Page: {0}".format(self.page))

    def response(self):
        # answer from www
        print("Getting response for " + str(self.page))
        return requests.get(self.www, headers=self.user_agent)

    def soup(self, response):
        # souping this shit
        print("Getting soup for " + str(self.page))
        return BeautifulSoup(response.text, 'lxml')

    def find(self, soup):
        # with species
        # JOB, SALARY, DESCRIPTION, SKILLS
        print("Getting information for " + str(self.page))
        print(soup)
        headings = soup.findAll("a",  class_="job-title-link")
        budget = soup.findAll("span", {"itemprop": "baseSalary"})
        information = soup.findAll("div", class_="description")
        skills = soup.findAll("span", class_="js-skills skills")
        return zip(headings, information, budget, skills)

    def parsed_result(self, finded):
        print("Parsing for " + str(self.page))
        for i, (a, b, c, d) in enumerate(finded):
            self.id += 1
            # unpacking skills result
            tags = " ".join(i.text.strip() for i in d.findAll("a", class_="o-tag-skill"))
            print(a.text.strip(), b.text.strip().replace('\n', ' '), c.text.strip(), tags)
            result = (str(self.id), a.text.strip(), b.text.strip().replace('\n', ' '), c.text.strip(), tags)
            self.database_insert(result)

    def database_insert(self, data):
        # connecting with database
        print("Inserting for " + str(self.page))
        config_data = config.Configuration().output()
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(config_data[0],
                                config_data[1], config_data[2], config_data[3]))
        cursor = conn.cursor()
        print(data)
        cursor.execute('INSERT INTO jobs (id,job_name,description,salary,tags) VALUES (%s,%s, %s, %s, %s)',data)
        conn.commit()

    def parse_everything(self):
        # page can't be greater than 500
        # supermethod
        # new GET
        # sleeping for NOT getting captcha
        while self.page < 500:
            self.parsed_result(self.find(self.soup(self.response())))
            self.next_page()
            time.sleep(5 + random.randint(0, 9))


if __name__ == "__main__":
    Page()

