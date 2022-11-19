from selenium import webdriver
import time
import json

options = webdriver.ChromeOptions()
options.add_argument(
    'User-Agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
    'Safari/537.36"')
driver = webdriver.Chrome(chrome_options=options)

driver.implicitly_wait(10)
driver.get('https://mikrotik.com/products/group/ethernet-routers')
driver.implicitly_wait(10)

count = 0  # 记录点击次数
device_link = []
result = []
time.sleep(2)
link_list = driver.find_elements('xpath', '//div[@id="productlist17"]/div[@class="product"]/div/a')
# device_info1 = {}
# 存储按钮，进入二级界面
# print(link_list)
device_type_list = driver.find_elements('xpath', '//div[@id="productlist17"]/div[@class="product"]')

for i in device_type_list:
    device_info1 = {}
    device_info1['vender'] = 'MikroTik'
    device_info1['device_type'] = i.get_attribute('data-code')
    device_info1['firmware_name'] = i.get_attribute('data-name')
    result.append(device_info1)


for link in link_list:
    device_list = {'link': link.get_attribute('href')}
    # device_list['device_type'] = link.get_attribute('innerHTML')
    device_link.append(device_list)

result_new = []
for i in range(len(device_link)):
    url = device_link[i]['link']
    driver.get(url)
    herf = url + '#fndtn-downloads'
    driver.get(herf)
    driver.implicitly_wait(10)
    button = driver.find_elements('xpath', '//div[@id="downloads"]/div[5]/a')
    device_info2 = {'download_link': button[0].get_attribute('href')}
    device_info2['hardware_version'] = device_info2['download_link'].split('/')[-1][:-4]
    device_info = dict(device_info2, **result[i])
    result_new.append(device_info)
    # print(result_new)

aJson = json.dumps(result_new, indent=2)
with open("MT.json", "w") as fp:
    fp.write(aJson)
