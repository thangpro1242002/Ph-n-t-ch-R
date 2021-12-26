# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Tên sản phẩm
    name = scrapy.Field()
    # Danh mục
    # tag = scrapy.Field()
    # Giá gốc
    price = scrapy.Field()
    # Hạ giá
    discount = scrapy.Field()
    # Giá sau khi giảm
    new_price = scrapy.Field()
    #  Thương hiệu
    brand = scrapy.Field()
    # Đánh giá tích cực
    positive_rating = scrapy.Field()
    # Giao đúng hạn
    delivered_on_time = scrapy.Field()
    # Tỷ lệ phản hồi
    response_rate = scrapy.Field()
