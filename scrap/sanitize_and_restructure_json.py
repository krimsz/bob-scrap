import json
import os
import re

SCRAPPER_DOWNLOAD_DIR = './scrapped_data'
SANITIZED_DATA_DIR = './json_posts'

# This script has as aim, take the result of the scraping and for each item, add an extra field 'sanitized_content' for
# both the post and each comment. This sanitized content is basically the normal content without the tags so that can be
# easily indexed by elasticsearch. this could have been done in the first place from the scrapper itself as well

# Besides adding this extra field, also works as an aggregator because will go through each folder and copy the json files
# in a structure that works with the "insert_elasticsearch.py" script

def striphtml(data):
    p = re.compile(r'<.*?>')
    stripped_html = p.sub('', data)
    stripped_html = stripped_html.replace('\r', '')
    stripped_html = stripped_html.replace('\n', '')
    return stripped_html

posts = os.walk(SCRAPPER_DOWNLOAD_DIR).__next__()[1]
total_posts = len(posts)
for index, post_id in enumerate(posts):
    if index % 1000 == 0:
        print(str(index) + "/" + str(total_posts))
    with open(SCRAPPER_DOWNLOAD_DIR + str(post_id) + "/items.json", 'r') as f:
        post_content = json.loads(f.read())
        post_content['sanitized_content'] = striphtml(post_content['content'])
        for index, comment in enumerate(post_content['comments']):
            post_content['comments'][index]['sanitized_content'] = striphtml(post_content['comments'][index]['content'])
        with open(SANITIZED_DATA_DIR + '/' + str(post_id) + ".json", 'w') as fw:
            fw.write(json.dumps(post_content))

