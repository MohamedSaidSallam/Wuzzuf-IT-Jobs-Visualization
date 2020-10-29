import json
import os.path
import time
from pathlib import Path

from Wuzzuf_DataCollection.getjobinfo import getJobInfo
from Wuzzuf_DataCollection.getjoblinks import getJobLinks
from Wuzzuf_DataCollection.logger import logger

OUTPUT_FOLDER = "output"
JOBS_OUTPUT_FOLDER = f"{OUTPUT_FOLDER}/jobs"
OUTPUT_LINKS_FILE = f"{OUTPUT_FOLDER}/links.json"
TIME_BETWEEN_REQUESTS = 2.5

def formattedJsonDumps(data, file):
    json.dump(data, file, indent=4, sort_keys=True)

logger.debug("Started")

logger.debug(f"create output folder if not present @ {OUTPUT_FOLDER}")
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
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
        formattedJsonDumps(jobLinks, outputFile)


logger.debug(f"going through links list")
for i, link in enumerate(jobLinks):
    logger.debug(f"Getting Info for Job # {i}/{len(jobLinks)}")
    jobInfo = getJobInfo(link)

    logger.debug(f"Going to sleep")
    time.sleep(TIME_BETWEEN_REQUESTS)

    logger.debug(f"Writing File to {JOBS_OUTPUT_FOLDER}/{i}.json")
    with open(f"{JOBS_OUTPUT_FOLDER}/{i}.json", "w") as outputFile:
        formattedJsonDumps(jobInfo, outputFile)

logger.debug(f"DONE!!")
