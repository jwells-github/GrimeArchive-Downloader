import requests
import os
import concurrent.futures
from bs4 import BeautifulSoup
from columns import Columns
from mix import Mix
from config import Config

downloadedMixes = {}

def get_mcs(mixMcs:list[str], mixId:str):
  mcs = ""
  # There are no listed MCs
  if len(mixMcs) == 0:
    return mcs
  # There are MCs, but all can be retrieved from the mix table
  elif len(mixMcs) < 4:
    for mc in mixMcs:
      mcs += mc.string + ","
    return mcs[0:(len(mcs)-1)]
  # There are too many MCs to be listed in the table and Mix detail page must be fetched
  else:
    mixPage = BeautifulSoup(requests.get(Config().MIX_DETAIL_URL + mixId).content, 'html.parser')
    mixItems = mixPage.find_all('div', class_='mix-item')
    for item in mixItems:
      if item.a != None:
        mcs += item.a.string + ","
    return mcs[0:(len(mcs)-1)]

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
  return parse_page(page)

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

def get_mixes():
  siteMixes = []
  create_downloaded_mixes_file()
  get_already_downloaded_mixes()
  pageCount = get_number_of_pages()
  with concurrent.futures.ThreadPoolExecutor(max_workers=Config().MAX_CRAWLER_THREADS) as executor:
    future_to_crawl = {executor.submit(get_mixes_from_page, pageNumber): pageNumber for pageNumber in range(1,pageCount+1)}
    for future in concurrent.futures.as_completed(future_to_crawl):
      siteMixes.extend(future.result())
  return siteMixes
