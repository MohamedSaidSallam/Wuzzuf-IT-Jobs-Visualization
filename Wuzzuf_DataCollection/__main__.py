import json
from pathlib import Path

from Wuzzuf_DataCollection.getjobinfo import getJobInfo
from Wuzzuf_DataCollection.getjoblinks import getJobLinks

OUTPUT_FOLDER = "output"

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

jobLinks = getJobLinks()

with open(f"{OUTPUT_FOLDER}/links.json", "w") as outputFile:
    json.dump(jobLinks, outputFile)


for i, link in enumerate(jobLinks):
    jobInfo = getJobInfo(link)

    with open(f"{OUTPUT_FOLDER}/{i}.json", "w") as outputFile:
        json.dump(jobInfo, outputFile)
