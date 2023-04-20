from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service   
import time
import requests
import multiprocessing


count = 33
def istockphoto(row):
    global count
    url = f"https://www.istockphoto.com/search/2/image?alloweduse=availableforalluses&mediatype=photography&phrase=single%20tree&sort=best&page={str(row)}"
    option = Options()
    # option.headless = True
    option.add_argument('--headless')
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    driver.maximize_window()
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    pause_time = 1
    new_height =1000

    while True:
        driver.execute_script(f"window.scrollTo(0,{new_height});")
        time.sleep(pause_time)
        new_height = new_height + 1000
        if new_height >= last_height:
            break

    images_urls = driver.find_elements(By.CLASS_NAME,'PnVbv5qRe5ya18jbe2Gt')

    for i in images_urls:
        img_url = i.get_attribute('src')
        response = requests.get(img_url)
        with open(f"Tree_images/{count}.png",'wb') as f:
            f.write(response.content)
            count = count + 1

if __name__ == "__main__":
    pool = multiprocessing.Pool(4)
    pool.map(istockphoto,range(1,99))
    pool.close()
    pool.join()


