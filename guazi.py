import re
import csv
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 8)

car_urls = []
td1 = []
td2 = []
car_data = []


def request_page(r_url):
    browser.get(r_url)
    html = browser.page_source
    r_soup = BeautifulSoup(html, 'lxml')
    return r_soup


def page_parser():  # 获取每一页的url并解析出下一页面的后缀
    p_url = 'https://www.guazi.com/gz/bmw/'
    p_soup = request_page(p_url)
    infos = p_soup.select('.car-a')
    for info in infos:
        c_url = re.findall('href="(.*?)"', str(info))[0]
        car_url = 'https://www.guazi.com' + c_url
        car_urls.append(car_url)
    n_page = soup.find('a', {'class': 'next'})
    if n_page:
        next_page = n_page['href'].split('/')[-2] + '/#bread'
        return next_page
    else:
        return None


def get_info():
    for car_url in car_urls:
        g_soup = request_page(car_url)
        info = g_soup.select('.td1')
        for s in info:
            t1 = s.get_text().split('\n')[0]
            if not t1:  # 去掉表格中的空格
                continue
            td1.append(t1)
        info = g_soup.select('.td2')
        for s in info:
            t2 = s.get_text()
            if not t2:
                continue
            td2.append(t2)
        time.sleep(random.random())
    for s1, s2 in zip(td1, td2):
        d = {'配置': s1, '参数': s2}
        car_data.append(d)
    return car_data


def info_save():
    with open('E:\\car.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['配置', '参数']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = get_info()
        writer.writerows(data)
        print('保存成功')


if __name__ == '__main__':
    regions = ['gz', 'sz', 'sh', 'bj', 'cd']
    for region in regions:
        url = 'https://www.guazi.com/{region}/richan/'.format(region=region)
        next_url = ''
        while next_url or next_url == '':
            soup = request_page(url + next_url)
            next_url = page_parser()
            time.sleep(random.random())
        info_save()
