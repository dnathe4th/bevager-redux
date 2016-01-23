"""
from bevager_cli import BevagerClient
client = BevagerClient(user='dnathe4th@gmail.com')
client.login()
resp = client.load_rum_list_html()
rums = client.extract_rum_list_data(resp.text)
print rums
"""
from bs4 import BeautifulSoup
import json
import requests
import yaml

with open('./credentials.yaml', 'r') as file_:
    _password_map = yaml.safe_load(file_.read())


class BevagerClient(object):
    def __init__(self, session=None, user=None):
        self.session = session or requests.Session()
        self.user = user
        if user not in _password_map:
            raise Exception('Unable to initialize with user {}, no credentials available'.format(user))

    def login(self):
        return self.session.post(
            'https://www.bevager.com/brg/login',
            headers={
                'Content-Type': 'application/json; charset=UTF-8',
            },
            data=json.dumps({
                'email': self.user,
                'password': _password_map[self.user],
                'programId': 1,
                'referer': '/brg',
                'rewardsGroupName': 'rumbustion',
            })
        )

    def load_rum_list_html(self):
        return self.session.get('https://www.bevager.com/brg/home?rewardsGroupName=rumbustion')

    def extract_rum_list_data(self, rum_list_html):
        soup = BeautifulSoup(rum_list_html, 'html.parser')
        for row in soup.find_all('tr', attrs={'class': 'item'}):
            columns = row.find_all('td')
            yield {
                'user': self.user,
                'country': columns[0].text.strip(),
                'name': columns[1].text.strip(),
                'price': _get_price(columns[2]),
                'signed': _get_request_status(columns[3]),
                'notes': columns[4].text.strip(),
                'available': _get_availability(row),
            }


def _get_price(price_column):
    return int(float(price_column.text.strip()[1:]))


def _get_request_status(request_column):
    if request_column.text.strip() == 'REQ':
        return 'UNREQUESTED'
    if 'fa-check' in request_column.span['class']:
        return 'REQUESTED'
    return 'REQUEST_PENDING'


def _get_availability(row):
    return 'historic-item' not in row['class']
