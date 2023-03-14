import requests
def savePage(date: str):
  url = "russian-offensive-campaign-assessment-" + GenerateLinkByDate(date)
  savePageCustom(date, url)

def savePageCustom(date: str, customLink: str):
  url = "https://understandingwar.org/backgrounder/" + customLink
  r = requests.get(url)
  if (r.text.find("We're Sorry. The page you're looking for wasn't found.") != -1):
    print(date + " no such link")
  else:
    name = "C:\\Users\\PC\\PycharmProjects\\pythonProject1\\isw_collected_data\\"+date+".html"
    with open(name, "w") as output_file:
      output_file.write(r.text)
      output_file.close()

def saveFeb():
  savePageCustom("2022-02-24", "russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment")
  savePageCustom("2022-02-25", "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022")
  savePageCustom("2022-02-26", "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26")
  savePageCustom("2022-02-27", "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-27")
  savePageCustom("2022-02-28", "russian-offensive-campaign-assessment-february-28-2022")

def GenerateLinkByDate(date: str):
  year = date[0:4]
  day = int(date[-2:])
  month = int(date[5:-3])
  if(year=="2022"):
    return months[month-1]+"-"+str(day)
  else:
    return months[month-1]+"-"+str(day)+"-"+year


base_url = 'https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment-'
months = ["january", "february", "march", "april",
         "may", "june", "july", "august",
         "september", "october", "november", "december"]

def prepareBaseDate():
  saveFeb()
  for month in range(3,13):
    for day in range(1, 32):
      daystr = f"{day:02d}"
      monthstr = f"{month:02d}"
      date = "2022-"+monthstr+"-"+daystr
      savePage(date)
  for day in range(1, 26):
    daystr = f"{day:02d}"
    date = "2023-01-"+daystr
    savePage(date)

prepareBaseDate()