from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import os
import re
from lxml import etree
import random
from pyquery import PyQuery as pq
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)


class downIamge(object):
    # ================================== 抓取多页数据 ==================================
    def parseMultiplePages(self, url, page, page_num):
        self.page = page
        self.page_num = page_num
        self.hread = {
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://manhua.fzdm.com/2/' + str(self.page) + '//index_' + str(self.page_num) + '.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'

        }
        try:
            wb_data = requests.session().get(url, headers=self.hread, verify=False)
            if wb_data.status_code == 200:
                # print(wb_data.content)
                soup = BeautifulSoup(wb_data.text, 'lxml')
                # for child in soup.descendants:
                title = soup.find_all('script', type='text/javascript')
                # print(title[1])
                for name in title[1]:
                    mhurl = list(tuple(str(name).split(";")))
                    self.new_mhurl = list(tuple(str(mhurl[2]).split("=")))
                    # imageUrl="http://p17.xiaoshidi.net/"+new_mhurl
                    # print(new_mhurl[1])
                #         namelist = list(tuple(str(title).split("=",":")))

            else:
                print("超过访问限制")

        # imgs = soup.select('div#mh > div#pjax-container>div#mhimg0> a > img')

        # for img in imgs:
        #     data = {
        #         'img': img.get('src')
        #     }
        #     print(data)
        #     # onepiece_pic.insert_one(data)
        #     img_urls.append(data['img'])
        # # print('img_urls is a list as:', img_urls)
        # return img_urls

        except:
            for page_num in range(0, 18):
                url = 'http://manhua.fzdm.com/2/{}/index_{}.html'.format(935, page_num)

                parseMultiplePages(url, 935, page_num)

    def downImage(self):
        path = "海贼王/" + str(self.page)
        url = re.sub('"', '', str(self.new_mhurl[1]))
        imageUrl = "http://p17.xiaoshidi.net/" + url
        print(imageUrl)
        wb_data = requests.session().get(imageUrl, headers=self.hread, verify=False)

        if not os.path.exists(path):
            os.mkdir("海贼王/" + str(self.page))
        else:
            with open(path + '/{}.jpg'.format(self.page_num), 'wb')as f:
                f.write(wb_data.content)

    def getNumber(self):
        self.hread = {
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://manhua.fzdm.com/2/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'

        }
        #
        url = 'https://manhua.fzdm.com/2/'
        rep_data = requests.get(url, headers=self.hread, verify=False).text
        doc = pq(rep_data)
        data = doc('.pure-g  li a').items()
        thisset = list()

        for title in data:
            t = title.attr('href')
            thisset.append(t)
            # print(thisset)

        return thisset[3:7]
        # for tt in title:
        #
        #     print(tt)


if __name__ == '__main__':
    # dl_chapters(935,938)
    dwon = downIamge()
    number = dwon.getNumber()
    for page in number:
        # print(page)
        for page_num in range(0, 20):
            url = 'http://manhua.fzdm.com/2/{}index_{}.html'.format(page, page_num)
            print(url)
            dwon.parseMultiplePages(url, page, page_num)
            dwon.downImage()
