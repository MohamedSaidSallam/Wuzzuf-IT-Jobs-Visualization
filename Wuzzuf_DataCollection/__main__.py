import json
import os.path
import time
from pathlib import Path

from Wuzzuf_DataCollection.getjobinfo import getJobInfo
from Wuzzuf_DataCollection.getjoblinks import getJobLinks
from Wuzzuf_DataCollection.logger import logger

JOBS_OUTPUT_FOLDER = "output/jobs"
OUTPUT_LINKS_FILE = f"{JOBS_OUTPUT_FOLDER}/links.json"
TIME_BETWEEN_REQUESTS = 2.5

logger.debug("Started")

logger.debug(f"create output folder if not present @ {JOBS_OUTPUT_FOLDER}")
Path(JOBS_OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

if os.path.isfile(OUTPUT_LINKS_FILE):
    logger.debug(f"{OUTPUT_LINKS_FILE} found")
    with open(OUTPUT_LINKS_FILE, "r") as outputFile:
        jobLinks = json.load(outputFile)
else:
    logger.debug(f"{OUTPUT_LINKS_FILE} not found; getting links")
    jobLinks = getJobLinks()

    logger.debug(f"writing {OUTPUT_LINKS_FILE}")
    with open(OUTPUT_LINKS_FILE, "w") as outputFile:
        json.dump(jobLinks, outputFile)


logger.debug(f"going t {OUTPUT_LINKS_FILE}")
for i, link in enumerate(jobLinks[1208:]):
    logger.debug(f"Getting Info for Job # {i+1}/{len(jobLinks)}")
    jobInfo = getJobInfo(link)

    logger.debug(f"Going to sleep")
    time.sleep(TIME_BETWEEN_REQUESTS)

    logger.debug(f"Writing File to {JOBS_OUTPUT_FOLDER}/{i}.json")
    with open(f"{JOBS_OUTPUT_FOLDER}/{i}.json", "w") as outputFile:
        json.dump(jobInfo, outputFile)

logger.debug(f"DONE!")
