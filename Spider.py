# -*- coding:utf-8 -*-

import requests
import bs4
import re

# 豆瓣top250电影

def open_url(url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res = requests.get(url,headers=headers)

    return res

def find_movies(res):
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    
    # 电影名
    movies = []
    targets = soup.find_all('div',class_='hd')
    for i in targets:
        movies.append(i.a.span.text)

    # 评分
    ranks = []
    targets = soup.find_all('span',class_='rating_num')
    for i in targets:
        ranks.append('评分：%s ' % i.text)

    # 简介
    messages = []
    targets = soup.find_all('div',class_='bd')
    for i in targets:
        try:
            messages.append(i.p.text.split('\n')[1].strip() + i.p.text.split('\n')[2].strip())
        except:
            continue

    result = []
    lenth = len(movies)
    for i in range(lenth):
        result.append('《' + movies[i] + '》' + ' ' + ranks[i] + '\n')

    return result


def find_depth(res):
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    depth = soup.find('span',class_='next').previous_sibling.previous_sibling.text

    return int(depth)


def main():
    host = 'https://movie.douban.com/top250'
    res = open_url(host)
    depth = find_depth(res)

    result = []
    for i in range(depth):
        url = host + '/?start=' + str(25 * i)
        res = open_url(url)
        result.extend(find_movies(res))

    with open('豆瓣TOP250.txt','w',encoding='utf-8') as f:
        for i in result:
            f.write(i)

    print('爬取完成!')


if __name__ == "__main__":
    main()
