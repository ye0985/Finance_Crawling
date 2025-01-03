#https://finance.naver.com/sise/sise_market_sum.naver
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


browser = webdriver.Chrome() #브라우저 객체생성
browser.maximize_window() #창 최대화

#1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

#2. 조회항묵 초기화(페이지에서 체크되어있는 항목 체크해제하기) 개발자도구오픈
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()
    
#3.조회항목 설정(원하는 항목 체크하기)
items_to_select = ['영업이익','자산총계','매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH,'..')
    label = parent.find_element(By.TAG_NAME,'label')
    #print(label.text)
    if label.text in items_to_select:
        checkbox.click()
        
#4. 적용하기 버튼 누르기
apply = browser.find_element(By.XPATH,'//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]')
apply.click()

for idx in range(1,40): #1이상 40미만 페이지 반복
    #사전작업 > 페이지 이동
    browser.get(url + str(idx)) 

    #5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index',how='all',inplace=True) # 모두 naan인 row 지우기
    df.dropna(axis='columns',how='all',inplace=True)

    # 마지막 페이지 끝나면 반복문 종료
    if len(df) == 0:
        break
    
    #5. 파일 저장
    f_name = 'fin.csv'
    if os.path.exists(f_name): #파일이 있다면 헤더제외
        df.to_csv(f_name, encoding='utf-8-sig',index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig',index=False)
    print(f'{idx}페이지 완료')

browser.quit()