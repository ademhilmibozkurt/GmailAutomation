from selenium import webdriver
from Automate import GmailAutomation

def main():
    # create an instance of automation
    auto = GmailAutomation()
    
    # launch driver and sign in to gmail 
    driver: webdriver = auto.launch()
    auto.getGmail(driver)
    auto.signIn(driver)
    
    # import necessary variables
    receiver: str = auto.importReceiver()
    contacts: [str] = auto.importContacts()
    subject: str = auto.importSubject()
    message: str = auto.importMessage()
    pdfForUpload = auto.importPdfForUpload()
    
    # send message
    auto.sendMessage(driver, receiver, subject, message, pdfForUpload)
    
    # send message to all receivers
    # auto.sendtoMultipleRecepients(driver, contacts, subject, message, pdfForUpload)
    
    auto.finish(driver)

if __name__ == '__main__':
    main()