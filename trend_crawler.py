import requests
import csv
from datetime import datetime

def get_trending(filename='latest_trends.csv'):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get("https://api.signal.bz/news/realtime", headers=headers)

        if response.status_code == 200:
            trend_data = response.json()

            # top10 배열에서 keyword 추출
            if 'top10' in trend_data:
                trends = [item['keyword'] for item in trend_data['top10']]
            else:
                print("데이터 구조에 'top10'이 없습니다.")
                return []

            # CSV 파일로 저장
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Rank', 'Keyword'])
                for idx, trend in enumerate(trends, 1):
                    writer.writerow([idx, trend])

            return trends
        else:
            print(f"API 요청 실패: {response.status_code}")
            return []

    except Exception as e:
        print(f"트렌드를 가져오는데 실패했습니다: {str(e)}")
        return []

if __name__ == "__main__":
    print("트렌드 수집 시작...")
    trends = get_trending()
    print("\n=== 실시간 트렌드 ===")
    for idx, trend in enumerate(trends, 1):
        print(f"{idx}. {trend}")