from datetime import datetime

import requests
from bs4 import BeautifulSoup, element


class DotaParser:

    def __init__(self):
        self.main_url = 'https://game-tournaments.com'
        self.url = 'https://game-tournaments.com/dota-2/matches'
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')
        self.datetime_format = '%Y-%m-%d %H:%M:%S'

    def parse_future_matches(self):
        final_list = []
        table_match = self.soup.find('div', {"id": "block_matches_current"})
        for match in table_match.contents[1].contents:
            if type(match) != element.NavigableString:
                match_dict = {'seria_id': match.attrs["rel"],
                              'team1_name': match.contents[3].contents[1].contents[1].contents[1].contents[1].contents[
                                  0],
                              'team2_name': match.contents[3].contents[1].contents[5].contents[3].contents[1].contents[
                                  0], 'tour_title': match.contents[7].contents[1].attrs['title'],
                              'match_link': match.contents[3].contents[1].attrs["href"]}
                date_element = match.contents[5].contents[3].contents[1]
                if date_element.attrs.get('class') == ['sct']:
                    match_dict['date'] = datetime.strptime(date_element.attrs['data-time'], self.datetime_format)
                else:
                    match_dict['date'] = None
                final_list.append(match_dict)
        return final_list

    def parse_finished_matches(self):
        final_list = []
        table_match = self.soup.find('div', {"id": "block_matches_past"})
        for match in table_match.contents[1].contents:
            if type(match) != element.NavigableString:
                match_dict = {'seria_id': match.attrs["rel"],
                              'result': match.contents[3].contents[1].contents[3].contents[3].contents[1].attrs[
                                  "data-score"]}
                final_list.append(match_dict)
        return final_list
