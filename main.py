from GrimeArchiveDownloader.get_mixes import get_mixes
from GrimeArchiveDownloader.download_mixes import download_mixes
from GrimeArchiveDownloader.download_filter import DownloadFilter

def get_artist_filter():
  print('Enter the names of any artists that you would like to download mixes for')
  print('Names should be seperated by commas without spaces e.g. Skepta,Big H,Wiley')
  print('You may leave this field blank to download mixes from any artist')
  return input("Only download mixes containing these artists: ").split(',')

def get_year_fiter():
  print('Enter the year that you would like to download mixes from, e.g. 2004')
  print('You may leave this field blank to download mixes from any year')
  yearFilter = ""
  yearFilterValid = False
  while(not yearFilterValid):
    yearFilter = input("Only download mixes from this year: ")
    if len(yearFilter) == 0 or len(yearFilter) == 4:
      yearFilterValid = True
    else:
      print("Date must match yyyy format, e.g. '2020'")
  return yearFilter

print('Grime Archive Downloader:')
downloadFilter = DownloadFilter()
downloadFilter.artists = get_artist_filter()
print()
downloadFilter.year = get_year_fiter()
mixes = get_mixes(downloadFilter)
download_mixes(mixes)