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
        if message.content.startswith('&') :
            name = message.content[1:]
            r = api.get_summoner_by_name(name)
            x = api.rank(r['id'])
            y = '{} is {} {} {} LP'
            z = 0
            if x[0]['queueType'] == "RANKED_FLEX_SR" :
                z = 1
            await client.send_message(message.channel, y.format(name, x[z]['tier'], x[z]['rank'], x[z]['leaguePoints']))


    client.run(BOT_TOKEN)

if __name__ == "__main__" :
    main()
