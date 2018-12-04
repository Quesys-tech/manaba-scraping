import datetime
import json

import pytz
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def GetTable():

    # Linux
    webdriver_path = './chromedriver'
    # windows
    #webdriver_path = '.\\chromedriver.exe'

    driver = webdriver.Chrome(webdriver_path)

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

    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.NAME, "_eventId_proceed")))
    driver.find_element_by_name("_eventId_proceed").click()

    # 未提出課題のページへ飛ぶ
    WebDriverWait(driver, 10).until(
        expected_conditions.url_changes("https://manaba.tsukuba.ac.jp/"))
    driver.get('https://manaba.tsukuba.ac.jp/ct/home_library_query')

    # テキスト取得
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "stdlist")))
    soup = BeautifulSoup(driver.page_source, "lxml")

    rows = soup.find('table', class_='stdlist').find_all(
        'tr', class_=["row0", "row1"])

    assignments = list()

    for row in rows:

        assignment = dict()

        cells = row.find_all('td')

        # 要素のテキストを代入
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


def FindNearDeadline(assignments):
    criteria_hours = 7*24  # 通知を締切までの残り時間(単位:h)

    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)

    ret = []

    for assignment in assignments:

        if len(assignment['deadline']) == 0:  # 締切の設定がないものは無視する
            continue

        deadline = datetime.datetime.strptime(
            assignment['deadline']+'+0900', '%Y-%m-%d %H:%M%z')  # 日本標準時を示す"+0900"を追加

        # print(deadline)

        timedelta = deadline - now

        # 基準以内の処理をする
        if timedelta <= datetime.timedelta(hours=criteria_hours) and timedelta > datetime.timedelta(0):
            ret.append(
                {
                    'title': assignment['title'],
                    'link': assignment['link'],
                    'timedelta': timedelta
                }
            )

    return ret


def push2slack(near_deadlines):
    webhook_url = 'webhook url'

    message_body = '@channel\n'
    for assignment in near_deadlines:
        message_body += '<' + \
            assignment['link']+'|'+assignment['title'] + \
            '> 残り時間:'+str(assignment['timedelta']) + '\n'

    requests.post(webhook_url, data=json.dumps({
        'text': message_body,  # 投稿するテキスト
        'username': u'manaba 宿題',  # 投稿のユーザー名
        'icon_emoji': u':ghost:',  # 投稿のプロフィール画像に入れる絵文字
        'link_names': 1,  # メンションを有効にする
    }))


def main():
    assignments = GetTable()
    near_deadlines = FindNearDeadline(assignments)
    push2slack(near_deadlines)


if __name__ == '__main__':
    main()
