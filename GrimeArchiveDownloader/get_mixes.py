import requests
import os
import concurrent.futures
from bs4 import BeautifulSoup
from .columns import Columns
from .download_filter import DownloadFilter
from .mix import Mix
from .config import Config

downloadedMixes = {}

def get_mcs(mixMcs, mixId:str):
  mcs = ""
  if len(mixMcs) > 0 and len(mixMcs) < 4:
    for mc in mixMcs:
      mcs += mc.string + ","
    mcs = mcs[0:(len(mcs)-1)]
  else:
    mixPage = BeautifulSoup(requests.get(Config().MIX_DETAIL_URL + mixId).content, 'html.parser')
    mixItems = mixPage.find_all('div', class_='mix-item')
    for item in mixItems:
      if item.a != None:
        mcs += item.a.string + ","
    mcs = mcs[0:(len(mcs)-1)]
  return mcs

def parse_page(page):
  mixRows = page.find_all('tr', class_='mix-row')
  pageMixes = []
  if len(mixRows) == 0:
    return pageMixes
  for row in mixRows:
    columns = row.find_all('td')
    mixId = columns[Columns.TITLE].a.get('href').split('/')[2]
    title = columns[Columns.TITLE].a.string
    djs = "Unknown DJ" if columns[Columns.DJS].a is None else columns[Columns.DJS].a.string
    date = columns[Columns.DATE].string
    if mixId in downloadedMixes:
      print('Already downloaded ' + mixId + " - " + date + " " + title + " " + djs)
      continue
    mcs = get_mcs(columns[Columns.MCS].find_all('a'), mixId)  
    pageMixes.append(Mix(mixId, title, djs, mcs, date, downloadResult = "", downloadSuccessful= False))
  return pageMixes  

def get_mixes_from_page(pageNumber: int):
  print('Fetching data from page ' + str(pageNumber) + ' of mixes')
  page = BeautifulSoup(requests.get(Config().MIX_TABLE_URL + str(pageNumber)).content, 'html.parser')
  pageMixes = parse_page(page)
  return pageMixes

def get_number_of_pages():
  homePage = BeautifulSoup(requests.get(Config().HOME_PAGE_URL).content, 'html.parser')
  siteStatistics = homePage.find('span', class_='index-count').string
  mixCount = int(siteStatistics)
  numberOfPages = mixCount // Config().MAX_MIXES_PER_PAGE + (mixCount % Config().MAX_MIXES_PER_PAGE > 0)
  return numberOfPages

def create_downloaded_mixes_file():
  if not os.path.exists(Config().DOWNLOADED_MIXES_FILE_NAME):
    open(Config().DOWNLOADED_MIXES_FILE_NAME, 'x')

def get_already_downloaded_mixes():
  global downloadedMixes
  downloadedMixesFile = open(Config().DOWNLOADED_MIXES_FILE_NAME, 'r')
  downloadedMixes = set(downloadedMixesFile.read().split(','))

def get_mixes(downloadFilter: DownloadFilter):
  siteMixes = []
  create_downloaded_mixes_file()
  get_already_downloaded_mixes()
  pageCount = get_number_of_pages()
  with concurrent.futures.ThreadPoolExecutor(max_workers=Config().MAX_CRAWLER_THREADS) as executor:
    future_to_crawl = {executor.submit(get_mixes_from_page, pageNumber): pageNumber for pageNumber in range(35,pageCount+1)}
    for future in concurrent.futures.as_completed(future_to_crawl):
      pageMixes = future.result()
      pageMixes[:] = [mix for mix in pageMixes if downloadFilter.compare_year_filter(mix.date)]
      pageMixes[:] = [mix for mix in pageMixes if downloadFilter.compare_artist_filter(mix.mcs) or downloadFilter.compare_artist_filter(mix.djs)]
      siteMixes.extend(pageMixes)
  return siteMixes
