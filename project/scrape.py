import requests
from bs4 import BeautifulSoup
import dpath
import json
import asyncio
import telegram
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
x = datetime.datetime.now()
year=x.strftime("%G")
month=x.strftime("%B")
date=x.strftime("%d")


pagecontent= requests.get("https://movieweb.com/movies/"+str(year)+"/")
soup = BeautifulSoup(pagecontent.content,'html.parser')

rdate = soup.findAll('div',{"class":"database-card-spec"})
content = soup.findAll('div',{"class":"database-card-title"})
imagelink = soup.findAll('img',{"class":"lazyload"})

#storing value in dictionary
fulllist ={}
for reldate,title in zip(rdate,content):
    key=reldate.text
    value=title.text
    fulllist.setdefault(key, []).append(value)

clean_data = {key: [value.replace('\n', '') for value in values] for key, values in fulllist.items()}


#searching dictionary through dpath
search = dpath.search(clean_data,'*'+month.capitalize()+' '+str(date)+'*', separator=",")
# print(json.dumps(search, indent=4, sort_keys=False))
clean_1=json.dumps(search, indent=4, sort_keys=False)
characters_to_remove = ['{', '}', '[', ']']
translation_table = str.maketrans('', '', ''.join(characters_to_remove))
result = clean_1.translate(translation_table) 
res = result


# async def get_chat_id(bot_token):
    # bot = telegram.Bot(token=bot_token)
    # updates = await bot.get_updates()
    # if updates:
    #     chat_id_1 = updates[0].message.chat_id
    #     # print(f"Chat ID: {chat_id_1}")
    #     return chat_id_1
    # else:
    #     print("No messages received yet.")
async def send(chat, msg, bot_token):
    await telegram.Bot(bot_token).sendMessage(chat_id=chat, text=msg)

if res != "":
    async def main(mes,bot_token):
        # chatid=await get_chat_id(bot_token)
        await send('737340891',str(mes),bot_token)
    if __name__ == '__main__':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main(res,bot_token))
            # asyncio.get_event_loop().run_until_complete(main(res,bot_token))
        except KeyboardInterrupt:
            pass

else:
    async def main(bot_token):
        # chatid=await get_chat_id(bot_token)
        await send('737340891','no movie released today',bot_token)
    if __name__ == '__main__':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main(bot_token))
        # asyncio.get_event_loop().run_until_complete(main(bot_token))
        except KeyboardInterrupt:
            pass


