# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import datetime
from unidecode import unidecode
from dateutil.parser import parse
import pandas as pd

BASE_URL = 'https://www.google.com/flights/explore/'


# add wait method to actionchains class
# http://stackoverflow.com/questions/36572190/specify-wait-time-between-actions-when-using-selenium-actionchains
class ActionChains(ActionChains):
    def wait(self, time_s):
        self._actions.append(lambda: time.sleep(time_s))
        return self


# helper function
def setup(start_date, from_place, to_place,city_name):
    """
    used for initializing the start_date and typing from_place, to_place into the search box.

    :param start_date:
    this is a datetime object for the start date that you should use in your query to Google
    Flight explorer.

    :param from_place:
    this is a string with the name of the origin of the flights

    :param to_place:
    this is a string with the name of the regional destination of the flights, e.g. India, South America,
    Scandinavia This is what would be typed into the To field on the Flight Explorer page.

    :param city_name:
    this is a string for the name of the city who's data that you should actually scrape, e.g. Ålesund.

    :return:
    selenium driver, and the index of the target city
    """
    # modify date
    start_date = start_date.strftime('%Y-%m-%d')
    URL = BASE_URL + '#explore;d=' + start_date
    driver = webdriver.Chrome('./chromedriver')
    driver.get(URL)

    time.sleep(5)

    # input from place
    driver.find_elements_by_css_selector('.LJTSM3-p-a')[0].click()
    ActionChains(driver).wait(2).send_keys(from_place).perform()
    ActionChains(driver).wait(2).send_keys(Keys.ENTER).perform()
    # input to place
    driver.find_elements_by_css_selector('.LJTSM3-p-a')[1].click()
    ActionChains(driver).wait(2).send_keys(to_place).perform()
    ActionChains(driver).wait(2).send_keys(Keys.ENTER).perform()

    time.sleep(4)

    # find the location of target city
    cities = driver.find_elements_by_css_selector('.LJTSM3-v-c')
    city_names = [unidecode(n.text) for n in cities]
    n_th = None
    for i, name in enumerate(city_names):
        if city_name.lower() in name.lower():
            n_th = i

    return driver, n_th


# Task #1
def scrape_data(start_date, from_place, to_place, city_name):
    """
    :param start_date: same as above
    :param from_place: same as above
    :param to_place: same as above
    :param city_name: same as above
    :return: a dataframe with 60 rows and with two columns "Date_of_Flight" and "Price."
    """
    driver, n_th = setup(start_date, from_place, to_place,city_name)

    target = driver.find_elements_by_class_name('LJTSM3-v-d')[n_th]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    prices = []
    dates = []
    for bar in bars:
        ActionChains(driver).wait(0.01).move_to_element(bar).perform()
        price = driver.find_element_by_class_name('LJTSM3-w-w').text.replace('$','')
        date = driver.find_element_by_class_name('LJTSM3-w-h').text
        prices.append(price)
        dates.append(date)
    df = pd.DataFrame({'Date_of_Flight':dates,'Price':prices})
    driver.quit()
    return df


# Task #2
def scrape_data_90(start_date, from_place, to_place, city_name):
    """
    :param start_date: same as above
    :param from_place: same as above
    :param to_place: same as above
    :param city_name: same as above
    :return: a dataframe with 90 rows and with two columns "Date_of_Flight" and "Price."
    """
    driver,n_th = setup(start_date, from_place, to_place,city_name)

    target = driver.find_elements_by_class_name('LJTSM3-v-d')[n_th]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    prices = []
    dates = []
    for bar in bars:
        ActionChains(driver).wait(0.01).move_to_element(bar).perform()
        price = driver.find_element_by_class_name('LJTSM3-w-w').text.replace('$','')
        date = driver.find_element_by_class_name('LJTSM3-w-h').text
        prices.append(price)
        dates.append(date)

    time.sleep(3)
    driver.find_elements_by_class_name('LJTSM3-w-D')[0].click()
    time.sleep(3)
    driver.find_elements_by_class_name('LJTSM3-w-D')[0].click()
    time.sleep(3)

    target = driver.find_elements_by_class_name('LJTSM3-v-d')[n_th]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    for bar in bars[:30]:
        ActionChains(driver).wait(0.01).move_to_element(bar).perform()
        price = driver.find_element_by_class_name('LJTSM3-w-w').text.replace('$','')
        date = driver.find_element_by_class_name('LJTSM3-w-h').text
        prices.append(price)
        dates.append(date)
    df = pd.DataFrame({'Date_of_Flight':dates,'Price':prices})
    driver.quit()
    return df

# Task #3
def task_3_dbscan(flight_data):
    im


if __name__ == '__main__':
    scrape_data_90(datetime.datetime.now(),'london','norway','bergen')
