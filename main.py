import gspread, os, json
from oauth2client.service_account import ServiceAccountCredentials
from opencage.geocoder import OpenCageGeocode
from datetime import datetime, timedelta

time = datetime.now()

#Loading the config file
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'config.json')) as f:
    config = json.load(f)


#Initializing Opencage Geocoder
api_key = open(os.path.join(dirname, 'opencage-api-key')).read()
geocoder = OpenCageGeocode(api_key)

#Initializing gspread to access the Google Sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(dirname, 'drive-credentials.json'), scope)
client = gspread.authorize(creds)

#Opening the spreadsheet
spread = client.open(config.get('sheetName'))
worksheet = spread.get_worksheet(0)

#Function converting r, k to A1 notation
#E.g 2,3 --> C2
def _to_A1(r, c):
    return chr(64 + c) + str(r)

#Converts from A1 to r,c
#E.g A2 --> 2, 1
def _from_A1(s):
    c = ord(s[0]) - 64
    r = int(s[1])
    return (r, c)

#Function that returns the coordinates of a location string
#Only searches within coordinate bounds of Linköping: see https://opencagedata.com/bounds-finder
def _get_coordinates(location):
    response = geocoder.geocode(location, bounds='15.44952,58.33401,15.81001,58.48364', limit=1)
    if len(response) == 0:
        return None

    geometry = response[0].get('geometry')
    if geometry is None:
        return None

    return dict(lat=geometry.get('lat'), lng=geometry.get('lng'))

#Colors for formatting cells
red = {
    "backgroundColor": {
        "red": 0.878,
        "green": 0.4,
        "blue": 0.4
    }
}

green = {
    "backgroundColor": {
        "red": 0.576,
        "green": 0.769,
        "blue": 0.49
    }
}

r, c = _from_A1(config.get('addressStartCell'))
cell = worksheet.cell(r, c)
while cell.value != '':
    coords = _get_coordinates(cell.value)

    if coords is None:
        #worksheet.format(config.get('latitudeColumn') + str(r), red)
        #worksheet.format(config.get('longitudeColumn') + str(r), red)
        print('{:<4}: Could not find coordinates!'.format(_to_A1(r, c)))
        worksheet.update(config.get('latitudeColumn') + str(r), 'Kunde inte hitta adressen')
    else:
        #worksheet.format(config.get('latitudeColumn') + str(r), green)
        #worksheet.format(config.get('longitudeColumn') + str(r), green)
        
        worksheet.update(config.get('latitudeColumn') + str(r), coords.get('lat'))
        worksheet.update(config.get('longitudeColumn') + str(r), coords.get('lng'))
        
        print('{:<4}: Found coordinates!'.format(_to_A1(r, c)))
    
    r = r + 1
    cell = worksheet.cell(r, c)

print('Finished in {} seconds'.format((datetime.now() - time).total_seconds()))