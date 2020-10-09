import lxml.html
import requests


def getJobInfo(link):
    jobResponse = requests.get(link, stream=True)
    jobResponse.raise_for_status()
    jobResponse.raw.decode_content = True

    tree = lxml.html.parse(jobResponse.raw)

    jobJson = {}

    try:
        jobJson["title"] = str(tree.xpath(
            '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/h1')[0].text_content()).strip()
        jobJson["Company"] = str(tree.xpath(
            '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[1]/span[1]')[0].text_content()).strip()
        if jobJson["Company"] == "":
            jobJson["Company"] = str(tree.xpath(
                '/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/p[1]/span[1]/a')[0].text_content()).strip()
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
                fieldValue = " ".join(
                    innerDL[secondIndex].text_content().split())
                jobJson[fieldName] = fieldValue

        jobJson["Job Roles"] = [str(role.text_content()).strip() for role in tree.xpath(
            '/html/body/div[4]/div/div[1]/div[2]/div[2]/div/div')]
        jobJson["About The Job"] = '\n'.join([str(role.text_content()).strip(
        ) for role in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/span/ul[1]/li')])
        jobJson["Job Requirements"] = '\n'.join([str(role.text_content()).strip(
        ) for role in tree.xpath('/html/body/div[4]/div/div[1]/div[3]/span/ul/li')])
        jobJson["Keywords"] = [str(role.text_content()).strip() for role in tree.xpath(
            '/html/body/div[4]/div/div[1]/div[3]/div[2]/div/div')]

    except Exception as e:
        print("Failed: link (", link, ") exception (", e.__traceback__, ")")

    return jobJson
