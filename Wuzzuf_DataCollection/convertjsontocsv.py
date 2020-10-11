import json
import os.path
import os
import csv

JOBS_FOLDER = "output/jobs"
OUTPUT_FOLDER = "output"


def makeJobsCSV():
    with open(f"{OUTPUT_FOLDER}/jobs.csv", "w", newline='', encoding='utf-8') as jobsCSV:
        csvWriter = csv.writer(jobsCSV, delimiter=',', escapechar='"')
        csvWriter.writerow(["Key", "Title", "Company", "City", "PostedDate", "ExperienceNeeded", "CareerLevel",
                            "JobType", "Salary", "Vacancies", "Education Level", "About The Job", "Job Requirements"])
        for filename in os.listdir(JOBS_FOLDER):
            if os.path.isfile(os.path.join(JOBS_FOLDER, filename)):
                if os.path.splitext(filename)[1][1:] == 'json':
                    with open(f"{JOBS_FOLDER}/{filename}", "r") as job:
                        jobData = json.load(job)
                        jobData.pop("Keywords", None)
                        jobData.pop("Job Roles", None)
                        jobData['About The Job'] = jobData['About The Job'].replace(
                            '\n', '     ')
                        jobData['Job Requirements'] = jobData['Job Requirements'].replace(
                            '\n', '     ')
                        csvRow = [f"{jobData['title'] + jobData['Company']}"]
                        csvRow.extend(jobData.values())
                        csvWriter.writerow(csvRow)


def makeKeywordsCSV():
    with open(f"{OUTPUT_FOLDER}/keywords.csv", "w", newline='', encoding='utf-8') as keywordsCSV:
        csvWriter = csv.writer(keywordsCSV, delimiter=',', escapechar='"')
        csvWriter.writerow(["Key", "Keyword"])
        for filename in os.listdir(JOBS_FOLDER):
            if os.path.isfile(os.path.join(JOBS_FOLDER, filename)):
                if os.path.splitext(filename)[1][1:] == 'json':
                    with open(f"{JOBS_FOLDER}/{filename}", "r") as job:
                        jobData = json.load(job)
                        for keyword in jobData["Keywords"]:
                            csvWriter.writerow(
                                [f"{jobData['title'] + jobData['Company']}", keyword])


def makeJobrolesCSV():
    with open(f"{OUTPUT_FOLDER}/jobroles.csv", "w", newline='', encoding='utf-8') as jobrolesCSV:
        csvWriter = csv.writer(jobrolesCSV, delimiter=',', escapechar='"')
        csvWriter.writerow(["Key", "Job Roles"])
        for filename in os.listdir(JOBS_FOLDER):
            if os.path.isfile(os.path.join(JOBS_FOLDER, filename)):
                if os.path.splitext(filename)[1][1:] == 'json':
                    with open(f"{JOBS_FOLDER}/{filename}", "r") as job:
                        jobData = json.load(job)
                        for jobRole in jobData["Job Roles"]:
                            csvWriter.writerow(
                                [f"{jobData['title'] + jobData['Company']}", jobRole])


# def makeAllCSVs():
makeJobsCSV()
makeKeywordsCSV()
makeJobrolesCSV()
