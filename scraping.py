import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def GetTable():
    driver = webdriver.Chrome('C:\dev\chromedriver.exe')# 環境によって変える
    
    driver.get('https://manaba.tsukuba.ac.jp/')

    utid13 = ''
    password = ''

    # ファイルから資格情報の読み取り
    with open('secret.txt') as f:
        l = f.readlines()
        utid13 = l[0]
        password = l[1]

    driver.find_element_by_name("j_username").send_keys(utid13)
    driver.find_element_by_name("j_password").send_keys(password)

    sleep(1)
    driver.find_element_by_name("_eventId_proceed").click()

    # 未提出課題のページへ飛ぶ
    sleep(1)
    driver.get('https://manaba.tsukuba.ac.jp/ct/home_library_query')

    # テキスト取得
    sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml")

    rows = soup.find('table', class_='stdlist').find_all(
        'tr', class_=["row0", "row1"])

    assignments = list()

    for row in rows:

        assignment = dict()

        cells = row.find_all('td')

        #要素のテキストを代入
        assignment["course"] = cells[2].div.a.text
        assignment["title"] = cells[1].div.a.text
        assignment["link"] = "https://manaba.tsukuba.ac.jp/" + \
            cells[1].div.a.get('href')
        assignment["deadline"] = cells[4].text
        assignments.append(assignment)

    # 後始末
    driver.close()
    driver.quit()

    return assignments


def main():
    GetTable()


if __name__ == '__main__':
    main()
