import discord
import requests
import json

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('!도움말'):
        await message.channel.send('채팅창에 `!유저조회@[유저명]` 를 입력하시면 롤 전적이 검색됩니다.')
        await message.channel.send('롤 전적은 최근 12게임을 검색해줍니다.')

    if "!유" in message.content:
        if message.content.startswith('!유저조회@'):
            if "@" in message.content:
                userName = message.content.split("@")[1]

                userData = getUserData(userName)
                e = discord.Embed(title=userData["tierRank"])
                e.set_author(name="유저 조회 결과")
                e.set_thumbnail(url=userData["userImage"])

                for item in userData["result"]:
                    Game = item["ChampName"] + " - " + item["GameResult"]
                    KDA = item["Kill"] + " / " + item["Death"] + " / " + item["assist"]
                    e.add_field(name=Game, value=KDA, inline=False)

                await message.channel.send(embed=e)

        else:
            await message.channel.send('잘못된 명령어 입니다. 아래의 검색명령어 양식대로 적어주세요.')
            await message.channel.send("```!유저조회@[유저명]```")


def getUserData(userName):
    response = requests.get("http://3964bf147c56.ngrok.io?name="+userName)
    json_val = response.json()
    return json_val


client.run('token')