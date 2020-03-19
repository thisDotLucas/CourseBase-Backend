import dataScrape
import datetime
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

current_year = datetime.date.today().year
next_year = current_year + 1
course_info = {}


def run():
    courses = dataScrape.get_courses()

    for key in courses.keys():

        soup = dataScrape.create_soup(courses[key])

        if len(soup.find_all("div", {"class": "collapsible-header"})) == 0:# No course coming up.
            continue
        else:
            try:
                soup = create_soup(courses[key])
            except NoSuchElementException:
                continue

            divs = soup.find_all("div")

            for div in divs:
                if div.text[0:8] == "Teaching" and (str(current_year) in div.text or str(next_year) in div.text):
                    text = div.text[11:-10]
                    times = text.split("  ")
                    timestamps = []

                    for string in times:
                        timestamps.append(string[4:26])

                    data = {"url": courses[key], "timestamps": timestamps, "period": get_period(int(timestamps[0][3:5]))}
                    course_info[key] = data

                    print(key)
                    print(course_info[key]["url"])
                    print(course_info[key]["timestamps"])
                    print("Period " + course_info[key]["period"])
                    print("-" * 80)

                    break
    return course_info


def get_period(month):
    if month < 2:
        return 3
    elif month < 5:
        return 4
    elif month < 10:
        return 1
    else:
        return 2


def create_soup(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('window-size=1920x1080');
    driver = webdriver.Chrome("C:/Users/Lucas/Downloads/chromedriver_win32/chromedriver.exe", options=chrome_options)
    driver.get(url)

    time.sleep(1)
    course_box = driver.find_element_by_class_name("collapsible-header")
    course_box.click()

    time.sleep(1)
    show_more_link = driver.find_element_by_link_text("Show more")
    show_more_link.click()

    time.sleep(random.randint(2, 6))
    page = driver.page_source

    return BeautifulSoup(page, "html.parser")


