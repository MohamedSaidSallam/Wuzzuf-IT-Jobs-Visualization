# Wuzzuf IT Jobs Visualization

[![GitHub Release][github_release_badge]][github_release_link]
[![License][license-image]][license-url]

Data Collection and visualization for jobs offered under the IT section on [Wuzzuf](wuzzuf.net) for educational and statistical purposes.

> DISCLAIMER: Wuzzuf doesn't offer an open API to obtain the required data for the visualization and as such a web scraper ***with a delay between requests*** was used to obtain the data

## Visualization

You can view the whole visualization on [Tableau public](https://public.tableau.com/views/WuzzufITOffersVisualization/MainDashboard?:language=en&:display_count=y&:origin=viz_share_link)

![Visualization Screenshot](doc/Viz_1.png)
![Visualization Screenshot](doc/Viz_2.png)
![Visualization Screenshot](doc/Viz_3.png)
![Visualization Screenshot](doc/Viz_4.png)
![Visualization Screenshot](doc/Viz_5.png)

## Download Data

You can download previously collected data from this [drive][data-drive]. It should be updated every month (or a couple of month) so check back from time to time.

Side Note: if you are going to combine multiple zip files keep in mind that there might be an overlap because a job offer might have lasted for longer than a month.

## Installation

Don't forget to install the required modules. (unless ofcourse you are going to use docker)

```bash
pip install -r requirements.txt
```

## Usage

To obtain the data. Run the python module as follows:

> Note that because of the delay added between requests the script will take a long time to gather the data. Please be responsible and don't remove the delay.

You can also download some older data in the [Download Data](#download-data) Section.

```bash
py -m Wuzzuf_DataCollection
```

There are also command args available which you can view with:

```bash
$ py -m Wuzzuf_DataCollection --help

usage: __main__.py [-h] [-l] [-i START_INDEX] [-e END_INDEX] [-c] [-f] [-a]

Gets the list of Job offers on wuzzuf.com for it, gets the details of each offer then generates a CSV file with all the jobs and then archives the output to a zip file Warning: the output file is
overwritten with each run!!

optional arguments:
  -h, --help            show this help message and exit
  -l, --use-existing-Links-file
                        Use the existing links JSON file (default: False)
  -i START_INDEX, --start-index START_INDEX
                        Start index in links JSON to start getting job info (Inclusive, default: 0)
  -e END_INDEX, --end-index END_INDEX
                        Start index in links JSON to start getting job info (Exclusive)
  -c, --skip-create-csv
                        skip creating CSV files combining data from Job JSONs (default: False)
  -f, --skip-get-jobs-info
                        skip creating JSON files for each job (or jobs within the start and end index if specified) in links JSON file (default: False)
  -a, --skip-archive    Skip creating an archive for the output and deleting the current output (default: False)

https://github.com/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization
```

### Using docker

A docker file and a docker compose are present in the repo. So you can easly start the script using:

```bash
docker-compose up
```

## Deployement

If you are going to deploy the script to run periodicly. (Another reminder that you can download the data in the [Download Data](#download-data) Section) Use the following line to add it to the cron tab. Change the parameters to match your machine.

```bash
(crontab -l 2>/dev/null; echo "0 0 1 * * cd /home/ec2-user/Wuzzuf-IT-Jobs-Visualization && docker-compose up") | crontab -
 ```

## Built With

* [Tableau Public](https://public.tableau.com) - Data Visualization tool
* [Visual Studio Code](https://code.visualstudio.com/) - Code Editor
* [Docker](https://www.docker.com/) - Containerization

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository][github-tags].

## Authors

* **Mohamed Said Sallam** - Main Dev - [TheDigitalPhoenixX](https://github.com/TheDigitalPhoenixX)
* **Sameh Amnoun** - Main Dev - [SamehAmnoun](https://github.com/SamehAmnoun)

See also the list of [contributors][github-contributors] who participated in this project and their work in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [README.md Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

[license-image]: https://img.shields.io/badge/License-MIT-brightgreen.svg
[license-url]: https://opensource.org/licenses/MIT

[github_release_badge]: https://img.shields.io/github/v/release/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization.svg?style=flat&include_prereleases
[github_release_link]: https://github.com/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization/releases

[github-contributors]: https://github.com/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization/contributors
[github-tags]: https://github.com/TheDigitalPhoenixX/Wuzzuf-IT-Jobs-Visualization/tags

[data-drive]: https://drive.google.com/drive/folders/19DFHc4DF35bMF_mOlFGV1cd8hvQOCVeM?usp=sharing
