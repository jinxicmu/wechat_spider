# !/usr/bin/python
# -*- coding: utf-8 -*-

""" How to get cookie? Apparently wechat is using a SSL authentication mechanism to ensure that only the wechat inner browser
can open the wechat subscriptions. I tried fiddler to decode the cookie used here, but failed since fiddler is giving me
error that cannot decode the SSL.
Then I upgrate Chrome to newest version 55.0.2883.95, open the wechat app on mac and open the subscriptions article.
Then click the additional Chrome icon from wechat inner browser. Boom! All articles loaded! Then I found that Chrome decode
the cookie used here and added them to the request header.
Having the cookie, things become much easier. Only need to compare the difference between urls when load different article list,
and we can change the frommsgid to set the start index of article. -- failed.
Finally get the whole webpage through chrome.
"""


import urllib2
from BeautifulSoup import BeautifulSoup

html_file = open("history.html", "r")
parsed_html = BeautifulSoup(html_file.read())
articles1 = parsed_html.body.findAll('div', {'class': 'msg_item news redirect'})
articles2 = parsed_html.body.findAll('div', {'class': 'msg_item multi_news'})

article_links = open("articles", "w+")
i = 1
for article in articles1:
    try:
        article_title = article.find('h4', {'class': 'msg_title'}).text
        article_title = article_title.encode('utf-8')
        if article_title.find(u'女生场'.encode('utf-8')) != -1:
            article_url = article.find('div', {'class': 'msg_cover'})['hrefs']
            print  i, article_title, article_url
            i = i + 1
            article_links.write(article_url)
            article_links.write("\n")
    except KeyError:
        pass

for article in articles2:
    try:
        article_title = article.find('h4', {'class': 'msg_title'}).text.encode('utf-8')
        article_url = article.find('h4', {'class': 'msg_title'})['hrefs']
        if article_title.find(u'女生场'.encode('utf-8')) != -1:
            print i, article_title, article_url
            i = i + 1
            article_links.write(article_url)
            article_links.write("\n")
    except KeyError:
        pass


def compare(s1, s2):
    print len(s1), len(s2)
    for i in range(len(s1)):
        if (s1[i] != s2[i]):
            print i, s1[i]

def openUrlWithCookie(url):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie',
                              'wap_sid=CP/D4IgKEkBrdlpJS1U3UFZQenlRNFdQM3J5UmhIUmo0QnZJNUZUaHBYNkxBbm9NdFJ4Unc0U2RBVHV4dFI0TkE3Q2N4anZ5GAQg/REo8L/4uQsw9NHywgU=; '
                              'wap_sid2=CP/D4IgKElxpOTZDRDNVVC1SZ2JZUTd0cmYwOE5WWTRsaW5jNmV3TFdjdHNkUXQ5T3pWcDVBdnNwUEVucWpnWk43MjEzUXlrWGVnMC1BNzFyLVFXWmhvR3hlZEF1M1FEQUFBfg=='))
    opener.addheaders.append(('User-Agent',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'))
    f = opener.open(url)
    return f.read()
