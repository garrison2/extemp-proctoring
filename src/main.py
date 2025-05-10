from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.common.exceptions import *

import re 
import csv
import sys

def open_pairings(driver):
    pairings_button = driver.find_element(By.LINK_TEXT, 'Pairings')
    pairings_button.click()

def open_event(driver, event):
    dropdown = driver.find_element(By.CSS_SELECTOR,
                                  'div[class="even full centeralign"]')
    dropdown.click()
    pass

def open_user_input_event(driver, event_url):
    driver.get(event_url)
    pass

def get_table(driver):
    return driver.find_element(By.CSS_SELECTOR, 'tbody')

def get_rooms(table, event_name):
    rooms_list = []
    rooms = table.find_elements(By.CSS_SELECTOR, 'tr[role="row"]')
    for room in rooms:
        room_name = room.find_element(By.CSS_SELECTOR, 'td[class="smallish nospace padless"]').text
        names_list = []

        names = room.find_elements(By.CSS_SELECTOR, 'span')
        for name in names:
            names_list.append(re.match(r'.+ – (.+\S)', name.text).group(1))

        rooms_list.append((event_name, room_name, names_list))

    return rooms_list

def print_to_csv(rooms_list, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for room in rooms_list:
            row = list(room[0:2]) + room[2]
            writer.writerow(row)


def main():
    #    url = input('Enter the tournament page url: ')
    #    url = 'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id=35068&round_id=1321201'

    #    driver.get(url)

    # open_user_input_event(driver, 'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id=35068&round_id=1321225')

    if len(sys.argv) > 1:
        if len(sys.argv) < 4:
            raise Exception('Invalid number of arguments.')

        ix_url = sys.argv[1]
        nx_url = sys.argv[2]
        output_file = sys.argv[3]
    else:
        ix_url = input('Enter the IX url: ')
        nx_url = input('Enter the NX url: ')

        output_file = input('Enter the output filepath: ')

    driver = webdriver.Firefox()
    rooms_list = []

    open_user_input_event(driver, ix_url)
    table = get_table(driver)
    rooms_list += get_rooms(table, 'IX')

    open_user_input_event(driver, nx_url)
    table = get_table(driver)
    rooms_list += get_rooms(table, 'NX')

    print_to_csv(rooms_list, output_file)

if __name__ == '__main__':
    main()
