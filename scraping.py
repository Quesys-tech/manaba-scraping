import datetime
import json

import pytz
import requests
from bs4 import BeautifulSoup


def GetTable():

    username = ''
    password = ''

    # ファイルから資格情報の読み取り
    with open('secret.txt') as f:
        l = f.readlines()
        username = l[0]
        password = l[1]

    with requests.Session() as s:  # セッションを生成
        # ヘッダ偽装
        s.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

        r = s.get('https://manaba.tsukuba.ac.jp/')

        soup = BeautifulSoup(r.content, "lxml")
        form = soup.find("form")

        post_url = 'https://idp.account.tsukuba.ac.jp/'+form.get("action")

        payload = {
            '_eventId_proceed': '',
            'j_password': password,
            'j_username': username
        }

        # postしたあとcontinueボタンを押すページに飛ばされる
        r = s.post(post_url, data=payload)

        # continueボタンを押すときに送信されるデータを解析
        soup = BeautifulSoup(r.content, "lxml")

        # continueボタンを押したときに送信される内容
        payload = {
            'SAMLResponse': '',
            'RelayState': '',
            'submit': 'Continue'
        }

        payload['RelayState'] = soup.find(
            attrs={'name': 'RelayState'}).get('value')
        payload['SAMLResponse'] = soup.find(
            attrs={'name': 'SAMLResponse'}).get('value')

        post_url = soup.find('form').get('action')

        s.post(post_url, payload)  # continueボタンを押す

        # manabaの課題ページを取得
        r = s.get('https://manaba.tsukuba.ac.jp/ct/home_library_query')

    # 未提出課題の表を解析
    soup = BeautifulSoup(r.content, "lxml")
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
