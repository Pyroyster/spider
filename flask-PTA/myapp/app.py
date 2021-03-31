from flask import Flask, render_template
import pymysql
import html


app = Flask(__name__)

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='210421',
    db='problemTest',
    charset='utf8'
)


@app.route('/')
def hello_world():
    cur = conn.cursor()
    # get annual sales rank
    sql = "select * from problems14"
    cur.execute(sql)
    content = cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM problems14"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    return render_template('index.html', labels=labels, content=content)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5003)
