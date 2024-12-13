from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import winsound

from plyer import notification

# 예약 가능 상태를 확인하고, 예약이 가능하면 시스템 트레이 알림을 보내는 함수
def send_system_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout= 10,  # 알림 표시 시간 (초 단위)
        toast = True
    )
 # 소리 내기
    winsound.Beep(1000, 1000)  # 1000Hz의 소리로 1초간 알림
    
# Chrome 옵션 설정
options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# options.add_argument('--headless')  # 화면 없이 실행
# options.add_argument('--disable-gpu')  # GPU 가속 비활성화 (필요시)
# options.add_argument('--no-sandbox')  # 권한 관련 오류 방지 (필요시)

# Chrome 드라이버 실행
driver = webdriver.Chrome(options=options)

# 원하는 URL로 이동
driver.get('https://www.letskorail.com/ebizprd/prdMain.do')

# 페이지 로딩을 기다림
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@onclick="return m_login_link()"]')))

# 로그인 링크 클릭
login_link = driver.find_element(By.XPATH, '//a[@onclick="return m_login_link()"]')
login_link.click()

# 전화번호 로그인 선택
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="radInputFlg2"]')))
phone = driver.find_element(By.XPATH, '//*[@id="radInputFlg2"]')
phone.click()

# 휴대전화 번호 입력
id1 = driver.find_element(By.XPATH, '//*[@id="txtCpNo2"]')
id1.send_keys('9881')
time.sleep(0.5)

id2 = driver.find_element(By.XPATH, '//*[@id="txtCpNo3"]')
id2.send_keys('1073')
time.sleep(0.5)

# 비밀번호 입력
pw = driver.find_element(By.XPATH, '//*[@id="txtPwd1"]')
pw.send_keys('qkrwpdn!1')
time.sleep(0.5)

# 로그인 버튼 클릭
confirm = driver.find_element(By.XPATH, '//*[@id="loginDisplay2"]/ul/li[3]/a/img')
confirm.click()

# 페이지가 로드될 때까지 잠시 대기
time.sleep(3)

aaa = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/div[1]/h3/a/img')
aaa.click()

time.sleep(1)


departure = driver.find_element(By.XPATH, '//*[@id="start"]')
departure.clear()
departure.send_keys('구미')
time.sleep(0.5)

stop = driver.find_element(By.XPATH, '//*[@id="get"]')
stop.clear()
stop.send_keys('서울')
time.sleep(0.5)

day = driver.find_element(By.XPATH, '//*[@id="s_day"]')
day.click()
day2 = driver.find_element(By.XPATH, '//*[@id="s_day"]/option[14]')
day2.click()
time.sleep(0.5)

hour = driver.find_element(By.XPATH, '//*[@id="s_hour"]/option[11]')
hour.click()
time.sleep(0.5)

find = driver.find_element(By.XPATH, '//*[@id="center"]/form/div/p/a/img')
find.click()
time.sleep(5)

while True:
    try:
        # "좌석매진" 상태인지 확인
        try:
            seat_status_img = driver.find_element(By.XPATH, '//*[@id="tableResult"]/tbody/tr[5]/td[6]/img')
            seat_status_alt = seat_status_img.get_attribute('alt')
            if seat_status_alt == "좌석매진":
                print("매진 상태, 페이지 새로 고침 중...")
                driver.refresh()  # 페이지 새로고침
                time.sleep(random.uniform(2, 5))  # 새로고침 후 대기
                continue  # 루프 처음으로 돌아감
        except:
            print("좌석 상태 확인 실패, 예약 버튼 확인 진행...")

        # 예약하기 버튼 확인 및 클릭
        reserve_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tableResult"]/tbody/tr[5]/td[6]/a[1]'))
        )
        reserve_button.click()
        time.sleep(1)

        # 예약 확인 창 확인 및 처리
        try:
            frame = driver.find_element(By.ID, 'embeded-modal-traininfo')
            driver.switch_to.frame(frame)
            confirmation_button = driver.find_element(By.CLASS_NAME, 'btn_blue_ang')
            confirmation_button.click()
            print("예약 가능 상태로 변경됨! 예약 버튼 클릭 및 확인 완료")
        except:
            print("예약 확인 버튼이 없어도 예약 버튼 클릭 완료")
        
        # 알림 및 루프 종료
        send_system_notification('가능', '예약가능!!')
        break

    except Exception as e:
        print(f"오류 발생: {e}")
        send_system_notification('오류', '오류발생!')
        break



# # 추가적인 동작을 원할 경우 작성
time.sleep(3)

