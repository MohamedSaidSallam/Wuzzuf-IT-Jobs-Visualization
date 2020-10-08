import requests
import lxml.html

JOB_URL = "https://wuzzuf.net/jobs/p/310929-Game-Designer-Cairo-Egypt?l=sp&t=sj&a=search-v3%7Cspbg&o=38"

jobResponse = requests.get(JOB_URL, stream=True)
jobResponse.raise_for_status()
jobResponse.raw.decode_content = True

tree = lxml.html.parse(jobResponse.raw)

jobJson = {}

jobJson["title"] =  str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/h1')[0].text_content()).strip()
jobJson["Company"] =  str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[1]/span[1]')[0].text_content()).strip()
jobJson["City"] =  str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[1]')[0].text_content()).strip() + str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[2]')[0].text_content()).strip()
# "PostedDate": "2020-10-06T18:16:48+02:00",
# "ExperienceNeeded": "4 to 7 years",
# "CareerLevel": "Experienced (Non-Manager)",
# "JobType": "Full Time",
# "Salary": "Confidential",
# "Vacancies": "4 open positions",
# "EducationLevel": "Bachelor's Degree",
jobJson["Job Roles"] =  [str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/div[2]/div/div')]
jobJson["About The Job"] = '\n'.join([str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/span/ul[1]/li')])
jobJson["Job Requirements"] =  '\n'.join([str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[3]/span/ul/li')])
jobJson["Keywords"] = [str(role.text_content()).strip() for role in tree.xpath('/html/body/div[4]/div/div[1]/div[3]/div[2]/div/div')]

print(jobJson)