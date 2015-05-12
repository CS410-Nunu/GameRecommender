import urllib, json

API_KEY = 'A4CBB01B5DB13D02D5651075E467FD7C'
#USER_ID = '76561197960434622'

#GAME_LIBRARY_URL = str('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + API_KEY + '&steamid=' + USER_ID + '&format=json')
#USER_INFO_URL = str('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + API_KEY + '&steamids=' + USER_ID + '&format=json')

class SteamUser:


    def __init__(self, user_id):
        self.USER_ID = str(user_id)
        self.GAME_LIBRARY_URL = str('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + API_KEY + '&steamid=' + self.USER_ID + '&format=json')
        self.USER_INFO_URL = str('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + API_KEY + '&steamids=' + self.USER_ID + '&format=json')
        self.games_dict = self.loadUserGames()
        self.userAvatar = 'User avatar not set'
        self.realName = 'Real name not set'

        try:
            self.userAvatar = str(self.loadUserAvatar())
        except KeyError as e:
            self.userAvatar = 'Avatar not found'

        try:
            self.realName = str(self.loadRealName())
        except KeyError as e:
            self.realName = 'Real name not found'


    def loadUserGames(self):
        response = urllib.urlopen(self.GAME_LIBRARY_URL)
        data = json.loads(response.read())
        games_list = []
        for game in data['response']['games']:
            game_id = str(game['appid'])
            playtime = int(game['playtime_forever'])
            tup = (game_id, playtime)
            games_list.append(tup)
        games_list.sort(key=lambda x: x[1], reverse=True)
        return games_list


    def loadUserAvatar(self):
        response = urllib.urlopen(self.USER_INFO_URL)
        data = json.loads(response.read())
        return data['response']['players'][0]['avatarfull']


    def loadRealName(self):
        response = urllib.urlopen(self.USER_INFO_URL)
        data = json.loads(response.read())
        return data['response']['players'][0]['realname']


    def getUserGames(self):
        return self.games_dict

    def getRealName(self):
        return self.realName

    def getUserAvatar(self):
        return self.userAvatar



#76561198075059171
#76561198010203943
test = SteamUser(76561198010203943)
print test.getUserGames()
print test.getRealName()
print test.getUserAvatar()
#76561198075059171
#print games_list

'''
response = urllib.urlopen(GAME_LIBRARY_URL)
data = json.loads(response.read())
for game in data['response']['games']:
    print game['appid']
'''
