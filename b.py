from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

ret_file =  open(f'company_data_mid.csv', 'a')
log_file =  open(f'log.txt', 'a')

CHROME_DRIVER = "/usr/lib/chromium-browser/chromedriver"
BASE_URL = "https://www.zaubacorp.com/company-list/"
BASE_URL1 = "https://www.zaubacorp.com/company/"

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--disable-hang-monitor")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)



class companydata:

    def __init__(self):
        self.CIN = ""
        self.Company = ""
        self.Roc = ""
        self.Status = ""
        self.Email = ""
        self.Url = ""
        self.Index = ""

    def to_line_string(self):
        return f"{self.CIN},{self.Company},{self.Roc},{self.Status},{self.Url}\n"

    def to_line_string_result(self):
        return f"{self.CIN},{self.Company},{self.Roc},{self.Status},{self.Email}\n"


def selenium_crawling(url, Index):
    try:
        driver.get(url)
        table_id = driver.find_elements(By.XPATH,'//table[@class="table table-striped col-md-12 col-sm-12 col-xs-12"]/tbody/tr')

        for a in table_id:
            data = companydata()
            col = a.find_elements(By.TAG_NAME, "td")
            data.CIN = col[0].text
            data.Company = col[1].text
            data.Roc = col[2].text
            data.Status = col[3].text
            url = col[1].find_element(By.TAG_NAME, "a").get_attribute('href')
            data.Url = url
            data.Index = str(Index)
            ret_file.write(data.to_line_string())
    except Exception:
        print('error')

if __name__ == "__main__":
    

    if len(sys.argv) != 3:
        print("Usage must equal [from page index] [to page index]")
        exit()


    print("===>>>> Starting Web Scrapping")
    url_country = "https://www.zaubacorp.com/company-list/p-1-company.html"
    # 13332
    for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
        start_time = time.time()
        url_country = BASE_URL + "p-" + str(i) + "-company.html"
        print(f"---> {i}.")
        selenium_crawling(url_country, i)
        log_file.write(f"--> {i}\n")
        print("--- %s seconds ---" % (time.time() - start_time))
        print(f"---> web scraping done for {url_country}")

        
    driver.quit()
    print("===>>>> DONE")