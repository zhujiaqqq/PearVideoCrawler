import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CHANNEL_MAP = {
    'KNOWLEDGE': 'category_10',
    'CHINA': 'category_1',
    'WORLD': 'category_2',
    'SPORTS': 'category_9',
    'LIFE': 'category_5',
    'TECH': 'category_8',
    'ENTERTAINMENT': 'category_4',
    'FINANCE': 'category_3',
    'AUTO': 'category_31',
    'TASTE': 'category_6',
    'MUSIC': 'category_59',
}


class PearCrawler:
    def __init__(self):
        self.base_url = 'https://www.pearvideo.com/'
        self.browser = webdriver.Chrome()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

    pass



