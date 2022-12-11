from datetime import date, datetime
from tzlocal import get_localzone
from dbconnect import get_data, get_data_line, insert
import difflib

def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()

res = similarity('Китайский хлебный братец кормит чаек плащом и короной из булочек', '«Братец-хлеб» из Китая носит плащ и корону из булочек, чтобы кормить чаек')
print(res)
