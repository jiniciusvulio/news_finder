from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import os
import sys

app_path = os.path.dirname(sys.executable)

now = datetime.now()
ymd = now.strftime("%Y%m%d")

website = "https://news.un.org/pt/news/topic/climate-change"
path = "%USERPROFILE%/chromedriver/chromedriver.exe"

sel_options = Options()
sel_options.add_argument("--headless=new")
sel_options.add_argument('--ignore-certificate-errors')
sel_options.add_argument('--ignore-ssl-errors')
sel_service = Service(executable_path= path)
driver = webdriver.Chrome(service= sel_service, options= sel_options)
driver.get(website)

containers = driver.find_elements(by= "xpath", value='//article')

titles= []
summaries = []
links= []

for container in containers:    
    title = container.find_element(by= "xpath", value= './div/div[@class="col-lg-7"]/header/h2/a/span').text
    summary = container.find_element(by= "xpath", value= './div/div[@class="col-lg-7"]/div/div/p').text
    link = container.find_element(by= "xpath", value= './div/div[@class="col-lg-7"]/header/h2/a').get_attribute("href")

    titles.append(title)
    summaries.append(summary)
    links.append(link)

dict = {'titles': titles, 'summaries': summaries, 'links': links}
headlines = pd.DataFrame(dict)
filename = f'headlines_{ymd}.csv'

file_path = os.path.join(app_path, filename)

headlines.to_csv(file_path)

driver.quit()
