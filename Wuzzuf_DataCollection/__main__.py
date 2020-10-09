import json
import os.path
import time
from pathlib import Path

from Wuzzuf_DataCollection.getjobinfo import getJobInfo
from Wuzzuf_DataCollection.getjoblinks import getJobLinks

OUTPUT_FOLDER = "output"
OUTPUT_LINKS_FILE = f"{OUTPUT_FOLDER}/links.json"
TIME_BETWEEN_REQUESTS = 2.5

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

if os.path.isfile(OUTPUT_LINKS_FILE):
    print("Links file found")
    with open(OUTPUT_LINKS_FILE, "r") as outputFile:
        jobLinks = json.load(outputFile)
else:
    jobLinks = getJobLinks()

    with open(OUTPUT_LINKS_FILE, "w") as outputFile:
        json.dump(jobLinks, outputFile)


for i, link in enumerate(jobLinks):
    print(f"Job # {i}")
    jobInfo = getJobInfo(link)

    time.sleep(TIME_BETWEEN_REQUESTS)

    with open(f"{OUTPUT_FOLDER}/{i}.json", "w") as outputFile:
        json.dump(jobInfo, outputFile)
