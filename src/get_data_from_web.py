import requests
import pandas as pd
from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://www.statsf1.com/en/lewis-hamilton/palmares-ct-austin.aspx') # locate html element with ID 'TD_GMy'

about = r.html.find('#TD_GMy', first=True)

print(about.text)