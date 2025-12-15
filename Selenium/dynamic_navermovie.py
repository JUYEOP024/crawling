from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import csv 
import os

# --- 1. 설정 및 초기화 ---
print("무신사 크롤링 스크립트 시작")

# 드라이버 옵션 설정
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 자동 드라이버 관리를 사용합니다.
try:
    driver = webdriver.Chrome(options=options) 
except WebDriverException as e:
    print(f"드라이버 초기화 오류: Chrome 브라우저가 설치되어 있는지, 최신 버전인지 확인하세요. {e}")
    exit()

URL = "https://www.musinsa.com/brand/arcteryx?gf=A"
driver.get(URL)
print(f"페이지 접속 완료: {URL}")

# 명시적 대기 객체 정의 (최대 15초 대기)
wait = WebDriverWait(driver,5) 
product_data = []

# --- 2. 페이지 로딩 및 스크롤 ---

# 초기 상품 목록이 로드될 때까지 대기
try:
    print("초기 상품 목록 로드 대기...")
    product_list_selector = "#searchList" 
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, product_list_selector)))
    print("초기 상품 목록 로드 확인.")
except TimeoutException:
    print("초기 상품 목록 로드 시간 초과. 페이지가 변경되었거나 차단되었을 수 있습니다.")
    driver.quit()
    exit()

# 전체 상품을 로드하기 위해 스크롤을 반복합니다.
print("스크롤을 통한 추가 상품 로드 시도...")
last_height = driver.execute_script("return document.body.scrollHeight")
max_scrolls = 10 

for i in range(max_scrolls):
    # 페이지 끝까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 로드될 시간을 잠시 대기
    time.sleep(3) 
    
    # 새로운 높이 측정
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        print(f"스크롤 종료 (총 {i+1}회 스크롤). 모든 상품이 로드된 것으로 보입니다.")
        break
        
    last_height = new_height
    print(f"스크롤 {i+1}회 완료. 새로운 상품 로드 확인.")

    if i == max_scrolls - 1:
        print(f"최대 스크롤 횟수({max_scrolls}회) 도달. 강제 종료.")

# --- 3. 상품 항목 추출 ---
print("\n--- 상품 데이터 추출 시작 ---")

# 모든 상품 아이템 찾기
try:
    items = driver.find_elements(By.CSS_SELECTOR, ".product-list > li")
    print(f"총 {len(items)}개의 상품 항목을 찾았습니다.")

    if len(items) == 0:
        print("경고: 상품 항목을 찾지 못했습니다. 셀렉터가 변경되었을 수 있습니다.")

    for i, item in enumerate(items):
        try:
            # 1. 상품명 (제목)
            title_element = item.find_element(By.CSS_SELECTOR, ".list_info > a")
            product_name = title_element.get_attribute('title').strip()
            
            # 2. 브랜드명
            brand_element = item.find_element(By.CSS_SELECTOR, ".item_title > a")
            brand_name = brand_element.text.strip()
            
            # 3. 가격
            price_element = item.find_element(By.CSS_SELECTOR, ".price")
            price_text = price_element.text.replace('\n', ' ').strip()
            
            # 4. 좋아요 수
            try:
                like_element = item.find_element(By.CSS_SELECTOR, ".list_info .txt_cnt")
                likes = like_element.text.strip()
            except NoSuchElementException:
                likes = "N/A"
            
            if product_name and price_text:
                product_data.append({
                    "brand": brand_name,
                    "product_name": product_name,
                    "price": price_text,
                    "likes": likes
                })
            
        except Exception as e:
            print(f"Error at product item {i+1}: 데이터 추출 중 오류 발생 ({e.__class__.__name__}). 건너뜁니다.")
            
except Exception as e:
    print(f"\n치명적인 오류 발생: 상품 목록 탐색 실패. 페이지 구조를 확인하세요. {e}")

finally:
    driver.quit()
    print("드라이버 종료.")

# --- 4. CSV 저장 ---
print("\n--- CSV 저장 ---")
FILE_NAME = "musinsa_arcteryx_products.csv"
try:
    if product_data:
        with open(FILE_NAME, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=product_data[0].keys())
            
            # 헤더(열 이름) 작성
            writer.writeheader()
            
            # 데이터 행 작성
            writer.writerows(product_data)
        
        print(f"완료! 총 {len(product_data)}개의 상품 정보가 '{FILE_NAME}'에 CSV 형식으로 저장되었습니다.")
    else:
        print("추출된 상품 데이터가 없습니다. CSV 파일이 저장되지 않았습니다.")

except Exception as e:
    print(f"CSV 파일 저장 중 오류 발생: {e}")