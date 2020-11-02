import traceback
from time import sleep

import lxml.html
import requests
from lxml.etree import tostring

from Wuzzuf_DataCollection.logger import logger

RETRY_SLEEP_TIME = 3

class GetJobInfoFailedException(Exception):
    pass

def getJobInfo(link, isRetry=False):
    jobResponse = requests.get(link, stream=True)
    jobResponse.raise_for_status()
    jobResponse.raw.decode_content = True

    tree = lxml.html.parse(jobResponse.raw)

    jobJson = {}

    logger.debug(f"Getting info for {link}")
    jobJson["link"] = link
    try:
        jobJson["title"] = ''.join(tree.xpath(
            '//h1[@class="job-title"]/text()')).strip()
        jobJson["Company"] = tree.xpath(
            '//*[@class="job-company-name"]/text()')[0].strip()
        jobJson["City"] = ''.join([span.text_content() for span in tree.xpath(
            '//span[@class="job-company-location"]')[0]]).strip()
        jobJson["Posted Date"] = tree.xpath(
            '//p[@class="job-post-date"]')[0].getchildren()[0].attrib["datetime"]

        for field in tree.xpath('//table[@class="table"]/tr/td/dl'):
            fieldTitle = field.xpath('.//dt/text()')[0].strip()[:-1]
            fieldValue = field.xpath('.//dd')[0]
            if len((children := fieldValue.getchildren())) == 1:
                jobJson[fieldTitle] = children[0].text_content().strip()
            else:
                jobJson[fieldTitle] = ' '.join(
                    fieldValue.text_content().split()).strip()

        jobJson["Job Roles"] = [item.strip() for item in tree.xpath(
            '//div[@class="about-job content-card"]')[0].xpath('.//div[@class="keyword-matching-labels"]/a/text()')]
        jobJson["About The Job"] = tostring(tree.xpath(
            '//span[@itemprop="description"]')[0]).decode("utf-8")
        jobJson["Job Requirements"] = tostring(jobreq[0]).decode(
            "utf-8") if len((jobreq := tree.xpath('//span[@itemprop="responsibilities"]'))) != 0 else ""
        jobJson["Keywords"] = [item.strip() for item in tree.xpath(
            '//div[@class="job-requirements content-card"]')[0].xpath('.//div[@class="keyword-matching-labels"]/a/text()')]

    except Exception:
        logger.error(
            f"Failed to get Job info: link ({link}), Exception ({traceback.format_exc()})")
        if isRetry:
            logger.error(f"Retry Failed; skipping job ({link})")
            raise GetJobInfoFailedException
        else:
            logger.debug(f"Retrying after sleeping for {RETRY_SLEEP_TIME}s")
            sleep(RETRY_SLEEP_TIME)
            jobJson=getJobInfo(link, True)

    return jobJson
