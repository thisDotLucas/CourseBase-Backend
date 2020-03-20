from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random

all_courses = {}


def scrape_studiehandboken():
    base_url = "https://studiehandboken.abo.fi"
    extensions = ["/en/degree-programme/3472", "/en/degree-programme/5071", "/en/degree-programme/4349",
                  "/en/degree-programme/4653", "/en/degree-programme/11294", "/en/degree-programme/8574"]

    for extension in extensions:
        soup = create_soup(base_url + extension)

        courses = soup.findAll("div", {"class": "programme-item-elem course-unit-item"})

        for course in courses[:int(len(courses) / 2)]:
            course = course.find("a")
            if " 4" not in course.text:  # Get rid of language courses
                all_courses[course.text] = base_url + course["href"]


def scrape_utu():
    base_url = "https://opas.peppi.utu.fi/"
    extensions = ["en/degree-programme/4247", "/en/degree-programme/4259", "/en/degree-programme/13196",
                  "/en/degree-programme/3305", "/en/degree-programme/9309"]

    for extension in extensions:
        soup = create_soup(base_url + extension)

        courses = soup.findAll("div", {"class": "programme-item-elem course-unit-item"})

        for course in courses[:int(len(courses) / 2)]:
            course = course.find("a")
            all_courses[course.text] = base_url + course["href"]


def create_soup(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('window-size=1920x1080');
    driver = webdriver.Chrome("C:/Users/Lucas/Downloads/chromedriver_win32/chromedriver.exe", options=chrome_options)
    driver.get(url)
    time.sleep(random.randint(2, 6))
    page = driver.page_source

    return BeautifulSoup(page, "html.parser")


def get_courses():
    scrape_studiehandboken()
    scrape_utu()
    return all_courses


