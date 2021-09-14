import csv
import json

# import requests
from bs4 import BeautifulSoup
from selenium import webdriver

BASE_URL = ''
import time

PAGES_COUNT = 1
OUT_FILENAME = 'outs.json'


def get_html(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver.page_source


def get_soup(url):
    soup = BeautifulSoup(get_html(url), features='html.parser')
    return soup


def crawl_products(pages_count):
    fmt = 'https://www.fiverr.com/categories/online-marketing/web-analytics-services/setup?source=pagination&page={page}&offset=-2'
    result_saver = []
    for page_n in range(1, 1 + pages_count):
        try:
            print('page: {}'.format(page_n))
            page_url = fmt.format(page=page_n)
            print('Страница перехода: ', page_url)
            soup = get_soup(page_url)
            cards = soup.find_all('div', class_='gig-card-layout')
            time.sleep(2)
            for card in soup.find_all('a', class_='media'):
                save = card['href']
                print(save)
                result_saver.append(save)
        except:
            continue
        if soup is None:
            break
    return result_saver


def parse_products(urls):
    data = []

    #for url in urls:
    for url in urls[0]:
        # print('product: {}'.format(url))

        soup = get_soup('https://www.fiverr.com/' + url)
        print('https://www.fiverr.com' + url)
        if soup is None:
            break
        headline = soup.select_one('h1', class_='text-display-3').text.strip()
        name = soup.select_one('a', class_='seller-link').text.strip()
        # avg_resp_time = soup.find_all('ul', class_='user-stats')
        ul_tag = soup.find_all('ul', class_='user-stats')

        for li_tag in ul_tag:
            newsoup = BeautifulSoup(str(li_tag), 'html.parser')
            strong_tags = newsoup.find_all('strong')
            last_dilivery = str(strong_tags[3])
            avg_resp_time = str(strong_tags[2])
            member_since = str(strong_tags[1])
            country = str(strong_tags[0])

        number_of_reviews = soup.select_one('span', class_='review-header-total-count').text.strip()
        services_type = soup.select_one('b', class_='title').text.strip()
        services = soup.find('div', class_='package-content').select_one('p')
        about_us = soup.find('div', class_='description-content').findChildren()

        price = soup.find('span', class_='price').text.strip()
        link = 'https://www.fiverr.com/' + url

        item = {
            'headline': headline,
            'user': name,
            'avg_resp_time': avg_resp_time.replace('<strong>', '').replace('</strong>', ''),
            'last_dilivery': last_dilivery.replace('<strong>', '').replace('</strong>', ''),
            'member_since': member_since.replace('<strong>', '').replace('</strong>', ''),
            'country': country.replace('<strong>', '').replace('</strong>', ''),
            'number_of_reviews': number_of_reviews,
            'services_type': services_type,
            'services': services,
            'about_us': str(about_us).replace('<p><strong>', '').replace('</strong></p>', ''),
            'price': price,
            'link': link,
        }
        print(item)
        data.append(item)
        time.sleep(2)

    return data


def save_file(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(
            ['headline', 'user', 'avg_resp_time', 'last_dilivery', 'member_since', 'country', 'number_of_reviews',
             'services_type', 'services', 'about_us', 'price', 'link'])
        for item in items:
            writer.writerow(
                [item['headline'], item['user'], item['avg_resp_time'], item['last_dilivery'], item['member_since'],
                 item['number_of_reviews'], item['services_type'], item['services'], item['about_us'], item['price'],
                 item['link']])


def main():
    urls = crawl_products(PAGES_COUNT)
    print(urls)
    data = parse_products(urls)
    print(data)

    save_file(data)


if __name__ == '__main__':
    main()
