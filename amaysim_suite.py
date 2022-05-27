#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

def seturl():
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    driver.get("https://www.amaysim.com.au")
    return driver

def login(driver,wait):
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[id='username']")))
    loginpage = driver.current_url
    wait = WebDriverWait(driver, 5)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='username']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='username']"))).send_keys("0466134574")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='password']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='password']"))).send_keys("AWqasde321")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']"))).click()
    
def referafriend(driver):
    try:
        testfile = open('mails.txt', 'r')
        Lines = testfile.readlines()

        #switch to frame
        wait = WebDriverWait(driver, 60)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='260e0219-2200-43ff-baf8-c1930afa23e2']")))

        count = 0
        mail = ''
        for line in Lines:
            count += 1
            mail = '{}'.format(line.strip())
            print(mail)

            #Refer a friend
            wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Send to (comma separated)']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Send to (comma separated)']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Send to (comma separated)']"))).send_keys(mail)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit']"))).click()
            
            if count == 1:
                #Checking successful email sent. Thanks for sharing
                thanksforshare = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text-markdown-container false']/p[text()='Thanks for sharing the big love']")))
                print(thanksforshare.text)
            else:
                #Checking if the invalid mail was sent
                thanksforshare = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text-markdown-container false']/p[text()='Tend your friends an email']")))
                print(thanksforshare.text)
            
            #Share again
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit']"))).click()
    except TimeoutException:
        print('The element was not visible, time out is reached!')
    else:
        print('Testing is PASSED!')

def main():
    
    #Set url
    driver = seturl()
    
    print('Test START')
    wait = WebDriverWait(driver, 20)

    #Homepage
    account = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Account']")))
    account.click()

    #Loginpage
    login(driver,wait)
    
    #Services
    wait = WebDriverWait(driver, 20)
    service = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'My New Sim Nickname')]")))
    print(service.text)
    service.click()
    
    #My New Sim Nickname
    newsimnickname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Refer a friend')]")))
    print(newsimnickname.text)
    newsimnickname.click()
    
    #test refer a friend
    print('Testing refer a friend emails.')
    referafriend(driver)
    
    #End test
    driver.close()
    print('Test END')

if __name__ == '__main__':
	main()