import re
import requests
import shutil
import copy
import sys
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def get_girl_imgs(parsed_html):
    girl_imgs_tag = parsed_html.body.findAll('img', {'data-type': 'jpeg'})[: -2]
    girl_imgs = []
    for img in girl_imgs_tag:
        girl_imgs.append(img['data-src'])
    return girl_imgs

def get_girl_infos(parsed_html):
    info = parsed_html.body.find('div', {'id': 'js_content'})
    girl_infos = info.text.split('dicksoup')
    return girl_infos

def formalize_girl_infos(girl_infos):
    formal_girl_infos = copy.deepcopy(girl_infos)
    formal_girl_infos[0] = formal_girl_infos[0][16:]
    formal_girl_infos[0] = "-------" + formal_girl_infos[0]
    return formal_girl_infos

def download_img(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('img.jpeg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def save_girl_img_to_html(img_src, id, html_file):
    div_id = "<div style=\"width:800px;\">" + id + "</div>"
    html_file.write(div_id)
    html_file.write("\n")
    img = "<img height=\"400\" src=\"" + img_src + "\">"
    html_file.write(img)
    html_file.write("\n")
    html_file.write("<br><br><br><br>")
    html_file.write("\n")

def save_girls_to_html(img_srcs, infos):
    html_file = open("content.html", "a")
    # if (len(img_srcs) != len(infos)):
    #     raise ValueError("Not equal size for girl_imgs and girl_infos, girl_imgs: "
    #                      , len(img_srcs), "girl_infos: ", len(infos))
    girl_ids = []
    for girl_info in infos:
        girl_ids.append(girl_info[7: 11])

    for i in range(min(len(img_srcs), len(infos))):
        save_girl_img_to_html(img_srcs[i], infos[i], html_file)

url = 'http://mp.weixin.qq.com/s' \
      '?__biz=MzA3NDMwMTkzNg==&mid=2650440457&idx=1&sn=1a260f8d71e3ab0d11d820ed56d7b842' \
      '&chksm=870fcb96b078428015ee46e5cf6ac294879ccd8eb72e6e7523a0b7d3f70ade373a01ef334761' \
      '&mpshare=1&scene=1&srcid=1218877mbxp8q9wEPP2SGJdX#rd'


def get_article_content(url):
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.content)
    girl_imgs = get_girl_imgs(parsed_html)
    raw_girl_infos = get_girl_infos(parsed_html)
    girl_infos = formalize_girl_infos(raw_girl_infos)
    # if (len(girl_imgs) == len(girl_infos)):
    save_girls_to_html(girl_imgs, girl_infos)
    for formal_girl_info in girl_infos:
        print formal_girl_info


articles = open('articles', 'r')
for line in articles:
    print line
    get_article_content(line)