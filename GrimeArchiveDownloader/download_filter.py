import re

class DownloadFilter:
  def __init__(self,artists=[""], year=""):
    self.artists = artists
    self.year = year

  def compare_year_filter(self, date):  
    if len(self.year) == 0:
      return True
    else:
      return self.year in date
    
  def compare_artist_filter(self, mcs):
    if len(self.artists[0]) == 0:
      print('0 artist length')
      return True
    for artist in self.artists:
      if artist.lower() in mcs.lower():
        print('' + artist.lower() + ' is in ' + mcs.lower())
        return True
    return False