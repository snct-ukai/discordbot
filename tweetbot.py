import discord,twitter,json,APIkeys,sys,tweepy #APIkeys.pyは別で用意
from googlesearch import search
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = APIkeys.CONSUMER_KEY
CS = APIkeys.CONSUMER_SECRET
AT = APIkeys.ACCESS_TOKEN
ATS = APIkeys.ACCESS_TOKEN_SECRET
DK = APIkeys.discord_token
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth ,wait_on_rate_limit = True)



client = discord.Client()

ModeFlag = 0

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global ModeFlag
    if message.content.startswith("*exit"):
        await message.channel.send("終了します")
        sys.exit()

    if ModeFlag == 1:
        kensaku = message.content
        ModeFlag=0
        await message.channel.send(kensaku+"を検索中です")
        tweets = api.search(q=kensaku, lang='ja', result_type='recent',count=1)
        for result in tweets: #タイムラインリストをループ処理
            a=result.id_str
            c=result.user.id
            m=("https://twitter.com/"+str(c)+"/status/"+a)
            await message.channel.send(m)

    if ModeFlag == 2:
        kensaku = message.content
        ModeFlag = 0
        await message.channel.send(kensaku+"を検索中です")
        count = 0
        # 日本語で検索した上位5件を順番に表示
        for url in search(kensaku, lang="jp",num = 5):
            await message.channel.send(url)
            count += 1
            if(count == 5):
               break

    if ModeFlag == 3:
        tweet = message.content
        ModeFlag = 0
        await message.channel.send(tweet+"をツイートします")
        api.update_status(tweet)

    if ModeFlag == 4:
        kensaku = message.content
        ModeFlag = 0
        await message.channel.send("ユーザー"+kensaku+"を検索中です")
        results = api.user_timeline(screen_name=kensaku,count=5)
        for result in results:
            a=result.id_str
            c=result.user.id
            m=("https://twitter.com/"+str(c)+"/status/"+a)
            await message.channel.send(m)

    if message.content == '*google':
        await message.channel.send("検索ワードを入力してください")
        ModeFlag = 2

    if message.content == ("*search"):
        await message.channel.send("検索ワードを入力してください")
        ModeFlag = 1

    if message.content == "*tweet":
        await message.channel.send("ツイートする内容を入力して下さい")
        ModeFlag = 3

    if message.content == "*user":
        await message.channel.send("検索したいユーザーIDを＠無しで入力してください")
        ModeFlag = 4

client.run(DK)