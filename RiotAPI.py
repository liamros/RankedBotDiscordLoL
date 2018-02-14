import requests
import RiotConts as Consts

class RiotAPI(object):

    def __init__(self, api_key, region = Consts.REGIONS['europe_west']) :
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}) :
        args = {'api_key' : self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
        Consts.URL['base'].format(
            url = api_url
            ),
            params = args
        )
        #print (response.url)
        return response.json()

    def get_summoner_by_name(self, name) :
        api_url = Consts.URL['summoner_by_name'].format(
            version = Consts.API_VERSION['league'],
            summonerName = name
            )
        return self._request(api_url)


    def rank(self, id) :
        api_url = Consts.URL['rank'].format(
            version = Consts.API_VERSION['league'],
            summonerid = id
            )
        return self._request(api_url)


    def champion_master(self, id) :
        api_url = Consts.URL['champion_mastery'].format(
            version = Consts.API_VERSION['league'],
            summonerid = id
            )
        return self._request(api_url)


    def match(self, accId) :
        api_url = Consts.URL['match'].format(
            version = Consts.API_VERSION['league'],
            accountId = accId
            #queue = 420
            )
        return self._request(api_url)


    def match_info(self, matId) :
        api_url = Consts.URL['matchdetails'].format(
            version = Consts.API_VERSION['league'],
            matchid = matId
            )
        return self._request(api_url)
