import unittest
from bs4 import BeautifulSoup
from GrimeArchiveDownloader.get_mixes import get_mcs
from GrimeArchiveDownloader.mix import Mix
from GrimeArchiveDownloader.mix import removeIllegalCharacters

class tests(unittest.TestCase):
  def test_get_mcs_with_zero_length_returns_empty_string(self):
    data = []
    result = get_mcs(data, "testId")
    self.assertEqual(result, "")

  def test_get_mcs_with_three_length_returns_comma_seperated_string(self):
    data = [BeautifulSoup("<a>Skepta</a>", "html.parser"),
            BeautifulSoup("<a>Big H</a>", "html.parser"),
            BeautifulSoup("<a>Demon</a>", "html.parser")]
    result = get_mcs(data, "testId")
    self.assertEqual(result, "Skepta,Big H,Demon")

  def test_mix_filename(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "Skepta,Big H,Demon", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.fileName()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ft. Skepta, Big H, Demon")

  def test_mix_filename_date_replacement(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "Skepta,Big H,Demon", "??/??/2012", downloadResult = "", downloadSuccessful= False)
    result = data.fileName()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ft. Skepta, Big H, Demon")

  def test_mix_filename_with_unknown_dj(self):
    data = Mix("1", "MixTitle", "Unknown DJ", "Skepta,Big H,Demon", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.fileName()
    self.assertEqual(result,"2012 - MixTitle ft. Skepta, Big H, Demon")

  def test_mix_filename_with_no_mcs(self):
    data = Mix("1", "MixTitle", "DJ Spooky", "", "2012", downloadResult = "", downloadSuccessful= False)
    result = data.fileName()
    self.assertEqual(result,"2012 - MixTitle - DJ Spooky ")

  def test_mix_removeIllegalCharacters(self):
    data = "a\\b/c:d\"e*f?g|h<i>j"
    result = removeIllegalCharacters(data)
    self.assertEqual(result,"a_b_c_d_e_f_g_h_i_j")
if __name__ == '__main__':
    unittest.main()