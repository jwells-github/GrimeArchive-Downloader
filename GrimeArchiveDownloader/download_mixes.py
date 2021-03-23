import requests
import os
import concurrent.futures
from .config import Config

def check_duplicate_path_name(filePath: str):
  if not os.path.exists(filePath + '.mp3'):
    return filePath
  counter = 1
  while True:
    appendedFilePath = filePath + " ("+str(counter)+")"
    if not os.path.exists(appendedFilePath + '.mp3'):
      return appendedFilePath
    else:
      counter += 1

def download_mix(mix):
    print('Downloading ' + mix.fileName())
    request = requests.get(Config().DOWNLOAD_URL + mix.id)
    if request.status_code == 404:
      mix.downloadResult = "Broken Link"
      return mix
    outputPath = check_duplicate_path_name(Config().OUTPUT_FOLDER_NAME +"/"+mix.fileName())
    outputPath +='.mp3'  
    with open(outputPath, 'wb') as f:
      f.write(request.content)
      mix.downloadResult = "Download Complete"
      mix.downloadSuccessful = True
      return mix

def create_downloaded_mixes_folder():
  if not os.path.exists(Config().OUTPUT_FOLDER_NAME):
    os.mkdir(Config().OUTPUT_FOLDER_NAME)

def download_mixes(siteMixes):
  create_downloaded_mixes_folder()
  with concurrent.futures.ThreadPoolExecutor(max_workers=Config().MAX_DOWNLOAD_THREADS) as executor:
    future_to_download = {executor.submit(download_mix , mix): mix for mix in siteMixes}
    for future in concurrent.futures.as_completed(future_to_download):
      if future.result().downloadSuccessful:
        downloadedMixesFile = open(Config().DOWNLOADED_MIXES_FILE_NAME, 'a')
        downloadedMixesFile.write(future.result().id +",")
        downloadedMixesFile.close()
      print(future.result().downloadResult)