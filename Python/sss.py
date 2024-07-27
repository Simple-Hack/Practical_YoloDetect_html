from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.edge.options import Options


# 创建字典存储景点名和URL
scenic_spots = {
    #'武隆三桥': 'https://you.ctrip.com/sight/chongqing158/45771.html',
    #'重庆动物园': 'https://you.ctrip.com/sight/chongqing158/10377.html',
    # '重庆大足石刻景区':'https://you.ctrip.com/sight/chongqing158/10330.html',
    # '重庆巫山小三峡—小小三峡':'https://you.ctrip.com/sight/wushancounty2025187/4299.html',
    # '重庆武隆喀斯特旅游区（天生三桥·仙女山·芙蓉洞）':'https://you.ctrip.com/sight/chongqing158/112663.html',
    # '重庆酉阳桃花源景区':'https://you.ctrip.com/sight/youyangcounty2025213/10373.html',
    # '重庆万盛黑山谷景区':"https://you.ctrip.com/sight/chongqing158/1412960.html",
    # '重庆南川金佛山景区':"https://you.ctrip.com/sight/chongqing158/10348.html",
    # '重庆江津四面山景区':'https://you.ctrip.com/sight/chongqing158/10414.html',
    # '重庆云阳龙缸景区':'https://you.ctrip.com/sight/yunyangcounty2025226/2707023.html',
    # '重庆彭水阿依河景区':'https://you.ctrip.com/sight/pengshuicounty2025231/143007.html',
    # '重庆黔江濯水景区':'https://you.ctrip.com/sight/chongqing158/1481421.html',
    # '重庆奉节白帝城·瞿塘峡景区':'https://you.ctrip.com/sight/fengjiecounty2025223/4298.html',
    # '重庆涪陵武陵山大裂谷景区':'https://you.ctrip.com/sight/chongqing158/1697167.html',
    # '重庆丰都名山风景区':'https://you.ctrip.com/sight/fengducounty2025250/112358.html',
    # '重庆聂荣臻元帅陈列馆':'https://you.ctrip.com/sight/chongqing158/10343.html',
    # '重庆忠县石宝寨':'https://you.ctrip.com/sight/zhongcounty2025198/4311.html',
    # '重庆人民大礼堂及人民广场':'https://you.ctrip.com/sight/chongqing158/10395.html'
    # 添加更多景点...
}

opt = Options()
opt.add_argument("--headless")
opt.add_argument("window-size=1920x1080")
opt.add_argument('--start-maximized')
driver = webdriver.Edge(options=opt)
 
def to_the_buttom():
    js = 'document.getElementsByClassName("search-body left_is_mini")[0].scrollTop=10000'
    driver.execute_script(js)
def to_the_top():
    js = "var q=document.documentElement.scrollTop=0"  # 滚动到最上面
    driver.execute_script(js)
def to_view():
    driver.implicitly_wait(10)#隐式等待10s，条件成立则立即结束等待
    to_the_buttom()
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR,'li.ant-pagination-next>span')
    driver.execute_script("arguments[0].scrollIntoView();", button)    
    
def fun(name, url):
    print(f'This is {name}')
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    with open("all_comment.csv", "a", encoding='utf-8-sig', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(('景点', '日期', '用户评论'))

        for page in range(1, 31):
            try:
                comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "commentDetail")))
                dates = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "commentTime")))

                for i, comment in enumerate(comments):
                    text = comment.text.strip().replace('\n', '')
                    date = dates[i].text.strip().replace('\n', '')
                    csvwriter.writerow((name, date, text))
                    f.flush()
                    print(text)

                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[7]/a')))
                ActionChains(driver).move_to_element(next_button).click().perform()
                print(page)
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

for spot_name, url in scenic_spots.items():
    fun(spot_name, url)

driver.quit()