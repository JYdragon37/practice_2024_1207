from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import os

def capture_weather():
    try:
        print("날씨 캡처 시작...")

        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.binary_location = os.getenv('CHROME_BIN', '/usr/bin/chromium')

        # Service 설정
        service = Service(
            executable_path=os.getenv('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')
        )

        print("Chrome 설정 완료")

        # WebDriver 초기화
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        print("WebDriver 초기화 완료")

        driver.set_window_size(1200, 1000)

        url = "https://weather.naver.com/today/09140104"
        driver.get(url)
        print("날씨 페이지 로딩 중...")

        # 페이지 로딩 대기
        time.sleep(3)

        try:
            # static 폴더가 없으면 생성
            if not os.path.exists('static'):
                os.makedirs('static')
                print("static 폴더 생성 완료")

            # 각 영역 찾기
            location_area = driver.find_element(By.CLASS_NAME, "location_info_area._cnBlockTemplate")
            weather_area = driver.find_element(By.CLASS_NAME, "weather_area._cnBlockTemplate")
            weather_graph = driver.find_element(By.CLASS_NAME, "card_weather_graph._cnBlockTemplate")

            print("날씨 요소 찾기 완료")

            # 임시 스크린샷들의 경로
            temp_path = os.path.join('static', 'temp_weather.png')
            final_path = os.path.join('static', 'latest_weather.png')

            # 전체 페이지 스크린샷
            driver.save_screenshot(temp_path)
            print("임시 스크린샷 저장 완료")

            # 각 영역의 위치와 크기 가져오기
            loc_rect = location_area.rect
            weather_rect = weather_area.rect
            graph_rect = weather_graph.rect

            # PIL을 사용하여 이미지 처리
            with Image.open(temp_path) as img:
                # 모든 영역을 포함할 수 있는 크기 계산
                min_x = min(loc_rect['x'], weather_rect['x'], graph_rect['x'])
                max_x = max(loc_rect['x'] + loc_rect['width'], 
                          weather_rect['x'] + weather_rect['width'],
                          graph_rect['x'] + graph_rect['width'])
                min_y = min(loc_rect['y'], weather_rect['y'], graph_rect['y'])
                max_y = max(loc_rect['y'] + loc_rect['height'],
                          weather_rect['y'] + weather_rect['height'],
                          graph_rect['y'] + graph_rect['height'])

                # 여백 추가
                padding = 20
                min_x = max(0, min_x - padding)
                min_y = max(0, min_y - padding)
                max_x = min(img.width, max_x + padding)
                max_y = min(img.height, max_y + padding)

                # 이미지 자르기
                cropped = img.crop((min_x, min_y, max_x, max_y))
                cropped.save(final_path)
                print(f"최종 스크린샷 저장 완료: {final_path}")

            # 임시 파일 삭제
            os.remove(temp_path)
            print("임시 파일 삭제 완료")

            return True

        except Exception as e:
            print(f"요소를 찾거나 스크린샷 촬영 중 오류 발생: {str(e)}")
            return False

    except Exception as e:
        print(f"Weather capture failed: {str(e)}")
        return False

    finally:
        try:
            if 'driver' in locals():
                driver.quit()
                print("WebDriver 종료 완료")
        except Exception as e:
            print(f"WebDriver 종료 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    success = capture_weather()
    if success:
        print("날씨 캡처 성공")
    else:
        print("날씨 캡처 실패")