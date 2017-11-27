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

# def sendmsg(bot,chat_id):
#  #envia as mensagens pro tele

# def dbstuff(bot,errorC):
#     #faz tudo que diz respeito ao banco

#     conn = sqlite3.connect('feedero.db')

#     if errorC:
#         #executar se tiver erro no feed
#     else:
#         #executar se n tiver erro
#     conn.close()
#     return 0

def alarm(bot, job):
    try:
        conn = sqlite3.connect('feedero.db')
        chat_id = "@RamonCanabarro"
        read = open('lista.txt', 'r+')
        linha = (read.readline(),)
        x = 0
        while(linha[x]):
            linha+=(read.readline(),)
            x+=1
        read.close()
        cont = 0
        for x in range(len(linha)-1):
            print ('Iniciando codigo: '+str(time.strftime("%Y-%m-%d %H:%M:%S" )))
            sql = 'SELECT post_id FROM feedero WHERE feed_link = (?)'
            rodar = 1
            post = feedparser.parse(linha[x])
            print ('Link:'+linha[x]+'  '+str(time.strftime("%Y-%m-%d %H:%M:%S" )))
            curs = conn.cursor()
            curs.execute(sql,(linha[x],))
            result = curs.fetchone()
            # verifica se o feed tem erro de bozo
            if (post['bozo'] == 1):
                print('com bozo'+str(time.strftime("%Y-%m-%d %H:%M:%S" )))
                url = (linha[x])
                try:
                    ler = urlopen(url)
                except Exception as e:
                   print ('Erro no link: ' + url +'\n'+' Erro:'+str(e.code)+'  ' +str(time.strftime("%Y-%m-%d %H:%M:%S" )))
                   x+=1
                   break
                soup = BeautifulSoup(ler,'html.parser')
                #titulo da noticia
                titles = soup.find_all('title')

                #link da noticia
                posts = soup.find_all('guid')
                var = soup.find_all('link')

                # if (titles):

                print (titles)
                print (posts)
                print (var)

                ler.close()
                if(result):
                    cont = 1
                    #atribui o guid(links da pagina) para a variavel i
                    for i in posts:
                        #i.text compara os links que estao no banco
                        if(result[0] == i.text):
                            params = (titles[0].text,linha[x])
                            for z in range(cont):
                                if(titles[z].text != 'Notícias'):
                                    bot.sendMessage(job.context,''+titles[z].text+'\n'+linha[x], timeout=300)


                            sql = '''UPDATE feedero SET post_id = ? WHERE feed_link = ?'''
                            curs = conn.cursor()
                            if(titles[0].text == 'Notícias'):
                                params = (titles[1].text,linha[x])
                            curs.execute(sql,params)
                            conn.commit()
                            break
                        else:
                            cont+=1
                else:
                    print('nao existe'+str(time.strftime("%Y-%m-%d %H:%M:%S" )))
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                params = (titles[0].text,linha[x])
                if(titles[0].text == 'Notícias'):
		                  params = (titles[1].text,linha[x])
                result = curs.execute(sql,params)
                for z in range(len(titles)):
                    if(titles[z].text != 'Notícias'):
                        bot.sendMessage(job.context,""+titles[z].text+'\n'+linha[x], timeout=300)
                conn.commit()
            else:
                if(result):
                    cont = 0
                    while (rodar):
                        for i in range(len(post['entries'])):
                            if (result[0] == (post['entries'][i]['links'][0]['href'])):
                                for z in range(cont):
                                    bot.sendMessage(job.context,""+post['entries'][z]['title']+'\n'+post['entries'][z]['links'][0]['href'], timeout=300)
                                sql = '''UPDATE feedero SET post_id = ? WHERE feed_link = ?'''
                                curs = conn.cursor()
                                params = (post['entries'][0]['links'][0]['href'],linha[x])
                                curs.execute(sql,params)
                                conn.commit()
                                rodar = 0
                                break
                            else:
                                cont+=1
                else:
                    print('nao existe'+str(time.strftime("%Y-%m-%d %H:%M:%S" )))
                    sql = 'INSERT INTO feedero VALUES (?,?)'
                    curs = conn.cursor()
                    params = (post['entries'][0]['links'][0]['href'],linha[x])
                    result = curs.execute(sql,params)
                    for z in range(len(post['entries'])):
                        bot.sendMessage(job.context,""+post['entries'][z]['title']+'\n'+post['entries'][z]['links'][0]['href'], timeout=300)
                    conn.commit()
        conn.close()

    except():
        bot.sendMessage(job.context, "Erros-------------------------------------------------------")


def set_timer(bot, update, args, job_queue, chat_data):

    chat_id = update.message.chat_id
    try:

        due = 240  #Tempo em segundos!

        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Servico reiniciado com sucesso! \n Continuando execucao...')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def error(bot, update, error):

    logger.warning('Update "%s" caused error "%s"', update, error)


def main():

    updater = Updater(os.environ.get('GOV_TOKEN'))


    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(timeout=8220)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
