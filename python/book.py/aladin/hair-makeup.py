from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Geonseol4_{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")  # Headless 모드 추가
options.add_argument("--no-sandbox")  # Sandbox 모드 비활성화
options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
options.add_argument("--disable-gpu")  # GPU 비활성화
options.add_argument("--window-size=1920x1080")  # 윈도우 크기 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# URL 열기
browser.get('https://www.yes24.com/Product/Search?domain=BOOK&query=%EA%B1%B4%EC%84%A4%EC%95%88%EC%A0%84%EA%B8%B0%EC%82%AC')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "sGLi"))
)

# 모든 이미지를 로드하기 위해 페이지 끝까지 스크롤
scroll_pause_time = 2
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
book_data = []

# 첫 번째 tracks
tracks = soup.select("li[data-goods-no]")

for track in tracks:
    title = track.select_one(".info_row.info_name .gd_name").text.strip()
    author = track.select_one(".info_row.info_pubGrp .info_auth").text.strip()
    price = track.select_one(".info_row.info_price .txt_num").text.strip()
    
    # 이미지 요소가 로드될 때까지 대기
    image_element = track.select_one(".img_bdr img")  # 이미지 요소 가져오기
    image_url = image_element.get('src') if image_element else None  # src에서 이미지 URL 가져오기
    
    # 이미지 URL이 .jpg로 끝나는 경우 제외
    if image_url and '.jpg' in image_url:
        image_url = None

    link_element = track.select_one(".gd_name a")  # 링크 요소 가져오기
    href = link_element.get('href') if link_element else None  # href 속성 가져오기
    full_url = f"https://www.yes24.com{href}" if href else None  # 앞에 URL 추가

    book_data.append({
        "title": title,
        "author": author,
        "imageURL": image_url,
        "price": price,
        "url": full_url
    })

print(book_data)

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
