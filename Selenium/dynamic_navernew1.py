from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("https://www.naver.com")
time.sleep(1)

# 검색창 입력
search_box = driver.find_element(By.ID, "query")
search_box.send_keys("크롤링")
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# 네이버 검색 결과 로딩 이후 뉴스 탭 클릭
try:
    news_tab = driver.find_element(By.XPATH, '//a[span[text()="뉴스"]]')
    news_tab.click()
    print("✅ 뉴스 탭 클릭 성공!")
except Exception as e:
    print("❌ 뉴스 탭 클릭 실패:", e)

time.sleep(2)

driver.quit()