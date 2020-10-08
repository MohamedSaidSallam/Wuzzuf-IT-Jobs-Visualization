import requests
import lxml.html

JOB_URL = "https://wuzzuf.net/jobs/p/310929-Game-Designer-Cairo-Egypt?l=sp&t=sj&a=search-v3%7Cspbg&o=38"

jobResponse = requests.get(JOB_URL, stream=True)
jobResponse.raise_for_status()
jobResponse.raw.decode_content = True

tree = lxml.html.parse(jobResponse.raw)

jobJson = {}

jobJson["title"] = str(tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/h1')[0].text_content()).strip()
jobJson["Company"] = str(tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[1]/span[1]')[0].text_content()).strip()
jobJson["City"] = str(tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[1]')[0].text_content()).strip() \
    + str(tree.xpath(
        '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[1]/span[2]/span/span[2]')[0].text_content()).strip()
jobJson["Posted Date"] = tree.xpath(
    '/html/body/div[4]/div/div[1]/div[1]/div[1]/div/p[2]/time')[0].attrib["datetime"]

for row in tree.xpath('/html/body/div[4]/div/div[1]/div[2]/div[1]/div/table')[0].getchildren():
    for field in row.getchildren():
        innerDL = field.getchildren()[0].getchildren()
        firstIndex = 0
        secondIndex = 1
        if len(innerDL) == 3:
            firstIndex = 1
            secondIndex = 2
        fieldName = innerDL[firstIndex].text_content().strip()
        fieldValue = " ".join(innerDL[secondIndex].text_content().split())
        jobJson[fieldName] = fieldValue
# "Job Roles": [
# "AbouttheJob": "We are looking for a game designer with a passion for all genres of games, a knack for coding and storytelling, and an understanding of the industry, market, and target audiences.     Game designers can expect to manage teams of programmers, artists, animators, and sound engineers, as well as plan schedules and work with budgets.     Their responsibilities also include developing design and gaming protocols, defining game-play mechanics, coordinating with other game designers, ensuring quality, and meeting with company executives.     Main Job Duties: Creating innovative games for entertainment or education purposes. Conceptualizing and developing characters, rules, settings and stories for new games. Pitching new game ideas to executives and clients. Managing multiple teams and projects. Prototyping new games. Following industry trends and good practices. Monitoring work and cash flows. Developing design and gaming protocols. Doing quality control.",
# "Job Requirements": "Understanding of mobile apps infrastructure    Knowledge of the JavaScript, TypeScript -including ES6+ syntax- and its nuances     Familiarity with native build tools, like XCode, Android Studio, Gradle, ..etc.     Understanding of REST/Graph APIs, the document request model, and offline storage   Experience with third-party libraries and APIs such as Google Maps API, Scandit API, SQLite API, etc.    Rock solid at working with third-party dependencies and debugging dependency conflicts     Experience with Git Source Control.     Good understanding of mobile application design patterns.   Experience connecting/calling RESTful services.   Excellent problem solving, analytical, and troubleshooting skills.  Knowledge of UI/UX design principles and data visualization to create a polished, intuitive user experience is strongly desired.",
# "Keywords": [

print(jobJson)
