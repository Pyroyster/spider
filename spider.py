import requests
import json
from urllib.parse import urlencode
import pymysql
from db import MyDB
base_url = 'https://pintia.cn/api/problem-sets/14/'
id_list = []

headers = {
    'Host': 'pintia.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'application/json;charset=UTF-8',
    'apiVersion': '2.0',
    'X-Requested-With': 'XMLHttpRequest',
}

param1 = {
        'problem_type': 'CODE_COMPLETION',
        'page': 0,
        'limit': 100,
    }

param2 = {
        'problem_type': 'PROGRAMMING',
        'page': 0,
        'limit': 100,
    }


def get_id_list():
    url1 = base_url + 'problem-list?' + urlencode(param1)
    print(url1)
    url2 = base_url + 'problem-list?' + urlencode(param2)
    try:
        response1 = requests.get(url1, headers=headers)
        if response1.status_code == 200:
            problem_set_list1 = response1.json()['problemSetProblems']
            for problem_str in problem_set_list1:
                id_list.append(problem_str['id'])
    except requests.ConnectionError as e:
        print('Error', e.args)
    try:
        response2 = requests.get(url2, headers=headers)
        if response2.status_code == 200:
            problem_set_list1 = response2.json()['problemSetProblems']
            for problem_str in problem_set_list1:
                id_list.append(problem_str['id'])
    except requests.ConnectionError as e:
        print('Error', e.args)


def get_page(id):
    url = base_url + 'problems/' + id
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        items = json.get('problemSetProblem')
        # print(items)
        problem_info = {
            'problemId': items['id'],
            'title': items['title'],
            'type': items['type'],
            'content': items['content'],
            'points': items['score']
        }
        yield problem_info


if __name__ == '__main__':
    db = MyDB()
    table = 'problems'
    sql = """CREATE TABLE IF NOT EXISTS problems (
    problemId VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(64) NOT NULL,
    content TEXT,
    points INT NOT NULL,
    score INT,
    PRIMARY KEY (problemId))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    """
    db.create_table(sql)
    get_id_list()
    for id in id_list:
        json = get_page(id)
        problem_info_list = parse_page(json)
        for problem_data in problem_info_list:
            db.savedata(problem_data, table)
    db.close()








