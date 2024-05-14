import requests
import io
from bs4 import BeautifulSoup
from pypdf import PdfReader

# Creates list of pdfs of passing candidate names from SOA website
pdfs = []
for i in range(8):
    i = str(i + 1)
    url = 'https://www.soa.org/education/exam-results/?crgTh6VCO0qGRV7-page='+i
    r = requests.get(url) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    anchors = soup.find_all('a')
    for link in anchors: 
        if "names" in link.get('href', []):
            path = link.get('href', [])
            i = 'https://www.soa.org'+link.get('href')
            pdfs.append(i)


# Initalize list of names and exams
names = ["Dailey, Ethan", "Reiley, Rory", "Bauer, Morgan", "Greiner, Autumn", "Bours Jr., Jeremy",
         "Baker, Mason", "Halecki, Luke", "Kline, Emily", "Rahtjen, Peter", "Schleicher, Jacob",
         "Rosselli, Carmen", "Stanavage, Petra", "Bugda, Ezekiel", "Bieniakowski, David", "Leight, Abigail"]
exams = {}

# Iterate over each pdf and grab exam name
for doc in pdfs:
    once = True
    res = [dash for dash in range(len(doc)) if doc.startswith('-', dash)]
    exam_date = doc[res[1]+1:res[4]]
    exam = doc[res[3]+1:res[4]]
    r = requests.get(doc)
    f = io.BytesIO(r.content)
    reader = PdfReader(f)
    num = len(reader.pages)

    # Iterate over each page in pdf
    passed = []
    for page_num in range(num):
        page = reader.pages[page_num].extract_text()
        
        # Check for each name on the page
        for name in names:
            if name in page:
                passed.append(name)
    
    # Add list of passed names to exams dictionary
    if passed:
        """Uncomment line below to see names by sitting"""
        #print(exam_date,passed)
        if exam in exams.keys():
            exams[exam].append(passed)
        else:
            exams[exam] = [passed]

# Make each exam be a consolidated list
for exam in exams:
    updated = [x for xs in exams[exam] for x in xs]
    exams[exam] = updated

print(exams)