# -*- coding: utf-8 -*-
import scrapy


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = []
    for i in range(1, 677):
        url_pre = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,"
        url_end = ".html?"
        url = url_pre + str(i) + url_end
        start_urls.append(url)

    def parse(self, response):
        networks = response.xpath("//div[@class='el']/p[contains(@class,'t1')]/span/a/@href").extract()
        for network in networks:
            # 详情页网址
            if network:
                # 进入详情页
                yield scrapy.Request(network, callback=self.detail)

    def detail(self, response):
        # 用来处理详情页的数据
        company = response.xpath("//p[@class='cname']/a/@title").extract()
        # 1.公司名称
        title = response.xpath("//div[@class='cn']/h1/text()").extract()
        # 2.职位
        salary = response.xpath("//div[@class='cn']/strong/text()").extract()
        # 3.工资
        location = response.xpath("//p[@class='msg ltype']/text()").extract()[0]
        # 4.地点
        experience = response.xpath("//p[@class='msg ltype']/text()").extract()[1]
        # 5.工作经验
        education = response.xpath("//p[@class='msg ltype']/text()").extract()[2]
        # 6.学历   有的公司格式不一样，全部提取完再用正则表达式处理
        company_type = response.xpath("//div[@class='com_tag']/p[1]/@title").extract()
        # 7.公司类型
        company_size = response.xpath('//div[@class="com_tag"]/p[2]/@title').extract()
        # 8。公司规模
        field = response.xpath('//div[@class="com_tag"]/p[3]/@title').extract()
        # 9.所属行业
        describe = response.xpath("//div[@class='bmsg job_msg inbox']/p/text()").extract()
        # 10.职位描述
        items = {
            '公司': company,
            '职位': title,
            '工资': salary,
            '工作地点': location,
            '工作经验': experience,
            '学历': education,
            '公司类型': company_type,
            '公司规模': company_size,
            '行业': field,
            '岗位描述': describe
        }
        yield items
