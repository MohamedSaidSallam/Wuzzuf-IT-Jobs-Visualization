import json
from pathlib import Path

from Wuzzuf_DataCollection.getjobinfo import getJobInfo

OUTPUT_FOLDER = "output"

jobInfo = getJobInfo()

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

with open(f"{OUTPUT_FOLDER}/job.json", "w") as outputFile:
    json.dump(jobInfo, outputFile)
