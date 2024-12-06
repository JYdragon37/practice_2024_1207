from flask import Flask, render_template, request  # request 추가
from datetime import datetime
from trend_crawler import get_trending  # 새로 추가


app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time)

# 새로운 라우트 추가

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    return render_template('greet.html', name=name)

@app.route('/trend')
def trend():
    trends = get_trending()
    return render_template('trend.html', trends=trends)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)