import urllib.parse
import urllib.request
import json
import mysql.connector
from datetime import datetime
# API KEY
client_id = 'V12BgFSFkiowXx3ZCXU3'
client_secret = 'OHFnlzlOT_'

# 검색어
searchText = urllib.parse.quote('크리스마스')

# url 및 헤더 설정
url = 'https://openapi.naver.com/v1/search/book.json?query=' + searchText + '&display=1'
request = urllib.request.Request(url)  # 네이버 API 요청 준비
request.add_header("X-Naver-Client-Id", client_id)  # 인증 헤더 추가
request.add_header("X-Naver-Client-Secret", client_secret)  # 인증 헤더 추가

response = urllib.request.urlopen(request)  # 네이버 API 호출
response_body = response.read()  # 실제 응답 데이터
response_body = json.loads(response_body)  # JSON -> 파이썬 Dict 변환

total_count = response_body['total'] #전체 검색 결과 개수 확인
start_num = 1       #start파라미터 초기화
loop_count = total_count // 100+ 1 #100개씩 끊어서ㅁ 리스트 반복 
book_list = []                      #리스트 추가


for i in  range(loop_count):
    url = 'https://openapi.naver.com/v1/search/book.json?query='+ searchText + '&display=100&start=' + str(start_num)
    request.add_header("X-Naver-Client-Id", client_id)  # 인증 헤더 추가
    request.add_header("X-Naver-Client-Secret", client_secret)  # 인증 헤더 추가


    response = urllib.request.urlopen(request)  # 네이버 API 호출
    response_body = response.read()  # 실제 응답 데이터
    response_body = json.loads(response_body)  # JSON -> 파이썬 Dict 변환


    book_list += response_body['item'] #리스트 이어붙임
    start_num += 100 # 다음구간요청 

    if start_num > 1000:
        break
ㅁㅁ

# db 연결 객체 생성
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'wo115566?!',
    database = 'bookdb'
)

cursor = connection.cursor()  # SQL 실행 담당 객체 cursor 생성

sql = "INSERT INTO naver_book (book_title, book_image, author, publisher, isbn, book_description, pub_date) values (%s, %s, %s, %s, %s, %s, %s)"
for book_info in book_list:

    pub_str = book_info.get('pubdate','')
    if pub_str:
        pub_date = datetime.strptime(pub_str,'%Y%m%d').date()
    else:
        pub_date = None 
# 받아온 리스트만큼 돌면서 SQL 실행
for book_info in book_list:
    values = (
        book_info['title'],           # 책 제목
        book_info['image'],           # 이미지 (URL)
        book_info['author'],          # 저자
        book_info['publisher'],       # 출판사
        book_info['isbn'],
        book_info['description'],     # 책 소개
        book_info['pubdate']          # 출판일(YYYYMMDD)
    )
    cursor.execute(sql, values)  # SQL 실행

connection.commit()   # 실제 DB에 저장

#커서 및 연결 객체 종료
cursor.close()
connection.close()