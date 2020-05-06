import json
import os
import random

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import dateparser

BASE_URL = 'http://www.forumtopics.com/busobj/'
BASE_DIR = './scrapped_data'

visited = {}
import re

# Scrapper for the forums. Will take the posts one by one and, for each of them, will create a folder and store
# inside a json with all the interpreted data, as well as all the html that have been visited (possibly more than 1)
# if the post has many pages of comments

class Comment:
    def __init__(self, author, date, content):
        self.author = author
        self.date = date
        self.content = content
    def toJson(self):
        return {
            "date": str(self.date),
            "content": self.content,
            "author": self.author,
        }

class Post:
    def __init__(self, id, title, author, content, date, comments=[]):
        self.id = id
        self.title = title
        self.author = author
        self.content = content
        self.date = date
        self.comments = comments

    def toJson(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "date": str(self.date),
            "comments": [comment.toJson() for comment in self.comments],
        }

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

class TestSpider(scrapy.Spider):
    name = "test"
    posts = []
    start_urls = [
       "http://www.forumtopics.com/busobj/viewtopic.php?t=" + str(number) for number in range(1, 256191)
    ]
    custom_settings = {
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 6
    }
    random.shuffle(start_urls)
    def parse(self, response):
        # Find out post number (id)
        try:
            match = re.search(r't=(\d*)', response.url)
            post_number = match.group(1)
        except Exception as e:
            print(response.url)
            print(e)

        folder_path = "download/" + str(post_number)

        # Keep track of all the visited pages
        if (post_number not in visited):
            visited[post_number] = {
                "comments": [],
                "n_pages": 0
            }

        not_found = Selector(response).xpath("//table[@class='forumline']//td[@class='row1']/table/tr[2]/td/span[@class='gen']").extract()
        if len(not_found) > 0:
            print("ERROR PAGE")
            return

        # Create folder if doesn't exist
        try:
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
        except Exception as e:
            print(e)

        # Save page N of the current post id
        with open(folder_path + "/" + str(visited[post_number]['n_pages']) + ".html", "wb") as f:
            f.write(response.body)

        # Start scrapping of data
        row = Selector(response).xpath("//table[@class ='forumline']/tr").extract()
        title = Selector(response).xpath("///a[@class ='maintitle']/text()").get()
        next_page = Selector(response).xpath("//span[@class='nav']//a[contains(text(),'Next')]/@href")

        for item in row[2:]:
            author_1 = Selector(text=item).xpath("//td[1]//b/span/text()").get()
            author_2 = Selector(text=item).xpath("//td[1]//b/text()").get()
            author = author_1 if author_1 is not None else author_2
            if author:
                date_text = Selector(text=item).xpath("//td[2]/table//span[@class='postdetails']/text()").get().replace("Posted: ", "").strip()
                comment_content = Selector(text=item).xpath("//td[2]/table/tr[3]/td").get()
                visited[post_number]['comments'].append(Comment(author, dateparser.parse(date_text), comment_content))

        # If has more comment pages, queue them up to be visited
        if(len(next_page) > 0):
            visited[post_number]['n_pages'] += 1
            next_page_url = BASE_URL + next_page.get()
            yield scrapy.Request(next_page_url, callback=self.parse)

        # For the last page, store the accumulated json in a file and delete the content of comments to not clog RAM
        else:
            post = visited[post_number]['comments'][0]
            new_post = Post(post_number, title, post.author, post.content, post.date, visited[post_number]['comments'][1:])
            with open(folder_path + "/items.json", "w") as f:
                f.write(json.dumps(new_post.toJson()))
            del visited[post_number]['comments']

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

process.crawl(TestSpider)
process.start()
