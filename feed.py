import telepot
import sqlite3
import feedparser
import time
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.request import urlopen

def on_chat_message(msg):
    while 1:

        conn = sqlite3.connect('feedero.db')

        text, chat_type, chat_id = telepot.glance(msg)
        chat_id = '@FeederinhoCanal'
        bot = telepot.Bot(TOKEN)

        read = open('lista.txt', 'r+')
        link = (read.readline(),)
        cont = 0
        while (link[0]):
            print ('Iniciando codigo')
            sql = 'SELECT post_id FROM feedero WHERE feed_link = (?)'
            rodar = 1
            print ('Link:  '+link[0])
            post = feedparser.parse(link[0])
            
            curs = conn.cursor()
            curs.execute(sql,link)
            result = curs.fetchone()

            if (post['bozo'] == 1):
                url = (link[0])
                read = urlopen(url)
                soup = BeautifulSoup(read,'html.parser')
                #Remover tags titles e guid
                titles = soup.find('title').find_all(text=True)
                links = soup.find('guid').find_all(text=True)
                AFC = 1
                if(result):              
                    cont = 0
                    while (rodar):
                        for i in range(len(titles)):    
                            if(result[0] == titles[i]):    
                                for linkP in links:
                                    print(titles[AFC])
                                    print(linkP)
                                    bot.sendMessage(chat_id,''+titles[AFC]+'\n'+linkP)
                                    AFC+=1
                             
                                sql = '''UPDATE feedero SET post_id = ? WHERE feed_link = ?'''
                                curs = conn.cursor()
                                params = (links[0],link[0])
                                curs.execute(sql,params)
                                conn.commit()
                                
                                #botar para enviar a mensagem e salvar ultimo titulo no banco
                                rodar=0
                                break
                            else:
                                cont+=1
                else:
                    print('nao existe')
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                    params = (links[0],link[0])
                    result = curs.execute(sql,params)
                    for z in range(len(titles)):
                        bot.sendMessage(chat_id,titles[z]+' \n '+links[z])
                    conn.commit()
                          
            else:
                if(result):
                    cont = 0
                    while (rodar):
                        for i in range(len(post['entries'])):
                            if (result[0] == (post['entries'][i]['id'])):
                                for z in range(cont):
                    
                                    bot.sendMessage(chat_id,post['entries'][z]['title']+' \n '+post['entries'][z]['id'])
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
                    print('nao existe')
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                    params = (post['entries'][0]['id'],link[0])
                    result = curs.execute(sql,params)
                    for z in range(len(post['entries'])):
                        bot.sendMessage(chat_id,post['entries'][z]['title']+' \n '+post['entries'][z]['id'])
                    conn.commit()
            link = (read.readline(),)
        read.close()
        conn.close()
        # code sleeps for 4 minutes
        time.sleep(240)

TOKEN = '420896204:AAEVJamoLZA-LFfyRb3dh9dLRZWujQv8vbY'  # get token from command-line

bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
