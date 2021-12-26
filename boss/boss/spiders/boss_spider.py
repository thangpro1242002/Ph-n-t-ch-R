import scrapy
from ..items import BossItem
from selenium import webdriver
from scrapy.utils.project import get_project_settings
class BossSpiderSpider(scrapy.Spider):
    name = 'boss_spider'
    def start_requests(self):
        url = ['https://www.lazada.vn/trang-phuc-nam/?page=1&sort=popularity&spm=a2o4n.home.cate_9.1.19056afeEMh8vP',
               'https://www.lazada.vn/trang-phuc-nam/?page=2&sort=popularity&spm=a2o4n.home.cate_9.1.19056afeEMh8vP',
               'https://www.lazada.vn/trang-phuc-nam/?page=3&sort=popularity&spm=a2o4n.home.cate_9.1.19056afeEMh8vP',
               'https://www.lazada.vn/trang-phuc-nam/?page=4&sort=popularity&spm=a2o4n.home.cate_9.1.19056afeEMh8vP']
        for item in url:
            settings= get_project_settings()
            driver_path = settings['CHROME_DRIVER_PATH']
            options= webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(driver_path, options=options)
            driver.get(item)
            link_elements = driver.find_elements_by_xpath(
                 '//*[@data-qa-locator="product-item"]//a[text()]'
            )
            for link in link_elements:
                yield scrapy.Request(link.get_attribute('href'), callback=self.parse)
            driver.quit()
    def parse(self, response):
        #<h1 class="pdp-mod-product-badge-title" data-spm-anchor-id="a2o4n.pdp_revamp.0.i1.28946dd67InIRs">Quần jean nam form ôm cao cấp ,full team mác, chất liệu jean , co giãn tốt ,hàng chuẩn shop (ảnh thật shop chụp ) DIỄM NHI SHOP KV015</h1>
        name = response.xpath('//h1[@class="pdp-mod-product-badge-title"]/text()').get()
        # <span class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs" data-spm-anchor-id="a2o4n.pdp_revamp.0.i2.28946dd67InIRs">160.000 ₫</span>
        new_price = response.xpath('//span[@class="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]//text()').getall()
        # <span class="pdp-product-price__discount" data-spm-anchor-id="a2o4n.pdp_revamp.0.i6.28946dd67InIRs">-46%</span>
        discount = response.xpath('//span[@class="pdp-product-price__discount"]//text()').getall()
        # <span class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs" data-spm-anchor-id="a2o4n.pdp_revamp.0.i2.28946dd67InIRs">160.000 ₫</span>
        price = response.xpath('//span[@class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs"]//text()').getall()
        # <span class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs" data-spm-anchor-id="a2o4n.pdp_revamp.0.i2.28946dd67InIRs">160.000 ₫</span>
        brand = response.xpath('//a[@class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link"]/text()').getall()
        #<div class="seller-info-value rating-positive " data-spm-anchor-id="a2o4n.pdp_revamp.seller.i3.28946dd67InIRs">94%</div>
        positive_rating =  response.xpath('//div[@class="seller-info-value rating-positive "]/text()').get()
        #<div style="color:" class="seller-info-value " data-spm-anchor-id="a2o4n.pdp_revamp.seller.i5.28946dd67InIRs">99%</div>
        delivered_on_time = response.xpath('//div[@class="info-content"][2]/div[2]/text()').get()
        #<div style="color:" class="seller-info-value " data-spm-anchor-id="a2o4n.pdp_revamp.seller.i7.28946dd67InIRs">99%</div>
        response_rate = response.xpath('//div[@class="info-content"][3]/div[2]/text()').get()
        item = BossItem()
        item["name"] = name
        item["new_price"] = new_price
        item["discount"] = discount
        item["price"] = price
        item["brand"] = brand
        item['positive_rating']=positive_rating
        item['delivered_on_time']=delivered_on_time
        item['response_rate']=response_rate
        yield item
