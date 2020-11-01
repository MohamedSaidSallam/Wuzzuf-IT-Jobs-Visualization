import argparse
import json
import os
import os.path
import time
import zipfile
from datetime import datetime
from pathlib import Path

from Wuzzuf_DataCollection.convertjsontocsv import createCSVs
from Wuzzuf_DataCollection.getjobinfo import getJobInfo
from Wuzzuf_DataCollection.getjoblinks import getJobLinks
from Wuzzuf_DataCollection.logger import logger

OUTPUT_FOLDER = "output"
JOBS_OUTPUT_FOLDER = f"{OUTPUT_FOLDER}/jobs"
OUTPUT_LINKS_FILE = f"{OUTPUT_FOLDER}/links.json"
TIME_BETWEEN_REQUESTS = 2.5


def formattedJsonDumps(data, file):
    json.dump(data, file, indent=4, sort_keys=True)


def main(use_existing_Links_file, linksStartIndex, linksEndIndex, skipCreateCSV, skipGetJobInfo):
    logger.debug("Started")

    logger.debug(f"create output folder if not present @ {OUTPUT_FOLDER}")
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    logger.debug(
        f"create jobs output folder if not present @ {JOBS_OUTPUT_FOLDER}")
    Path(JOBS_OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    if use_existing_Links_file:
        if os.path.isfile(OUTPUT_LINKS_FILE):
            logger.debug(f"using Existing Links JSON")
            with open(OUTPUT_LINKS_FILE, "r") as outputFile:
                jobLinks = json.load(outputFile)
        else:
            logger.critical(f"links JSON file not found @{OUTPUT_LINKS_FILE}")
            exit(-1)
    else:
        logger.debug(f"getting jobs links")
        jobLinks = getJobLinks()

        logger.debug(f"writing job {OUTPUT_LINKS_FILE}")
        with open(OUTPUT_LINKS_FILE, "w") as outputFile:
            formattedJsonDumps(jobLinks, outputFile)

    if skipGetJobInfo:
        if linksEndIndex == -1:
            linksEndIndex = len(jobLinks)

        if linksStartIndex > len(jobLinks) or linksEndIndex > len(jobLinks):
            logger.critical(
                f"Invalid job index linksStartIndex: {linksStartIndex}, linksEndIndex: {linksEndIndex}, length of job links: {len(jobLinks)}")
            exit(-1)

        logger.debug(
            f"going through links list from {linksStartIndex} to {linksEndIndex}")
        for i, link in enumerate(jobLinks[linksStartIndex:linksEndIndex]):
            logger.debug(f"Getting Info for Job # {i}(real index={linksStartIndex+i})/{linksEndIndex-linksStartIndex}")
            jobInfo = getJobInfo(link)

            logger.debug(f"Going to sleep")
            time.sleep(TIME_BETWEEN_REQUESTS)

            logger.debug(f"Writing File to {JOBS_OUTPUT_FOLDER}/{linksStartIndex+i}.json")
            with open(f"{JOBS_OUTPUT_FOLDER}/{linksStartIndex+i}.json", "w") as outputFile:
                formattedJsonDumps(jobInfo, outputFile)
    else:
        logger.debug(f"creating job info JSON was disabled by command args")

    if skipCreateCSV:
        logger.debug(f"creating CSVs")
        createCSVs()
    else:
        logger.debug(f"creating CSV was disabled by command args")

    logger.debug("archiving output")

    outputArchiveName= f"{datetime.today().strftime('%Y-%m-%d')}.zip"

    with zipfile.ZipFile( OUTPUT_FOLDER +'/'+ outputArchiveName, 'w', zipfile.ZIP_DEFLATED) as outputZip:
        for root, _, files in os.walk(OUTPUT_FOLDER):
            for file in files:
                fileExtension = os.path.splitext(file)[1][1:]
                if fileExtension == 'csv' or fileExtension == 'json':
                    fileToArchive = os.path.join(root, file)
                    outputZip.write(fileToArchive, arcname=os.path.join(root[len(OUTPUT_FOLDER):], file))
                    os.remove(fileToArchive)

    logger.debug(f"output archived to {outputArchiveName}")

    logger.debug("DONE!!")


parser = argparse.ArgumentParser(
    description=("Gets the list of Job offers on wuzzuf.com for it, gets the details of each offer then generates a CSV file with all the jobs"
                 "\nWarning: the output file is overwritten with each run!!"),
    epilog="https://github.com/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization"
)

parser.add_argument("-l", "--use-existing-Links-file",
                    help="Use the existing links JSON file (default: %(default)s)",
                    default=False,
                    action="store_true")


def positiveInt(string):
    value = int(string)
    if value < 0:
        raise argparse.ArgumentTypeError(
            f"{string} is not a index (not a positive integer)")
    return value


parser.add_argument("-i", "--start-index",
                    help="Start index in links JSON to start getting job info (Inclusive, default: %(default)s)",
                    default=0,
                    type=positiveInt,
                    action="store")

parser.add_argument("-e", "--end-index",
                    help="Start index in links JSON to start getting job info (Exclusive)",
                    default=-1,
                    type=positiveInt,
                    action="store")

parser.add_argument("-c", "--skip-create-csv",
                    help="Create CSV files combining data from Job JSONs (default: %(default)s)",
                    default=False,
                    action="store_true")

parser.add_argument("-f", "--skip-get-jobs-info",
                    help="Create JSON files for each job (or jobs within the start and end index if specified) in links JSON file (default: %(default)s)",
                    default=False,
                    action="store_true")

args = parser.parse_args()

if args.end_index != -1 and args.start_index >= args.end_index:
    logger.critical(
        "end index ({args.end_index}) is smaller than or equal start index ({args.start_index})")
    exit(-1)


main(
    use_existing_Links_file=args.use_existing_Links_file,
    linksStartIndex=args.start_index,
    linksEndIndex=args.end_index,
    skipCreateCSV=not args.skip_create_csv,
    skipGetJobInfo=not args.skip_get_jobs_info,
)
