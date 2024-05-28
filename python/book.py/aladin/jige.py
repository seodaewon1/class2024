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
from urllib.parse import urlparse, parse_qs  # 필요한 모듈 임포트

current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"jige_{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()

service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# CGV 페이지 열기
browser.get('https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=%EC%A7%80%EA%B2%8C%EC%B0%A8%EC%9A%B4%EC%A0%84%EA%B8%B0%EB%8A%A5%EC%82%AC')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "Search3_Result"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
book_data = []

# 첫 번째 tracks
tracks = soup.select(".ss_book_list")

for track in tracks:
    title = track.select_one(".bo3").text.strip()
    # rank = track.select_one(".rank.realtime_rank23").text.strip()
    # rate = track.select_one(".ticketing span").text.strip()
    # date = track.select_one(".movie-launch").text.strip()
    # image_url = track.select_one(".movieBox-item img").get('src')


    book_data.append({
        "title": title,
        # "rank": rank,
        # "rate": rate,
        # "date": date,
        # "imageURL": image_url
    })

print(book_data)

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
