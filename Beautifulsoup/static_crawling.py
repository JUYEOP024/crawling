import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from datetime import datetime

class MusicEntry:
    def __init__(self, title, artist, img_path):
        self.title = title
        self.artist = artist
        self.img_path = img_path

    def __repr__(self):
        return f'🎵 {self.artist}의 {self.title} | {self.img_path}'

# 1) 웹 페이지 요청
url = 'https://music.bugs.co.kr/chart/track/week/total'
response = requests.get(url)

# 2) BeautifulSoup 파싱
bs = BeautifulSoup(response.text, 'html.parser')

# 3) 차트 리스트 추출
track_list = bs.select('table.list.trackList.byChart tbody tr')

print(track_list[0])

result_list = []
#title=p.class a / artist = p.artist a / image = a.thumbnail img 태그의 src속성값
for i, song in enumerate(track_list[:30]):
    title = song.select_one('p.title a').text.strip()
    artist = song.select_one('p.artist a').text.strip()
    img_src = song.select_one('a.thumbnail img')['src']
#이미지 저장 
    filename = f"album/images/{datetime.now().strftime('%y%m%d_%H%M%S')}_{i+1}.jpg"
    urlretrieve(img_src,filename)

    music_entry = MusicEntry(title,artist,filename)
    result_list.append(music_entry)

for result in result_list:
    print(result)