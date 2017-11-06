
from telegram.ext import Updater, CommandHandler
import logging
import os
import sys
import telepot
import sqlite3
import feedparser
import time
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.request import urlopen


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def alarm(bot, job):
    try:                                
        conn = sqlite3.connect('feedero.db')
        
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
                                    bot.sendMessage(job.context,''+titles[z].text+'\n'+posts[z].text)
                                   
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
                            bot.sendMessage(job.context,""+titles[z].text+'\n'+posts[z].text)
                    conn.commit()                       
            else:
                if(result):
                    cont = 0
                    while (rodar):
                        for i in range(len(post['entries'])):
                            if (result[0] == (post['entries'][i]['id'])):
                                for z in range(cont):
                                    bot.sendMessage(job.context,""+post['entries'][z]['title']+'\n'+link[0])
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
                        bot.sendMessage(job.context,""+post['entries'][z]['title']+'\n'+link[0])
                    conn.commit()

            link = (read.readline(),)
        read.close()
        conn.close()

    except(TimedOut, ReadTimeoutError):
        bot.sendMessage(job.context, "Erros-------------------------------------------------------")


def set_timer(bot, update, args, job_queue, chat_data):
    
    chat_id = update.message.chat_id
    try:
        
        due = 5

        
        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Serviço reiniciado com sucesso! \n Continuando execução...')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def error(bot, update, error):
    
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    
    updater = Updater(os.environ.get('BOT_TOKEN'))

    
    dp = updater.dispatcher

    
    dp.add_handler(CommandHandler("start", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()