from tpblite import TPB
import telebot
import os
import pyfiglet
import time
from telebot import types
from telebot.types import Chat, Message
import requests
from telegraph import Telegraph
from sendreport import send__message

telegraph = Telegraph()
telegraph.create_account(short_name='TorBot')

bot_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(bot_token)
t = TPB()

@bot.message_handler(commands=["start"])
def welcome(message):
    cid = message.chat.id
    user = message.chat.username
    result = pyfiglet.figlet_format("HI..")
    text = "This is a PirateBay torrent search Bot.\nFor more information use /help"
    bot.send_message(cid,result)
    bot.send_message(cid,text)
    message_t = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) has accessed the bot."
    send__message(message_t)

@bot.message_handler(commands=["help"])
def help(message):
    cid = message.chat.id
    text = "To seach a torrent use /tor <query>.\nLike (/tor Ubuntu)"
    bot.send_message(cid,text)


@bot.message_handler(func=lambda message: message.text is not None)
def get_name(message):
    cid = message.chat.id
    t_link = " "
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
            t_link = t_link
            message_t = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) has accessed the bot for [{torrent_name}]({t_link})"
            send__message(message_t)
            print(t_link)
        except:
            message_t = "Bot is not Working"
            bot.send_message(cid,"Some Error Occured...Try Again After Sometime..!")
            send__message(message_t)


# @bot.message_handler(func=lambda message: message.text is not None)
# def other(message):
#     cid = message.chat.id
#     text = "Only /start /help and /tor are available"
#     bot.send_message(cid,text)



bot.polling()