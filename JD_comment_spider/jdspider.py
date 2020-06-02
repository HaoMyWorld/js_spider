import requests
from lxml import etree
import logging
from urllib.parse import quote
import json
from urllib.parse import urlencode
import time

class JDSpider:

    def __init__(self,categlory, n):  
        self.startUrl = "https://search.jd.com/Search?keyword=%s&enc=utf-8"%(quote(categlory))    
        self.endUrl = '&qrst=1&rt=1&stop=1&vt=2&stock=1&page='+str(n)+'&s='+str(1+(n-1)*30)+'&click=0&scrolling=y'
        self.commentBaseUrl = "https://sclub.jd.com/comment/productPageComments.action?"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        self.productsId = self.getId()
        self.comtype = {1:"nagetive",2:"medium",3:"positive"}
        self.categlory = categlory
        self.iplist = {
                    'http':[],
                    'https':[]
        }
    def getParamUrl(self,productid,page,score):
        params = {                    
            "productId": "%s"%(productid),
            "score": "%s"%(score),              
            "sortType": "5",
            "page": "%s"%(page),
            "pageSize": "10",
            "isShadowSku": "0",
            "rid": "0",
            "fold": "1"
        }
        url = self.commentBaseUrl+urlencode(params)
        return params,url


    def getHeaders(self,productid):            
        header = {"Referer": "https://item.jd.com/%s.html"%(productid),
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
                  }
        return header

    def getId(self):    
        cururl = self.startUrl + self.endUrl
        print(cururl)
        response = requests.get(cururl, headers = self.headers)
        if response.status_code != 200:
            logging.warning("状态码错误，爬虫连接异常！")
        html = etree.HTML(response.text)
        return html.xpath('//li[@class="gl-item"]/@data-sku')

    def getForePageId():

        pass

    def getBackPageId():

        pass

    def getData(self,maxPage,score,): 
        label_s = []
        url_s = []

        for j in range(len(self.productsId)):
            id = self.productsId[j]
            header = self.getHeaders(id)
            for i in range(1,maxPage+1):
                param,url = self.getParamUrl(id,i,score)
                print(">>>>>>>>>>>>>>>>第：%d 个生鲜，第 %d 页"%(j+1,i))
                try:
                    response = requests.get(url,headers = header,params=param)
                except Exception as e:
                    logging.warning(e)
                    break
                if response.status_code !=200:
                    logging.warning("状态码错误，爬虫连接异常")
                    continue
                time.sleep(2)    #设置时延
                if response.text=='':
                    logging.warning("未爬取到信息")
                    continue
                try:
                    res_json = json.loads(response.text)
                except Exception as e:
                    logging.warning(e)
                    continue
                if len((res_json['comments']))==0:
                    logging.warning("页面次数已到：%d,超出范围"%(i))
                    break
                logging.info("正在爬取%s %s 第 %d"%(self.categlory,self.comtype[score],i))
                for cdit in res_json['comments']:
                    if 'images' not in cdit.keys():
                        continue
                    if 'videos' not in cdit.keys():
                        continue
                    resolution_img_h = cdit['videos'][0]['videoHeight']
                    resolution_img_w = cdit['videos'][0]['videoWidth']
                    imagesinfo = cdit['images']
                    if len(imagesinfo)==0:
                        continue
                    urls = ['https:'+imginfo['imgUrl'].replace('s128x96_jfs', 's'+ str(resolution_img_w)+ 'x'+ str(resolution_img_h) + '_jfs') for imginfo in imagesinfo]
                    urls_str = ' '.join(urls)
                    cursku_id = cdit['referenceId']
                    # or (cdit['productColor']!='')
                    label = ('productColor' not in cdit.keys()) and cursku_id or (cursku_id + ' ' + cdit['productColor'])
                    if urls_str in url_s:
                        continue
                    url_s.append(urls_str)
                    label_s.append(label)
        savepath = './'+self.categlory+'_'+self.comtype[score]+'.csv'
        logging.warning("已爬取%d 条 %s 评价信息"%(len(label_s),self.comtype[score]))
        with open(savepath,'a+',encoding ='utf8') as f:
            for i in range(len(label_s)):
                f.write("%s\t%s\n"%(label_s[i],url_s[i]))
        logging.warning("数据已保存在 %s"%(savepath))



if __name__ =="__main__":
    list = ['生鲜']
    pagenum = 100 #每一类商品需要的页,每页60个商品，默认只能jd只显示100页
    goodCom = 2000 #每一商品需要的评论页数,每页10个评论，遇到超出的页码会自动跳出，所以设大点也没有关系。

    for item in list:
        for n in range(1,pagenum*2+1):
            spider = JDSpider(item,n)
            for onescor in range(3,4):
                spider.getData(goodCom,onescor)
                print('ok')
    print('ok')


