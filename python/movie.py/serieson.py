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
filename = f"serieson_{current_date}.json"


# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get('https://serieson.naver.com/v3/movie/products/hot_new')


# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ListPage_category_wrap__L1R0q"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')


# 데이터 추출
movie_data = []
tracks = soup.select(".ListCollection_list__uk9qe li")
for track in tracks:
    # rank = track.select_one(".RankingNumber_rank__zZLNC").text.strip()
    title = track.select_one(".Title_title__s9o0D").text.strip()
    price = track.select_one(".Price_price__GqXqo").text.strip()
    image_url = track.select_one("img.Thumbnail_image__TxHd0").get('src')

    movie_data.append({
        # "rank": rank,
        "title": title,
        "price": price,
        "imageURL": image_url,
    })
    print(movie_data)
# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(movie_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
