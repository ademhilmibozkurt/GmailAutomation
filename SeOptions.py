from selenium import webdriver

# from selenium.webdriver.Chrome.service import Service 
# from webdriver_manager.Chrome import ChromeDriverManager
# service=Service(ChromeDriverManager().install())

def chromeOptions(proxy:str= None) -> webdriver.ChromeOptions():
    options = webdriver.ChromeOptions()
    
    prefs = {'profile.default_content_settings_values.notifications':2,
             'page_load_strategy': 'normal',
             'plugins.always_open_pdf_externally': 'True',}
             # 'profile.managed_default_content_settings.javascript': 2} # try disable js

    # options.add_argument('--incognito')
    # options.add_argument('--start-minimized')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-blink-features')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("prefs", prefs)
    options.headless = False
    
    if(proxy != None):
        options.add_argument(f'--proxy-server={proxy}')
    
    return options