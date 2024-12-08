from flask import Flask, render_template, request
from datetime import datetime
from trend_crawler import get_trending
from news_crawler import get_news
from weather_crawler import capture_weather
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    trends = get_trending()
    news_items = get_news()
    weather_image = None

    if os.path.exists('static/latest_weather.png'):
        weather_image = 'static/latest_weather.png'
    else:
        if capture_weather():
            weather_image = 'static/latest_weather.png'

    return render_template('index.html', 
                         trends=trends, 
                         news_items=news_items,
                         weather_image=weather_image)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)