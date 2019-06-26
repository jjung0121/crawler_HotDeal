from bs4 import BeautifulSoup
import requests
from datetime import datetime
# from Detail_info import Detail_info

class Sale_info:

    # < 날짜 및 시간 >
    # now = datetime.now()
    today = datetime.today().strftime("%Y-%m-%d")
    now = datetime.today().strftime("%H:%M:%S")
    
    def __init__(self, tag):
        self.title = self.get_text(tag, 'div.info_box > p')
        self.view = self.get_text(tag,'span.cnt_box > span.cnt_lft > span.cnt_rgt > span.cnt_mid > em.cnt')
        self.pageURL = self.get_attr(tag,'a[href]', 'href') 
        self.detail_info= self.get_detail(self.pageURL)

    def get_attr(self, parent_tag, selector, attr_name):
        tag = self.get_tag(parent_tag, selector)
        if tag != None:
            return tag.get(attr_name).strip()
        else:
            return ""

    def get_text(self, parent_tag, selector):
        tag = self.get_tag(parent_tag, selector)
        return tag.text.strip().replace(",","")

    def get_tag(self, parent_tag, selector):
        tag = parent_tag.select(selector)
        if tag == None or len(tag) == 0:
            return None
        else:
            return tag[0]

    detail = ''
    def get_detail(self, pageURL):

        url = self.pageURL
        response = requests.get(url)

        html = BeautifulSoup(response.text, 'html.parser')
        product_info = html.select_one('#wrap')        
        detail = Detail_info(product_info)
        return detail

    def __str__(self):
        return self.to_str()
        
    def to_str(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t".format(self.today, self.now, self.title,self.view,self.detail_info,self.pageURL)


class Detail_info(Sale_info):

    def __init__(self, tag):

        # < 상품번호 >
        self.product_num = self.get_text(tag, 'p > span.thm')
        # < 상품명 >
        self.product_name = self.get_text(tag, 'dl > dt > strong')
        # < 정가 > 
        self.original_price = self.get_text(tag, 'dd:nth-child(2) > p > strong > span.thm')
        # < 할인가 > 
        self.sale_price = self.get_text(tag, 'dd:nth-child(4) > p > strong > span.thm')
        # < 배송방법 >
        self.delivery_type = self.get_text(tag, 'li.odd > input[type=hidden]')
        # < 배송비 >
        self.delivery_fee = self.get_text(tag, 'li._deliveryBaseFeeArea.odd2 > span._deliveryBaseFeeAreaValue.ag')
        # < 리뷰 수 >
        self.reviews_num = self.get_text(tag, 'span > a > strong.num')
        # < 리뷰 평점 >
        self.reviews_score = self.get_text(tag, 'span.wrap_label > strong')

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(self.product_num, self.product_name, 
                                                        self.original_price, self.sale_price,
                                                        self.delivery_type, self.delivery_fee, 
                                                        self.reviews_num, self.reviews_score)

