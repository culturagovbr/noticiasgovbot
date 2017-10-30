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
            # verifica se o feed tem erro de bozo
            if (post['bozo'] == 1):
                print('com bozo')
                debuga = 1
                url = (link[0])
                ler = urlopen(url)
                soup = BeautifulSoup(ler,'html.parser')
                #titulo da noticia
                titles = soup.find_all('title')
                
                #link da noticia
                posts = soup.find_all('guid')
                
                if(result):
                    cont = 1
                    #atribui o guid(links da pagina) para a variavel i
                    for i in posts:
                        #i.text compara os links que estao no banco
                        if(result[0] == i.text):

                            for z in range(cont):
                                if(titles[z].text != 'Fundação Cultural Palmares'):
                                    bot.sendMessage(chat_id,''+titles[z].text+'\n'+posts[z].text)
                                   
                            sql = '''UPDATE feedero SET post_id = ? WHERE feed_link = ?'''
                            curs = conn.cursor()
                            params = (posts[0].text,link[0])
                            curs.execute(sql,params)
                            conn.commit()

                            break
                        else:
                            cont+=1
                else:
                    print('nao existe')
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                    params = (posts[0].text,link[0])
                    result = curs.execute(sql,params)
                    for z in range(len(posts)):
                        if(titles[z].text != 'Fundação Cultural Palmares'):
                            bot.sendMessage(chat_id,''+titles[z].text+'\n'+posts[0].text)
                    conn.commit()                       
            else:
                if(result):
                    cont = 0
                    while (rodar):
                        for i in range(len(post['entries'])):
                            if (result[0] == (post['entries'][i]['id'])):
                                for z in range(cont):
                                    bot.sendMessage(chat_id,post['entries'][z]['title']+'\n'+link[0])
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