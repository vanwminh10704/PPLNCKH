import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = 'D:\\Study\\phuong_phap_luan_NCKH\\THPT_2019 Analysis\\chromedriver.exe'

browser = webdriver.Chrome(options=options)
# Khai bao bien browser

url = 'https://diemthi.vnanet.vn/diem-thi/2019'

# So bao danh
current_sbd = 3000001

# Bien count thoat khoi vong lap
count = 0

# Thong tin cac cot
so_bao_danh = []
diem_toan = []
diem_van = []
diem_ngoai_ngu = []
diem_ly = []
diem_hoa = []
diem_sinh = []
diem_khtn = []
diem_su = []
diem_dia = []
diem_gdcd = []
diem_khxh = []

def grade_crawl(sbd):
    so_bao_danh.append(sbd)

    toan = WebDriverWait(browser, 4000).until(EC.presence_of_element_located((By.ID, "Toan")))
    diem_toan.append(toan.text)

    van = browser.find_element(By.ID, 'NguVan')
    diem_van.append(van.text)

    ngoai_ngu = browser.find_element(By.ID, 'NgoaiNgu')
    diem_ngoai_ngu.append(ngoai_ngu.text)

    ly = browser.find_element(By.ID, 'VatLi')
    diem_ly.append(ly.text)

    hoa = browser.find_element(By.ID, 'HoaHoc')
    diem_hoa.append(hoa.text)

    sinh = browser.find_element(By.ID, 'SinhHoc')
    diem_sinh.append(sinh.text)

    khtn = browser.find_element(By.ID, 'KHTN')
    diem_khtn.append(khtn.text)

    su = browser.find_element(By.ID, 'LichSu')
    diem_su.append(su.text)

    dia = browser.find_element(By.ID, 'DiaLi')
    diem_dia.append(dia.text)

    gdcd = browser.find_element(By.ID, 'GDCD')
    diem_gdcd.append(gdcd.text)

    khxh = browser.find_element(By.ID, 'KHXH')
    diem_khxh.append(khxh.text)

    return

def check_condition():
    continue_cond = WebDriverWait(browser, 4000).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr/td")))
    if continue_cond.text == 'CHƯA CÓ DỮ LIỆU':
        return 0
    else:
        return 1

while True:
    try:
        print('Checking SBD: 0' + str(current_sbd))
        browser.get(url)

        # Nhap SBD tai o nhap
        sbd = browser.find_element(By.ID, 'Code')
        sbd.clear()
        sbd_key = '0' + str(current_sbd)
        sbd.send_keys(sbd_key)

        # Click nut tra cuu
        btn = WebDriverWait(browser, 4000).until(EC.element_to_be_clickable((By.ID, "btnSearch")))
        btn.click()

        # Xu ly dieu kien
        if check_condition() == 0:
            count += 1
            # Neu 4 lan lien tiep khong doc duoc du lieu => Da doc het
            if count == 4:
                break
            else:
                current_sbd += 1
                continue
        else:
            count = 0

        # Lay du lieu ve sbd va diem
        grade_crawl(sbd_key)
        print(f"Data for SBD {sbd_key} has been crawled.")

        current_sbd += 1
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Chuyen du lieu sang file csv
df = pd.DataFrame({'So Bao Danh': so_bao_danh, 'Toan': diem_toan, 'Ngu Van': diem_van, 'Ngoai Ngu': diem_ngoai_ngu,
                   'Vat Ly': diem_ly, 'Hoa Hoc': diem_hoa, 'Sinh Hoc': diem_sinh, 'KHTN': diem_khtn,
                   'Lich Su': diem_su, 'Dia Ly': diem_dia, 'GDCD': diem_gdcd, 'KHXH': diem_khxh})
df.to_csv('diem_thptqg_2019.csv', index=False)
browser.close()