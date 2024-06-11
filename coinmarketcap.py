from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip as pc
import requests
class CoinMarketCap:
    
    def __init__(self,tasks:list):
        if not isinstance(tasks,list):
            raise TypeError('Input Must be a List')
        self.task=tasks
        self.option=webdriver.ChromeOptions()
        self.option.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self.option)
        self.URL='https://coinmarketcap.com/currencies/'
        self.json_output=[]
        

    def get_crypto_details(self,currency):
        self.driver.get(self.URL+currency)
        time.sleep(10)
        stats={}
        self.driver.find_element(by=By.ID,value="onetrust-reject-all-handler").click()
        stats['price']=self.driver.find_element(by=By.CSS_SELECTOR,value="span.sc-d1ede7e3-0.fsQm.base-text").text[1:]
        price_change=self.driver.find_element(by=By.CSS_SELECTOR,value="p.sc-71024e3e-0.sc-58c82cf9-1.ihXFUo.iPawMI")
        if price_change.get_attribute('color')=='red':
            stats['price_change']='-'+price_change.text.split('%')[0]
        else:
            stats['price_change']=price_change.text.split('%')[0]
        stats['market_cap']=self.driver.find_elements(by=By.CSS_SELECTOR,value="dd.sc-d1ede7e3-0.hPHvUM.base-text")[0].text.split('\n')[1][1:].replace(',','')
        stats['market_cap_rank']=self.driver.find_element(by=By.CSS_SELECTOR,value="span.text.slider-value.rank-value").text[1:]
        stats['volume']=self.driver.find_elements(by=By.CSS_SELECTOR,value="dd.sc-d1ede7e3-0.hPHvUM.base-text")[1].text.split('\n')[1][1:].replace(',','')
        stats['volume_rank']=self.driver.find_element(by=By.CSS_SELECTOR,value="span.text.slider-value.rank-value").text[1:]
        stats['volume_change']=self.driver.find_elements(by=By.CSS_SELECTOR,value="dd.sc-d1ede7e3-0.hPHvUM.base-text")[2].text.split('%')[0]
        stats['circulating_supply']=self.driver.find_elements(by=By.CSS_SELECTOR,value='dd.sc-d1ede7e3-0.hPHvUM.base-text')[3].text.split(' ')[0].replace(',','')
        stats['total_supply']=self.driver.find_elements(by=By.CSS_SELECTOR,value='dd.sc-d1ede7e3-0.hPHvUM.base-text')[4].text.split(' ')[0].replace(',','')
        stats['dilute_supply']=self.driver.find_elements(by=By.CSS_SELECTOR,value='dd.sc-d1ede7e3-0.hPHvUM.base-text')[6].text[1:].replace(',','')
        return stats
    def get_contracts(self):
        name=self.driver.find_element(by=By.CSS_SELECTOR,value="span.sc-71024e3e-0.dEZnuB").text[:-1]
        address=self.driver.find_element(by=By.CSS_SELECTOR,value="a.chain-name").get_attribute('href').split('/')[-1]
        return [{'name':name,'address':address}]

    def get_official_links(self):
        link_obj={'Official_link':[],'Socials':[]}
        item_dict={}
        div_ele=self.driver.find_elements(by=By.CSS_SELECTOR,value="div.sc-d1ede7e3-0.jTYLCR")
        for index,i in enumerate(div_ele[1:3]):
            links_list=i.find_elements(by=By.TAG_NAME,value="a")
            for j in links_list:
                item_dict={}
                item_dict['name']=j.text.replace('\n','')
                item_dict['link']=j.get_attribute('href')
                link_obj[(list(link_obj.items()))[index][0]].append(item_dict)
        return link_obj
    def validate_currency(self):
        for i in self.task:
            re=requests.get(self.URL+i.lower())
            print(re.url)
            if re.url!=self.URL+i.lower()+'/':
                return False
            elif re.status_code!=200:
                return False
            else:
                return True
    def get_Json_format(self):
        if self.validate_currency():
            for i in self.task:
                currency_dict={}
                coin_output=self.get_crypto_details(i)
                currency_dict['coin']=i
                coin_output['contracts']=self.get_contracts()
                for key,value in list(self.get_official_links().items()):
                    coin_output[key]=value
                self.driver.quit()
                currency_dict['output']=coin_output
                self.json_output.append(currency_dict)
            return self.json_output
        else:
            print('Not a Valid Input')
            return None

