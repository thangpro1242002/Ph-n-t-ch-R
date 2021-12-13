import scrapy
from ..items import Trip1Item
from selenium import webdriver
from scrapy.utils.project import get_project_settings
import os



class Trip1spiderSpider(scrapy.Spider):
    name = 'trip1spider'
    #allowed_domains = ['tripadvisor.com.vn']
    def start_requests(self):
        url = ['https://www.tripadvisor.com/Hotels-g298085-Da_Nang-Hotels.html']
                

            
        for item in url:
            settings= get_project_settings()
            driver_path = "C:\\Users\\Admin\\trip1\\trip1\\chromedriver.exe"
            options= webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(driver_path, options=options)
            driver.get(item)
            link_elements = driver.find_elements_by_xpath(
                 "//div[@class=' photo-wrapper ']/a"
            )
            for link in link_elements:
                yield scrapy.Request(link.get_attribute('href'), callback=self.parse)
            driver.quit()
    
    
                
    

    def parse(self, response):
        hotel_name=response.xpath('//h1[@class="fkWsC b d Pn"]/text()').get()
        rank = response.xpath('//b[@class="rank"]/text()').get()
        address = response.xpath('//span[@class="ceIOZ yYjkv"]/text()').get()
        review = response.xpath('//div[@class="cNJsa"]/text()').get()
        
        #<span class="bpwqy VyMdE">105</span>
        restaurant_nearby = response.xpath('//span[@class="bpwqy VyMdE"]/text()').get()
        #<span class="bpwqy dfNPK">93</span>
        GFW = response.xpath('//span[@class="bpwqy dfNPK"]/text()').get()
        #<span class="bpwqy eKwbS">14</span>
        Attractions = response.xpath('//span[@class="bpwqy eKwbS"]/text()').get()
        #<span class="btQSs q Wi z Wc">2,509 reviews</span>
        review_number = response.xpath('//span[@class="btQSs q Wi z Wc"]/text()').get()
        #<div class="ui_column  is-3-tablet is-shown-at-tablet "><div class="cMImN b S4 H4">Language</div><ul class="mPill w S4"><li class="ui_radio dQNlC"><input id="LanguageFilter_0" type="radio" value=""><label for="LanguageFilter_0" class="bahwx Vm _S"><span class="fwSIg q">All languages</span><span class="cvxmR">(2,509)</span></label></li><li class="ui_radio dQNlC"><input id="LanguageFilter_1" type="radio" value="en" checked=""><label for="LanguageFilter_1" class="bahwx Vm _S"><span class="fwSIg q">English</span><span class="cvxmR">(1,905)</span></label></li><li class="ui_radio dQNlC"><input id="LanguageFilter_2" type="radio" value="fr"><label for="LanguageFilter_2" class="bahwx Vm _S"><span class="fwSIg q">French</span><span class="cvxmR">(224)</span></label></li><li class="ui_radio dQNlC"><input id="LanguageFilter_3" type="radio" value="de"><label for="LanguageFilter_3" class="bahwx Vm _S"><span class="fwSIg q">German</span><span class="cvxmR">(111)</span></label></li><div class="dbKhu b _S"><span class="text">More</span></div></ul></div>
        languages = response.xpath('//span[@class="fwSIg q"]/text()').getall()
        #<label for="TravelTypeFilter_0" class="Oixff Vm _S">Families</label>
        traveltype = response.xpath('//label[contains(@for, "TravelTypeFilter")]/text()').getall()
        #<div class="cJdpk Ci">₫340,909<!-- --> - <!-- -->₫590,909<!-- --> <!-- -->(Based on Average Rates for a Standard Room) </div>
        
        room = response.xpath('//div[@class="cJdpk Ci"]/text()')[-1].getall()
        ##<span class="cXdRV"> (48) </span>
        traveler_pic = response.xpath('//span[@class="cXdRV"]/text()')[0:3].getall()
        number_room_dining = response.xpath('//span[@class="cXdRV"]/text()')[-2].getall()
        number_room_suite = response.xpath('//span[@class="cXdRV"]/text()')[-5].getall()
        item = Trip1Item()
        item['hotel_name'] = hotel_name
        item['rank'] = rank
        item['address'] = address
        item['review'] = review
        item["Restaurant_nearby"] = restaurant_nearby
        item["number_images_Traveler"] = traveler_pic
        item["Review_number"] = review_number
        item["Great_for_walker"] = GFW
        item["Attractions"] = Attractions
        item["languages"] = languages
        item["Travel_types"] = traveltype
        
        item["Room_number"] = room
        item["number_room_suite"] = number_room_suite
        item["number_room_dining"] = number_room_dining
        yield item
        pass
