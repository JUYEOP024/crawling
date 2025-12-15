from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("https://naver.com")
time.sleep(1)

# 검색창 입력
search_box = driver.find_element(By.ID, 'query')
search_box.send_keys("크롤링")
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# 뉴스 탭 클릭 (가장 확실한 선택자)
news_btn = driver.find_element(By.CSS_SELECTOR, "a.tab[href*='where=news']")
news_btn.click()
time.sleep(2)

# 스크롤 5번
for _ in range(5):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(1)

# 뉴스 제목/링크 추출
news_contents_elems = driver.find_elements(By.CSS_SELECTOR, "a.news_tit")

print(f"🔍 수집된 뉴스 개수: {len(news_contents_elems)}")

for elem in news_contents_elems:
    title = elem.get_attribute("title")
    href = elem.get_attribute("href")
    print(title, "|", href)

driver.quit()