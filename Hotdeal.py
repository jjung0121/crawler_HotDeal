from bs4 import BeautifulSoup
import requests
from Sale_info import Sale_info

class Hotdeal():
    url = 'https://shopping.naver.com/hotdeal/p/index.nhn'
    response = requests.get(url)

    # html 읽음
    html = BeautifulSoup(response.text, 'html.parser')
    hotDeal_list = html.select('#timesale_wrap')
    # print(hotDeal_list)

    # < 외부 정보 가져오기 >
    sale = []
    def get_list(self):
        for i in self.hotDeal_list:
            Sale_list = i.select('li')
            count = 0
            for s in Sale_list:
                if (count < 3):
                    count += 1
                    self.sale.append(Sale_info(s))
            break

        # for i in self.sale:
        #     print(i)

    def write_csv(self):
        with open("hotDeal.csv", "w", encoding='utf-8') as file:
            file.write("일자\t시간\t상품명\t뷰 수\t상품번호\t내부 상품명\t정가\t할인가\t배송타입\t배송비\t리뷰 수\t리뷰 평점\tURL\n")
            for i in self.sale:
                file.write(str(i) + "\n")

    def read_csv(self):
        with open("hotDeal.csv", "r", encoding='utf-8') as file:
            print(file.read())
                        

hotdeal = Hotdeal()
hotdeal.get_list()
hotdeal.write_csv()
hotdeal.read_csv()

