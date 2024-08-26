from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

log_file =  open(f'log_email.txt', 'a')
ret_file =  open(f'company_data_ret.csv', 'a')
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

    def to_line_string_result(self):
        return f"{self.CIN},{self.Company},{self.Roc},{self.Status},{self.Email}\n"

def ret_put_contact_email(url):
    try:
        driver.get(url)
        email = driver.find_element(By.XPATH, "//p[contains(., 'Email ID')]").text.split(' ')[2]
        return email
    except Exception:
        return ""


def update_email(si):
    index = 1
    with open('company_data_mid_1001_2000.csv') as csv:
      lines = csv.readlines()
      for row in lines:
        if index > si:
            start_time = time.time()
            col = row.split(',')
            data = companydata()
            data.CIN = col[0]
            data.Company = col[1]
            data.Roc = col[2]
            data.Status = col[3]
            url = col[4]
            print(url)
            data.Email = ret_put_contact_email(url)
            if data.Email is "":
                index = index + 1
                continue
            ret_file.write(data.to_line_string_result())
            log_file.write(f"--> {index}\n")
            print(f"---> {index}.")
            print("--- %s seconds ---" % (time.time() - start_time))
        index = index + 1

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage must equal [from page index]")
        exit()


    print("===>>>> Starting Web Scrapping")
    update_email(int(sys.argv[1]))
        
    driver.quit()
    print("===>>>> DONE")