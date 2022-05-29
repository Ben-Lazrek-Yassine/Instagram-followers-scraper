import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def scrape():
    email=input("Enter your email/username: ")
    passw=input("Enter your password: ")
    target=input("Enter the target instagram username: ")
    number=int(input("Enter the number of followers you want to scrape(~12 usernames per scroll): "))
    #there can't be errors if the console doesn't print them :)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #chromedriver shet
    driver = webdriver.Chrome("C:/chromewebdriver/chromedriver.exe",options=options)
    driver.get("https://www.instagram.com/")

    #login
    driver.implicitly_wait(3)
    username = driver.find_element(By.CSS_SELECTOR,"input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR,"input[name='password']")
    username.clear()
    password.clear()
    username.send_keys(email)
    password.send_keys(passw)
    login = driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

    #bypassing popups
    driver.implicitly_wait(3)
    notnow = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
    driver.implicitly_wait(3)
    notnow2 = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()


    #looking for a certain person
    time.sleep(2)
    searchbox = driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(target)
    search=driver.find_element(By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
    driver.implicitly_wait(3)
    followers=driver.find_element(By.XPATH,"//a[contains(@href, '/followers')]").click()

    #followers popup/scrolling
    time.sleep(2)
    driver.find_element(By.XPATH,value='/html/body/div[6]/div/div/div/div[2]')
    fBody  = driver.find_element(By.XPATH,"//div[@class='isgrP']")
    scroll = 0
    while scroll < number:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(1.5)
        scroll += 1

    #scraping names
    fList  = driver.find_elements(By.XPATH,"//div[@class='isgrP']//li")
    names = [name.text for name in fList if name.text != '']


    clean=[]
    final=[]
    for i in names:
        clean.append(i.split('\n'))
    for i in clean:
        for j in i[:-1]:
            final.append(j)
    return final

def save(final):
    with open('list.txt', 'a',encoding="utf-8") as f:
            for i in final:
                f.write(i + '\n')

def parse(list):
    for i in list:
        final=[]
        i = re.sub('[^a-zA-Z]', '', i)
        i = re.sub(r'[^\w]', '', i)
        i = i.replace(" ", "")
        i = re.sub(r'[\u0600-\u06FF]', '', i)
        if i != '' and i not in final:
            final.append(i)
        save(final)

scraped=scrape()
parsed=parse(scraped)
