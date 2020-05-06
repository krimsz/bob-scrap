import json

from elasticsearch import Elasticsearch
import os

JSON_BASE_PATH='./json_posts'
es = Elasticsearch()

# In order to process all the json files, this file assumes that the json files have been downloaded in a folder
# where each file has as name the post id and .json extension.

# es.indices.delete(index="test-index")

posts = os.walk(JSON_BASE_PATH).__next__()[2]
for index, post_id in enumerate(posts):
    with open(JSON_BASE_PATH + str(post_id)) as f:
        res = es.index(index="bob-index", id=post_id, body=json.loads(f.read()))
    if index % 1000 == 0:
        print(index)
        es.indices.refresh(index="bob-index")
