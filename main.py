from GrimeArchiveDownloader.get_mixes import get_mixes
from GrimeArchiveDownloader.download_mixes import download_mixes

mixes = get_mixes()
download_mixes(mixes)