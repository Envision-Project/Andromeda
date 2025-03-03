#!/usr/bin/python

from queue import Queue
import sys

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from andromeda.parser import Parser


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]

class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH, initial_links=None):
        if initial_links is None:
            initial_links = INITIAL_LINKS

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        self.link_queue = Queue()
        for link in initial_links:
            self.link_queue.put(link)

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            link = self.link_queue.get()
            print(link)

            page = self.get(link)

            new_links, _ = self.parser.parse(link, page)
            for link in new_links:
                self.link_queue.put(link)
            print(self.link_queue.qsize())

            if self.link_queue.empty():
                sys.exit(0)

CRAWLER = Crawler()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
    CRAWLER.run()

cli.add_command(start)

if __name__ == '__main__':
    cli()
