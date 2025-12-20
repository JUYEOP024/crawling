params = {
    "key": "33d28a024ade6c377ded6e2b3b69bcd4",
    "targetDt": "20251207"
}


import requests

url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"


# API 요청
response = requests.get(url, params=params)
# 결과 출력
if response.status_code == 200:

    print(response.json())
else:
    print(f"Error: {response.status_code}")

print(response.json()["boxOfficeResult"]['dailyBoxOfficeList'][0]['movieNm'])

data = response.json()
daily_list = ["boxOfficeResult"]['dailyboxOfficelist']

for i,movie in enumerate(daily_list):
    pritn
# for i, movie in enumerate(daily_list):