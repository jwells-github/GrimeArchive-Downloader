from GrimeArchiveDownloader.get_mixes import get_mixes
from GrimeArchiveDownloader.download_mixes import download_mixes
from GrimeArchiveDownloader.download_filter import DownloadFilter

downloadFilter = DownloadFilter()
downloadFilter.artists = input("Only download mixes containing this artist: ").split(',')
yearFilter = ""
yearFilterValid = False
while(not yearFilterValid):
  yearFilter = input("Only download mixes from this year: ")
  if len(yearFilter) == 0 or len(yearFilter) == 4:
    yearFilterValid = True
  else:
    print("Date must match yyyy format, e.g. '2020'")
downloadFilter.year = yearFilter
mixes = get_mixes(downloadFilter)
download_mixes(mixes)