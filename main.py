from tpblite import TPB
import telebot
from telebot import types
from telebot.types import Chat, Message
import requests
from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='TorBot')

bot_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(bot_token)
t = TPB()

@bot.message_handler(commands=["start"])
def welcome(message):
    cid = message.chat.id
    user = message.from_user.first_name
    text = f"_Hi {message.from_user.first_name}\nThis is a torrent search bot based on TPB.\nFor more information use /help_"
    print(user)
    bot.send_message(cid,text,parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def help(message):
    cid = message.chat.id
    text = "Send the Torrent Name and I will send you the Magnet Links"
    bot.send_message(cid,text)

@bot.message_handler(func=lambda message: message.text is not None)
def get_name(message):
    cid = message.chat.id
    t_link = ""
    print(message.chat.username)
    # message_text = message.text
    torrent_name = message.text
    final_msg = ""
    msg = bot.send_message(cid,"Getting Your Torrents Ready...")
    # mid = msg.message_id
    torrents = t.search(torrent_name)
    print(torrent_name)
    if int(len(torrents)) == 0:
        bot.send_message(cid,"*No Torrents Found*",parse_mode="Markdown")
    else:
        try:
            for torrent in torrents:
                if int(torrent.seeds)>0:
                    t_name = torrent.title
                    t_seeds = torrent.seeds
                    t_leeches = torrent.leeches
                    t_filesize = torrent.filesize
                    t_torrent = torrent.magnetlink
                    html = '<p><b>{}</b></p>'.format(t_name)+'<p><b>Seeds : </b>{}</p>'.format(t_seeds)+'<p><b>Leeches : </b>{}</p>'.format(t_leeches)+'<p><b>File Size : </b>{}</p>'.format(t_filesize)+'<p><b>Magnet Link : </b><i>{}</i></p>'.format(t_torrent)+'<br><br>'
                    final_msg = final_msg + html
            response = telegraph.create_page('Search Results for {}'.format(torrent_name),html_content=final_msg)
            t_link = ('https://telegra.ph/{}'.format(response['path']))
            bot.send_message(cid,t_link)
            print(t_link)
        except:
            bot.send_message(cid,"*Some Error Occured..Try again after sometime..*",parse_mode="Markdown")

# @bot.message_handler(func=lambda message: message.text is not None)
# def other(message):
#     cid = message.chat.id
#     text = "Only /start /help and /tor are available"
#     bot.send_message(cid,text)

bot.polling()