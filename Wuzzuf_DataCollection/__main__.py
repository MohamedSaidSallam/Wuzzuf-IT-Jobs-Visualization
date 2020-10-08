import requests
import lxml.html
import json
from pathlib import Path

OUTPUT_FOLDER = "output"

JOB_URL = "https://wuzzuf.net/jobs/p/310929-Game-Designer-Cairo-Egypt?l=sp&t=sj&a=search-v3%7Cspbg&o=38"

jobResponse = requests.get(JOB_URL, stream=True)
jobResponse.raise_for_status()
jobResponse.raw.decode_content = True

tree = lxml.html.parse(jobResponse.raw)

jobJson = {}

jobJson["title"] = str(tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/h1')[0].text_content()).strip()
jobJson["Company"] = str(tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[1]/span[1]')[0].text_content()).strip()
jobJson["City"] = str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[1]')[0].text_content()).strip() \
    + str(tree.xpath(
        '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[2]')[0].text_content()).strip()
jobJson["Posted Date"] = tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[2]/time')[0].attrib["datetime"]

for row in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/div[1]/div/table')[0].getchildren():
    for field in row.getchildren():
        innerDL = field.getchildren()[0].getchildren()
        firstIndex = 0
        secondIndex = 1
        if len(innerDL) == 3:
            firstIndex = 1
            secondIndex = 2
        fieldName = innerDL[firstIndex].text_content().strip()
        fieldValue = " ".join(innerDL[secondIndex].text_content().split())
        jobJson[fieldName] = fieldValue

jobJson["Job Roles"] =  [str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/div[2]/div/div')]
jobJson["About The Job"] = '\n'.join([str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/span/ul[1]/li')])
jobJson["Job Requirements"] =  '\n'.join([str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[3]/span/ul/li')])
jobJson["Keywords"] = [str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[3]/div[2]/div/div')]


Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

with open(f"{OUTPUT_FOLDER}/job.json", "w") as outputFile:
    json.dump(jobJson, outputFile)
