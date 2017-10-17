import telepot
import sqlite3
import feedparser
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import logging

def on_chat_message(msg):
    while 1:

        conn = sqlite3.connect('feedero.db')

        text, chat_type, chat_id = telepot.glance(msg)
        bot = telepot.Bot(TOKEN)

        read = open('lista.txt', 'r+')
        link = (read.readline(),)
        cont = 0
        while (link[0]):
            print ('IT VURKS!!!')
            sql = 'SELECT post_id FROM feedero WHERE feed_link = (?)'
            rodar = 1
            print (link[0])
            post = feedparser.parse(link[0])
            
            curs = conn.cursor()
            curs.execute(sql,link)
            result = curs.fetchone()

            if (post['bozo'] == 1):
                print('Feed com problemas: '+ link[0])
                # caso o link forneca download
                # url= y
                # urllib.urlretrieve(url, "RSS.txt")
                # o = urllib2.urlopen(url)
                # arq = o.read()
                # with open("RSS2.tpostt")
                pass
            else:
                if(result):
                    cont = 0
                    while (rodar):
                        for i in range(len(post['entries'])):
                            if (result[0] == (post['entries'][i]['id'])):
                                for z in range(cont):
                    
                                    bot.sendMessage(chat_id,post['entries'][z]['title']+'---'+link[0])
                                sql = '''UPDATE feedero SET post_id = ? WHERE feed_link = ?'''
                                curs = conn.cursor()
                                params = (post['entries'][0]['id'],link[0])
                                curs.execute(sql,params)
                                conn.commit()
                    
                                rodar = 0
                                break
                            else:
                                cont+=1                            
                else:
                    print('não existe')
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                    params = (post['entries'][0]['id'],link[0])
                    result = curs.execute(sql,params)
                    for z in range(len(post['entries'])):

                                    bot.sendMessage(chat_id,post['entries'][z]['title']+'---'+link[0])
                    conn.commit()

            link = (read.readline(),)

        read.close()
        conn.close()
        # code sleeps for 4 minutes
        time.sleep(240)

TOKEN = 'TOKEN'  # get token from command-line

bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)