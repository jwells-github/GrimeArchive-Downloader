import unittest
from bs4 import BeautifulSoup
from GrimeArchiveDownloader.get_mixes import get_mcs
from GrimeArchiveDownloader.mix import Mix
from GrimeArchiveDownloader.mix import remove_illegal_characters
from GrimeArchiveDownloader.download_filter import DownloadFilter

class tests(unittest.TestCase):
  def test_get_mcs_with_length_zero_returns_empty_string(self):
    data = []
    result = get_mcs(data, "testId")
    self.assertEqual(result, "")

  def test_get_mcs_with_length_three_returns_comma_seperated_string(self):
    data = [BeautifulSoup("<a>Skepta</a>", "html.parser"),
            BeautifulSoup("<a>Big H</a>", "html.parser"),
            BeautifulSoup("<a>Demon</a>", "html.parser")]
    result = get_mcs(data, "testId")
    self.assertEqual(result, "Skepta,Big H,Demon")

  def test_get_mcs_with_length_greather_than_three(self):
    # Mix URL: https://grimearchive.org/mix/4357405
    data = [BeautifulSoup("<a>Meridian dan</a>", "html.parser"),
            BeautifulSoup("<a>Big H</a>", "html.parser"),
            BeautifulSoup("<a>JME</a>", "html.parser"),
            BeautifulSoup("<a>more</a>", "html.parser")]
    result = get_mcs(data,"4357405")
    self.assertEqual(result, "Meridian Dan,Big H,JME,President T,Meridian")

  def test_mix_filename(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "Skepta,Big H,Demon", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.file_name()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ft. Skepta, Big H, Demon")

  def test_mix_filename_date_replacement(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "Skepta,Big H,Demon", "??/??/2012", downloadResult = "", downloadSuccessful= False)
    result = data.file_name()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ft. Skepta, Big H, Demon")

  def test_mix_filename_with_unknown_dj(self):
    data = Mix("1", "MixTitle", "Unknown DJ", "Skepta,Big H,Demon", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.file_name()
    self.assertEqual(result,"2012 - MixTitle ft. Skepta, Big H, Demon")

  def test_mix_filename_with_no_mcs(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.file_name()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ")

  def test_mix_removeIllegalCharacters(self):
    data = "a\\b/c:d\"e*f?g|h<i>j"
    result = remove_illegal_characters(data)
    self.assertEqual(result,"a_b_c_d_e_f_g_h_i_j")

  def test_download_year_filter_matches_date(self):
    data = DownloadFilter('','2002')
    result = data.compare_year_filter('2002')
    self.assertTrue(result)

  def test_no_download_year_filter_returns_true(self):
    data = DownloadFilter('','')
    result = data.compare_year_filter('2002')
    self.assertTrue(result)
  
  def test_download_year_filter_does_not_match_different_dates(self):
    data = DownloadFilter('','2002')
    result = data.compare_year_filter('2004')
    self.assertFalse(result)

  def test_download_artist_filter_matches_artists(self):
    data = DownloadFilter(['Skepta','Big H','Demon'],'')
    self.assertTrue(data.compare_artist_filter('Skepta'))
    self.assertTrue(data.compare_artist_filter('big h'))
    self.assertTrue(data.compare_artist_filter('deMon'))
    self.assertTrue(data.compare_artist_filter('JME,President T,Bruza,Skepta,Big Zuu,Flirta D'))

  def test_no_download_artist_filter_returns_true(self):
    data = DownloadFilter([''],'') 
    self.assertTrue(data.compare_artist_filter('Skepta'))

  def test_download_artist_filter_does_match_different_artists(self):
    data = DownloadFilter(['Skepta','Big H','Demon'],'')
    self.assertFalse(data.compare_artist_filter('Wiley')) 
    self.assertFalse(data.compare_artist_filter('JME,President T,Bruza,Big Zuu,Flirta D'))

if __name__ == '__main__':
    unittest.main()