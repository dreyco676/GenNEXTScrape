
#This is my test branch
# Python 2.7 code to download the Assessment and Growth reports
# from the Minnesota Department of Education

# Requires the lxml module (pip install lxml)
# Requires the HTML table from the MN Dept of Education site
# TODO: Automate getting this table!


import csv
from lxml import etree
from lxml.cssselect import CSSSelector
import urllib
import os
datafiles = set()
def nice_filename(s):
    return ''.join(x for x in s if x.isalnum() or x in '_- ')

preferences = dict(tab=1, xlsx=2, xls=3, zip=4, txt=5, pdf=6)

parser = etree.HTMLParser()
tree = etree.parse('MDEReports.html', parser)
root = tree.getroot()
rows = root.findall('body/tbody/tr')
docpath = '../doc/'
if not os.path.isdir(docpath):
    os.mkdir(docpath)
datapath = '../data/MNDeptEdu/AssessmentAndGrowth/'
if not os.path.isdir(datapath):
    os.makedirs(datapath)
table = []
for row in rows[2:]:
    data = [td.text.strip() for td in row[:6]]
    test = data[0]
    testdir = datapath + test
    if not os.path.isdir(testdir):
        print 'create directory', testdir
        os.mkdir(testdir)
    nicename = data[5]
    if data[2] != '' and not (data[2] in nicename):
        nicename += ' ' + data[2]
    if data[3] != '' and not (data[3] in nicename):
        nicename += ' ' + data[3]
    nicename = nice_filename(nicename)

    for idx in (6,7):
        rank = 7
        url = fmt = ''

        for a in row[idx].findall('a'):
            newfmt = a.text.strip()
            newrank = preferences.get(newfmt, 7)
            if newrank < rank:
                rank = newrank
                fmt = newfmt
                url = a.get('href')

        
        if fmt != '':
            if idx == 6:
                path = datapath + test + '/'
            else:
                path = docpath
                
            filename = path + nicename + '.' + fmt
            if not os.path.isfile(filename):
                print 'download', url
                print 'save to', filename
                urllib.urlretrieve(url, filename)
        
            if idx == 6:
                datafiles.add(filename)
            
            
