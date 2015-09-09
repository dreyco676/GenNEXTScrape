from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

"""
This script retrieves a listing of all available "Assesment and Growth" files
from http://w20.education.state.mn.us/MDEAnalytics/Data.jsp.

The return value is a list of dictionaries. Each dictionary has the following attributes,
corresponding to the columns of the HTML table:
    testName
    year
    public
    subject
    grade
    document
    dataFiles
    helpFiles

dataFiles is a list of dictionaries. Each dictionary has two attributes: fileType and url.

In addition to the Python modules imported above, this script requires Google Chrome and
the WebDriver for Google Chrome. The WebDriver must be in the current path.
"""

def get_page_info():
    url = 'http://w20.education.state.mn.us/ibi_apps/WFServlet?IBIF_ex=mdea_ddl_driver&TOPICID=1'
    driver = webdriver.Chrome()
    driver.get(url)
    button1 = driver.find_element_by_css_selector('#button1')
    button1.click()
    time.sleep(3)
    driver.switch_to_frame(driver.find_element_by_id('ifReport'))
    html = driver.page_source
    soup = BeautifulSoup(html)
    div = soup.select('div.scrollDiv')[0]

    pageData = []
    for tr in div('tr') [2:]:
        data = tr('td')
        testName = data[0].text.strip()
        year = data[1].text.strip()
        public = data[2].text.strip()
        subject = data[3].text.strip()
        grade = data[4].text.strip()
        document = data[5].text.strip()
        dataFiles = []
        for a in data[6]('a'):
            fileType = a.text.strip()
            url = a['href']
            dataFiles.append(dict(fileType=fileType, url=url))
        helpFiles = []
        for a in data[7]('a'):
            fileType = a.text.strip()
            url = a['href']
            helpFiles.append(dict(fileType=fileType, url=url))
        pageData.append(
            dict(testName = testName,
                 year = year,
                 public = public,
                 subject = subject,
                 grade = grade,
                 document = document,
                 dataFiles = dataFiles,
                 helpFiles = helpFiles))
    driver.close()
    return pageData
    

if __name__ == '__main__':
    info = get_page_info()
    print json.dumps(info, indent=4)
