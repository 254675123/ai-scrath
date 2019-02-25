# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from settings import mongo_db_collection,mongo_db_name,mongo_host,mongo_port

class SinobookPipeline(object):


    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        collectionname = mongo_db_collection

        client = pymongo.MongoClient(host=host, port=port)
        db_client = client[dbname]
        self.collection_client = db_client[collectionname]


    def process_item(self, item, spider):
        data = dict(item)
        self.collection_client.insert(data)
        return item


def fileSaver(data_list, filepath = './out.txt'):

    fout = open(filepath, 'a')
    fout.write('\n'.join(data_list))

    fout.close()