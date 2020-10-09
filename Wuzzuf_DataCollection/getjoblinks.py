import time
import lxml.html
import requests

from Wuzzuf_DataCollection.logger import logger

JOBS_LIST_URL = "https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?start={start}"
# this is not an option, it's the increment for the start value in the url
RESAULTS_PER_PAGE = 20

TIME_BETWEEN_REQUESTS = 3


def getJobLinks():
    links = []

    tree = getPageTree(JOBS_LIST_URL.format(start=0))

    limit = int(str(tree.xpath(
        '//*[@id="search-results-container"]/div/p')[0].text_content()).split()[0])
    logger.debug(f"# of jobs = {limit}")


    numberOfLoops = int(limit / RESAULTS_PER_PAGE) + 1

    logger.debug(f"Looping for {numberOfLoops}")
    for i in range(numberOfLoops):
        logger.debug(f"Loop {i}/{numberOfLoops}")
        tree = getPageTree(JOBS_LIST_URL.format(
            start=i * RESAULTS_PER_PAGE))

        for result in tree.xpath('//*[@id="search-results-container"]/div')[0].cssselect("h2"):
            links.append(result.getchildren()[0].attrib["href"])

        logger.debug(f"Going to sleep")
        time.sleep(TIME_BETWEEN_REQUESTS)

    return links


def getPageTree(link):
    jobListResponse = requests.get(link, stream=True)
    jobListResponse.raise_for_status()
    jobListResponse.raw.decode_content = True

    return lxml.html.parse(jobListResponse.raw)
