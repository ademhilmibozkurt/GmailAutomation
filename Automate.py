import os
import time
import SECRETS
os.chdir('D:\projects\python\GmailAutomation')

from SeOptions import chromeOptions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

class GmailAutomation:
    def __init__(self):
        pass
    
    # import one receiver
    def importReceiver(self) -> str:
        ''' @docstrings '''
        with open('receiver.txt', 'r') as email:
            receiver = email.read()
                
        print(f'Length of receiver: {len(receiver)}')
        return receiver
    
    # import company contacts
    def importContacts(self) -> list[str]:
        ''' @docstrings '''
        contacts = []
        with open('TopTurkishCompanyContact.txt', 'r') as emails:
            for email in emails:
                contacts.append(email)
                
        print(f'Length of contacts: {len(contacts)}')
        return contacts
    
    def importSubject(self) -> str: 
        ''' ask '''       
        # import subject
        with open('subject.txt', 'r') as sub:
            subject = sub.read()
        
        print(f'Length of subject: {len(subject)}')
        return subject
    
    # import message
    def importMessage(self) -> str:
        with open('message.txt', 'r') as mes:
            message = mes.read()
            
        print(f'Length of message: {len(message)}')    
        return message
 
    # selenium
    def launch(self) -> webdriver:
        options = chromeOptions()
        
        wd = os.getcwd()
        driver = webdriver.Chrome(options=options, executable_path=f'{wd}/chromedriver.exe')
    
        return driver
        
    def getGmail(self, driver: webdriver):
        driver.get("https://workspace.google.com/intl/tr/gmail/")
    
    def signIn(self, driver: webdriver): 
        signIn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header__aside']/a[@aria-label='Sign into Gmail']"))).click()
        
        time.sleep(2)
        email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
        email.clear()
        email.send_keys(SECRETS.EMAIL) # SECRETS.email
        emailNext = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='identifierNext']/div/button"))).click()
        
        time.sleep(2)
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        password.clear()
        password.send_keys(SECRETS.PASSWORD) # SECRETS.email
        passwordNext = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='passwordNext']/div/button"))).click()
    
        time.sleep(2)
        
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Try another way']"))).click()
        except:
            pass
        
        # take 2FA code from user
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//form/span/section[2]/div//ul/li[2]"))).click()
            code = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel']")))
            code.clear()
            code.send_keys(input('Provide 2FA code: '))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Sonraki']]|//button[span[text()='Next']]"))).click()
        except:
            print('Code is not valid!!')
        
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Şimdi değil']]|//button[span[text()='Not now']]"))).click()
            time.sleep(3)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='İptal']]|//button[span[text()='Cancel']]"))).click()
            time.sleep(3)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Şimdi değil']]|//button[span[text()='Not now']]"))).click()
        except:
            pass
    
    def sendMessage(self, driver: webdriver, receiver: str, subject: str, message: str) -> None:
        createMail = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='navigation']/div/div/div"))).click()
        
        # provide user mail from TopTurkishCompanyContact.txt
        receiverBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@peoplekit-id]")))
        receiverBox.clear()
        receiverBox.send_keys(receiver)
        time.sleep(3)
        
        # this scope should in loop
        # take subject from user input
        subjectBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='subjectbox']")))
        subjectBox.clear()
        subjectBox.send_keys(subject)
        time.sleep(3)
        
        # take definition from user input
        messageBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']")))
        messageBox.clear()
        messageBox.send_keys(message)
        time.sleep(3)
        
        # upload a resume
        uploadAFile = driver.find_element(By.XPATH, "//input[@type='file']")
        uploadAFile.send_keys(f'{os.getcwd()}\TR_AdemHilmiBozkurt.pdf')
        time.sleep(3)
        
        # send mail
        send = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label,'Gönder')]|//div[contains(@aria-label,'Send')]"))).click() 
        time.sleep(5)
        
        
    def sendtoMultipleRecepients(self, driver: webdriver, contacts: [str], subject: str, message: str) -> None:  
        count = 0
        for contact in contacts: 
            if(count != 0 and count% 30 == 0):
                time.sleep(60)
            
            # press new mail
            createMail = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='navigation']/div/div/div"))).click()
            
            # provide user mail from TopTurkishCompanyContact.txt
            receiverBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@peoplekit-id]")))
            receiverBox.clear()
            receiverBox.send_keys(contact)
            time.sleep(3)
            
            # this scope should in loop
            # take subject from user input
            subjectBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='subjectbox']")))
            subjectBox.clear()
            subjectBox.send_keys(subject)
            time.sleep(3)
            
            # take definition from user input
            messageBox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']")))
            messageBox.clear()
            messageBox.send_keys(message)
            time.sleep(3)
            
            # upload a resume
            uploadAFile = driver.find_element(By.XPATH, "//input[@type='file']")
            uploadAFile.send_keys(f'{os.getcwd()}\TR_AdemHilmiBozkurt.pdf')
            time.sleep(3)
            
            # send mail
            send = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label,'Gönder')]|//div[contains(@aria-label,'Send')]"))).click() 
            time.sleep(5)
        
            count+= 1
    
    # finish
    def finish(self, driver: webdriver) -> None:
        driver.quit()