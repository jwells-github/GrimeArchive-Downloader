# GrimeArchive-Downloader

A Python program to download all of the grime mixes hosted on https://grimearchive.org/

An artist filter may be entered to restrict downloads to mixes that contain specific artists.

A year filter may be entered to restrict downloads to mixes from a given year.

Created with Python Version 3.9.2

## Use

1. Install the Python Package [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) `pip install beautifulsoup4`
2. Run main.py
3. When prompted enter a list of artists separated by commas without spaces (e.g. 'Wiley,Skepta,Dizzee Rascal,JME') to only download mixes from certain artists. A mix that features any of these artists will be downloaded. Alternatively you may leave this field blank to download all mixes
4. When prompted enter a year in the format YYYY (e.g. 2004) to only download mixes from a specific year. Alternatively you may leave this field blank to download mixes from any year
5. Wait whilst the program collects all mixes that match the given filters.
6. Wait whilst the program downloads all mixes gathered.

The ID number of all downloaded mixes are written to a .txt file named OUTPUT-downloadedMixes.txt which is created inside the program's directory when main.py is ran.
Mix ID numbers that are saved in this file will not be downloaded again if the program is rerun.

In order to redownload mixes OUTPUT-downloadedMixes.txt must be deleted, or the specific Mix ID must be removed from the file

## Configuration

### Output Folder

Downloaded mixes are saved in a folder named OUTPUT-GrimeArchiveDownloads/ which is created inside the program's directory when main.py is ran.

The name of this output folder can be altered by changing the OUTPUT_FOLDER_NAME variable in GrimeArchiveDownloader/config.py

### Downloaded Mixes File

The ID number of all downloaded mixes are written to a .txt file named OUTPUT-downloadedMixes.txt which is created inside the program's directory when main.py is ran.

The name of this file can be altered by changing the DOWNLOADED_MIXES_FILE_NAME variable in GrimeArchiveDownloader/config.py

### Number of Threads

By default a maximum of 15 threads are used to scrape mix information from the website and a maximum of 3 threads are used to download mixes.

The maximum number of threads used can be changed by altering MAX_CRAWLER_THREADS and MAX_DOWNLOAD_THREADS respectively in GrimeArchiveDownloader/config.py

## Running Tests

The unit tests for this program are written in tests/tests.py using the Python framework [unittest](https://docs.python.org/3/library/unittest.html#module-unittest)

Test are ran by running `python -m unittest tests.tests` at the command line from within the top level of the program directory
