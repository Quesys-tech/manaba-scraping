import datetime
import pytz
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


def GetTable():

    webdriver_path = 'C:\dev\chromedriver.exe'  # 環境によって変える

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

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "_eventId_proceed")))
    driver.find_element_by_name("_eventId_proceed").click()

    # 未提出課題のページへ飛ぶ
    WebDriverWait(driver, 10).until(expected_conditions.url_changes("https://manaba.tsukuba.ac.jp/"))
    driver.get('https://manaba.tsukuba.ac.jp/ct/home_library_query')

    # テキスト取得
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "stdlist")))
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


def main():
    assignments = GetTable()

    criteria_hours = 7*24  # 通知を締切までの残り時間(単位:h)

    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)

    for assignment in assignments:

        if len(assignment['deadline']) == 0: #締切の設定がないものは無視する
            continue

        deadline = datetime.datetime.strptime(
            assignment['deadline']+'+0900', '%Y-%m-%d %H:%M%z')  # 日本標準時を示す"+0900"を追加

        # print(deadline)

        timedelta = deadline - now

        if timedelta <= datetime.timedelta(hours=criteria_hours): #基準以内の処理をする
            print(assignment['title']+'\t' +
                  str(timedelta)+'\t'+'deadline is near.')
        else:
            print(assignment['title']+'\t'+str(timedelta) +
                  '\t'+'deadline is not near.')


if __name__ == '__main__':
    main()
