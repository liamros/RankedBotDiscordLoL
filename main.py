from RiotAPI import RiotAPI
from config import *
import discord
import asyncio


def main() :
    api = RiotAPI(API_KEY)

    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('---------')
        summoners = open("summoner_names.txt").read().splitlines() #add summoner here, and increse for range
        game = [3528775016, 3524659958, 3526634118, 3528480436, 3528775016, 3528645656, 3528818694]
        accounts = [0, 0, 0, 0, 0, 0, 0]
        for i in range (0, 7) :     #range depends on the number of summoners
            account_num = api.get_summoner_by_name(summoners[i])
            accounts[i] = account_num['accountId']
        loop = 0
        while True :
            for i in range (0, 7) :     #range depends on the number of summoners
                match = api.match(accounts[i])
                z = 0
                Idgame = match['matches'][z]['gameId']

                while match['matches'][z]['queue'] != 420 :
                    z+=1
                    Idgame = match['matches'][z]['gameId']

                if  Idgame != game[i] and loop != 0 :
                    details = api.match_info(Idgame)
                    game[i] = Idgame
                    j = 1
                    for j in range (0, 10) :        #controls each partecipant of the match in riot's dictionary
                        if details['participants'][j]['championId'] == match['matches'][z]['champion'] :
                            break
                    champion = CHAMPS[match['matches'][z]['champion']]
                    win = details['participants'][j]['stats']['win']
                    if win == True :
                        win = 'Victory'
                    else :
                        win = 'Defeat'
                    kills = details['participants'][j]['stats']['kills']
                    deaths = details['participants'][j]['stats']['deaths']
                    assists = details['participants'][j]['stats']['assists']
                    penta = details['participants'][j]['stats']['pentaKills']
                    if penta == 0 :
                        await client.send_message(client.get_channel('YOUR CHANNEL ID'), '{} last ranked game :\nChampion = {}\n{}\nKDA = {}/{}/{}\n---------------\n\n\n\n'.format(summoners[i], champion, win, kills, deaths, assists))
                    else :
                        await client.send_message(client.get_channel('YOUR CHANNEL ID'), '{} last ranked game :\nChampion = {}\n{}\nKDA = {}/{}/{}\n{}\n---------------\n\n\n\n'.format(summoners[i], champion, win, kills, deaths, assists, 'PENTAKILL'))
                else :
                    game[i] = Idgame
            loop = 1
            await asyncio.sleep(120.0)

    @client.event
    async def on_message(message):
        if message.content.startswith('\\rank ') :
            name = message.content[6:]
            r = api.get_summoner_by_name(name)
            x = api.rank(r['id'])
            y = '{} is {} {} {} LP'
            z = 0
            if x[0]['queueType'] == "RANKED_FLEX_SR" :
                z = 1
            await client.send_message(message.channel, y.format(name, x[z]['tier'], x[z]['rank'], x[z]['leaguePoints']))

        elif message.content.startswith('\\bestchamps ') :
            name = message.content[12:]
            r = api.get_summoner_by_name(name)
            x = api.champion_master(r['id'])
            z = 0
            y = '{} best champs are :\n'
            await client.send_message(message.channel, y.format(name))
            y = '{}° {}, mastery {} - {} points\n'
            for z in range(0, 5) :
                await client.send_message(message.channel, y.format(z+1, CHAMPS[x[z]['championId']], x[z]['championLevel'], x[z]['championPoints']))



    client.run(BOT_TOKEN)

if __name__ == "__main__" :
    main()
