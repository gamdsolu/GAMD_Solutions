from datetime import date, datetime
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

dict = {}
url = "http://www.erca.gov.et:8008/wserca/index.jsf?tin="

status_dict = {
            1: "Please enter your TIN number!",
            2: "TIN numbers are only digits. Please check your entery!",
            3: "We cannot find the person registered with this TIN number!",
            4: "It seams you have no Internet Connection!"
        }


def replaceIt(my_list):
    oldvallist = ["CITYNAME", "id", "KEBELEDESC", "LOCALITYDESC", 
    "PARISHNAME","STREETNO","TAXCENTRENO","TELPHONE","TPNAME",
    "TPNAME_F","TPNAME_S"]

    newvallist = ["ZONE/SUB CITY:", "TIN NUMBER:", "WOREDA:", "LOCALITYDESC:",
    "REGION:", "STREET NUMBER:", "TAX CENTER NUMBER:", "TELEPHONE NUMBER:",
    "TAX PAYER NAME:", "TPNAME_F", "TAX PAYER NAME (AMHARIC):"]
    
    for oldval in my_list:
        if oldval in oldvallist:
            x = my_list.index(oldval)
            y = oldvallist.index(oldval)
            try:
                my_list[x] = newvallist[y]
            except:
                pass
    return my_list