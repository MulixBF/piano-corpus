from datetime import datetime

BOT_NAME = 'src'

LOG_FILE = 'logs/log_{:%Y%m%d_%H%M%S}.txt'.format(datetime.now())
SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'
ROBOTSTXT_OBEY = False
FILES_STORE = 'data'
ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}