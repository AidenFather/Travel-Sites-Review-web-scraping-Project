from scrapy import Spider, Request
from consumeraffairs.items import ConsumeraffairsItem

class ConsumeraffairsSpider(Spider):
    name = 'consumeraffairs_spider'
    allowed_urls = ['https://www.consumeraffairs.com/']
    start_urls = ['https://www.consumeraffairs.com/travel/travel-sites/#travel-site-features']
       
    
    
    def parse (self, response):

        site_urls =  response.xpath('//td[@class = "brd-card__tit brd-card__td"]/a/@href').extract()

        for url in site_urls:
            yield Request(url = url, callback = self.parse_review_page)

   
    def parse_review_page(self, response):
        
        # Find all the review tags
        reviews = response.xpath('//div[@class = "rvw js-rvw"]')
        site = response.xpath('//h1[@class ="prf-hr-tl__cpy-nm  "]/text()').extract_first()

        # Extract each field from the review tag
        for review in reviews:
            
            user = review.xpath('.//div[@class = "rvw-aut__inf"]/strong[1]/text()').extract_first()
            rating = review.xpath('.//img[@class ="stars-rtg stars-rtg--sm"]/@data-rating').extract_first()
            review_date = review.xpath('.//span[@class = "ca-txt-cpt ca-txt--clr-gray"]/text()').extract_first()
            text = review.xpath('.//div[@class = "rvw-bd ca-txt-bd-2"]/p[2]/text()').extract_first()

            try:
                verified_reviewer = review.xpath('.//div[@class = "rvw-aut__inf"]/strong[2]/text()').extract_first()
            except IndexError:
                verified_reviewer = ""
            try:
                verified_buyer = review.xpath('.//div[@class = "rvw-aut__inf"]/strong[3]/text()').extract_first()
            except IndexError:
                verified_buyer = ""
            try:
                helpful = review.xpath('.//span[@class = "rvw-foot__helpful-count js-helpful-count ca-txt--clr-gray"]/strong/text()').extract_first()
            except IndexError:
                helpful = ""
                

            item = ConsumeraffairsItem()
            item['user'] = user
            item['rating'] = rating
            item['verified_reviewer'] = verified_reviewer
            item['verified_buyer'] = verified_buyer
            item['review_date'] = review_date
            item['text'] = text
            item['helpful'] = helpful
            item['site'] = site


            yield item

        


        #follow pagination link
        next_page_url = response.xpath('.//a[@class ="ca-a-md ca-a-uprcs ca-a-blk prf-pgr__nxt js-pager-next"]/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield Request(url = next_page_url, callback = self.parse_review_page)



