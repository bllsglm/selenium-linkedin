from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import credentials
from parsel import Selector
import csv

writer=csv.writer(open(credentials.result_file,'w'))
writer.writerow(['name','job','Location','ln_url','summary'])


driver=webdriver.Chrome('/home/billsglm/Desktop/Chrome_Driver/chromedriver')

driver.get('https://www.linkedin.com/')
sleep(5)

driver.maximize_window()
sleep(2)

driver.find_element_by_xpath('//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]').click()
sleep(3)

username_input=driver.find_element_by_xpath('//input[@id="username"]')
username_input.send_keys(credentials.username)
sleep(0.5)

username_password=driver.find_element_by_xpath('//input[@name="session_password"]')
username_password.send_keys(credentials.password)
sleep(0.5)

driver.find_element_by_xpath('//button[text()="Sign in"]').click()

#at this point, logged in 


driver.get('https://www.google.com/')
sleep(3)


driver.find_element_by_xpath('//*[@name="q"]').click()
sleep(3)

search_input=driver.find_element_by_xpath('//*[@name="q"]')
search_input.send_keys(credentials.search_query)
sleep(1)

search_input.send_keys(Keys.RETURN)
sleep(3)

profiles=driver.find_elements_by_xpath('//div[@id="search"]/div/div/div/div/div/div/div/a|//div[@id="search"]/div/div/div/div/div/div/div/div/a')
profiles=[profile.get_attribute('href') for profile in profiles]
for profile in profiles:
	driver.get(profile)
	sleep(5)
	sel=Selector(text=driver.page_source)
	name=sel.xpath('//title/text()').extract_first().split(" | ")[0]
	job = sel.xpath('//*[contains(@class,"text-body-medium break-words")]/text()').extract_first().strip()
	Location= sel.xpath('//*[contains(@class,"text-body-small inline t-black--light break-words")]/text()').extract_first().strip()
	ln_url= driver.current_url
	summary = sel.xpath('//span[contains(@class,"mr1 hoverable-link-text t-bold")]/span[1]/text()').extract()
	
	
	print('\n')
	print(name)
	print(job)
	print(Location)
	print(ln_url)
	print(summary)
	print('\n')
	
	writer.writerow([name,job,Location,ln_url,summary])
	
	
driver.quit()

