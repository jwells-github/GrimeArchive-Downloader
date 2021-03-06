MAX_FILENAME_LENGTH = 172

class Mix:
  def __init__(self, id, title, djs, mcs, date, downloadResult, downloadSuccessful):
    self.id = id
    self.title = title
    self.djs = djs
    self.mcs = mcs
    self.date = date
    self.downloadResult = downloadResult
    self.downloadSuccessful = downloadSuccessful
    
  def file_name(self):
    date = self.date.replace(" ","").replace("??/","").replace("/",".").replace("?","")
    if len(date) > 0:
      date += " - "
    title = remove_illegal_characters(self.title)
    filename = date + title + " "
    djs = remove_illegal_characters(self.djs)
    if djs != "Unknown DJ":
      filename += "- " +  djs + " " 
    mcs = remove_illegal_characters(self.mcs)
    if len(mcs) > 0:
      filename += "ft. "
    mcList = mcs.split(",")
    for mc in mcList:
      if len(filename) + len(mc) > MAX_FILENAME_LENGTH:
        break
      else:
        filename += mc + ", "
    # Remove comma at end of mc string
    if len(mcList) > 0:
      filename = filename[0:(len(filename)-2)]
    return filename

# Remove characters that cannot be used in a filename
def remove_illegal_characters(givenString:str):
  returnString = givenString.replace("\\","_")
  returnString = returnString.replace("/","_")
  returnString = returnString.replace(":","_")
  returnString = returnString.replace("\"","_")
  returnString = returnString.replace("*","_")
  returnString = returnString.replace("?","_")
  returnString = returnString.replace("|","_")
  returnString = returnString.replace("<","_")
  returnString = returnString.replace(">","_")
  return returnString