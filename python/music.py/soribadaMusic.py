import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
res = req.get("https://www.soribada.com/music/chart", headers=head)
soup = bs(res.text, "lxml")

ranking = soup.select(".hasPaddingContents .contentsSection .SongListWithTools .music-list-cont music-list-cont-type2 .music-list .listen .list-area-cont .list-area1 .number2 .num")
title = soup.select("tbody .info a.title.ellipsis")
artist = soup.select("tbody .info a.artist.ellipsis")


rankingList = []
titleList = []
artistList = []

print(len(ranking))
print(len(artist))
print(len(title))

rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]

chart_df = pd.DataFrame({
    'Ranking': rankingList,
    'Title': titleList,
    'Artist': artistList
})

# JSON 파일로 저장 
# chart_df.to_json("geniemusic.json", force_ascii=False, orient="records")
