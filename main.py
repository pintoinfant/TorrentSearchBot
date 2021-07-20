from tpblite import TPB
import telebot
import time
from telebot import types
from telebot.types import Chat, Message
import requests
from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='TorBot')

bot_token = "1859626661:AAF_qZJraZC_qkYkAqKeuHql0Uw5azNcDBQ"
bot = telebot.TeleBot(bot_token)
t = TPB()
@bot.message_handler(commands=['torrent'])
def get_name(message):
    cid = message.chat.id
    message_text = message.text
    #print(len(message_text))
    torrent_name = message_text[9:]
    #print(torrent_name)
    final_msg = ""
    msg = bot.send_message(cid,"Getting Your Torrents Ready...")
    mid = msg.message_id
    torrents = t.search(torrent_name)
    if int(len(torrents)) == 0:
        bot.send_message(cid,"*No Torrents Found*",parse_mode="Markdown")
    else:
        try:
            for torrent in torrents:
                if int(torrent.seeds)>0 and int(torrent.leeches)>0:
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
            #bot.edit_message_text(final_msg, cid, mid,parse_mode="Markdown",disable_web_page_preview=True)
        except:
            bot.send_message(cid,"Some Error Occured...Try Again After Sometime..!")
            #bot.send_message(cid,"*End of the List*",parse_mode="Markdown")
    # bot.send_message(cid,"*End of the List*",parse_mode="Markdown")

bot.polling()