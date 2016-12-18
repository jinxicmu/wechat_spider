import re
import requests
import shutil
from BeautifulSoup import BeautifulSoup

url = 'http://mp.weixin.qq.com/s' \
      '?__biz=MzA3NDMwMTkzNg==&mid=2650440457&idx=1&sn=1a260f8d71e3ab0d11d820ed56d7b842' \
      '&chksm=870fcb96b078428015ee46e5cf6ac294879ccd8eb72e6e7523a0b7d3f70ade373a01ef334761' \
      '&mpshare=1&scene=1&srcid=1218877mbxp8q9wEPP2SGJdX#rd'
response = requests.get(url)

file = open("content.html", "w+")
file.write(response.content)

parsed_html = BeautifulSoup(response.content)
girl_imgs = parsed_html.body.findAll('img', {'data-type': 'jpeg'})[: -2]
for imgsc in girl_imgs:
    print imgsc['data-src']

info = parsed_html.body.find('div', {'id': 'js_content'})
girl_infos = info.text.split('dicksoup')
for girl_info in girl_infos[1 :]:
    print girl_info

if (len(girl_imgs) != len(girl_infos)):
    raise ValueError("Not equal size for girl_imgs and girl_infos, girl_imgs: "
                     , len(girl_imgs), "girl_infos: ", len(girl_infos))
