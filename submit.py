from getCookies import readCookies
import time
import requests


headers = {
    'Host': 'pintia.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'application/json;charset=UTF-8',
    'Content-Type': 'application/json;charset=UTF-8'

}
PTACookies = readCookies()


def submit(pid, code):
    url = 'https://pintia.cn/api/exams/1161882109920690176/submissions'
    payload_dict = {
        "problemType": "PROGRAMMING",
        "details": [{"problemId": "0", "problemSetProblemId": pid,
                     "programmingSubmissionDetail": {"program": code, "compiler": "GCC"}}]
    }
    payload_data = str(payload_dict)
    response = requests.post(url, headers=headers, cookies=PTACookies, data=payload_data)
    time.sleep(3)
    sub_id = response.text[17:-2]
    score = get_score(sub_id)
    print(f'Your Score is: {score}')


def get_score(submission_id):
    base_url = 'https://pintia.cn/api/submissions/'
    url = base_url + submission_id
    response = requests.get(url, headers=headers,cookies=PTACookies)
    json = response.json()
    items = json.get('submission')
    score = items['score']
    return score


if __name__ == '__main__':
    pid = input('请输入题目id: ')
    file_path = input('请输入文件路径: ')
    f = open(file_path, 'r')
    code = f.read()
    submit(pid, code)