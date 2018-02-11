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
