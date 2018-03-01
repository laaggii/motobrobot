#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, messagehandler
import logging
import random
import os
import tablib

# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
ducati = True
user_count=0
data=tablib.Dataset()
# Standard commands
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def help(bot, update):
    global user_count
    #print(update)
    bot.sendMessage(update.message.chat_id, text="Мотобратюня!\n /pin ТЕКСТ - запинить сообщение\n /pinurg ТЕКСТ - запинить сообщение с уведомлением\n /unpin - распинить сообщение\n /title ТЕКСТ - изменить тему\n /ducation - включить автоответы \n /ducatioff - выключить\n count: {}".format(user_count))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
def welcome(bot,update):
    print("welcome called")
    global user_count
    user=update.message.from_user
    msg = update.message
    chat_id = msg.chat.id
    text="Есть три условия, " + msg.new_chat_members[0].username+ "\n1. Мотоцикл\n2. Лепер\n3. Сиськи (для хуеносцев - поручительство старожил чата)\n4. Пережил ПМС\n\nСоблюдаешь два из них - велкам."
    if msg.new_chat_members[0].id!=131215524:
        bot.sendMessage(update.message.chat_id, text)
    if chat_id==-1001344267689:
        user_count=bot.getChatMembersCount(chat_id)
        data.append([user.id, user.first_name, user.last_name, user.username])



def fuckoff(bot,update):
    print("fuckoff called")
    msg = update.message
    chat_id = msg.chat.id
    text="Ушел, " + msg.left_chat_member.username+ " и хуй с ним"
    bot.sendMessage(update.message.chat_id, text)
def setphoto(bot,update):
    msg = update.message
    chat_id = msg.chat.id
    file_id=msg.text.split('/setphoto ')
    bot.setChatPhoto(update.message.chat_id, file_id)


def photosave(bot,update):
    msg = update.message
    chat_id = msg.chat.id
    print(msg.photo[-1])
    bot.sendMessage(chat_id,msg.photo[-1].file_id)


def title(bot,update):
    print("title called")
    msg = update.message
    chat_id = msg.chat.id
    bot.setChatTitle(chat_id, msg.text.split('/title ')[1])

def text(bot,update):
    
    msg = update.message
    chat_id = msg.chat.id
    user=update.message.from_user
    global data
    global user_count

    if random.randint(1,12)==6:
        if "дукати" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "Дукати топчик", reply_to_message_id=msg.message_id)
        if "жепка" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "Хуепка блядь!", reply_to_message_id=msg.message_id)
        if "сузуки" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "Меня когда-то тоже вела дорога приключений, но потом мне прострелили колено...", reply_to_message_id=msg.message_id)
        if "бмв" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "Тысячи самолетиков не могут ошибаться...", reply_to_message_id=msg.message_id)
        if "африка" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "Вам сюда:", reply_to_message_id=msg.message_id)
            bot.sendLocation(chat_id,latitude=47.886838,longitude=106.908145)
        if "триумф говно" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "ty pidor", reply_to_message_id=msg.message_id)
            return
        if "триумф" in msg.text.lower() and ducati:
            bot.sendMessage(chat_id, "ТВРЩМЙР попросил передать, что все, что вы напишете про триумф, может быть использовано против вас в Красногорске.", reply_to_message_id=msg.message_id)
    if chat_id==-1001344267689:
        count=bot.getChatMembersCount(chat_id)
        if user_count>count and chat_id==-1001344267689:
            print("Кто-то ушел")
            bot.sendMessage(chat_id, "Ваc стало на {} меньше, кажись кто-то съебнул. Обновил счетчик на {}".format(user_count-count, count))
            #for i in data:
            #    print(bot.getChatMember(chat_id, i[0]))
            out=[(i,u) for i, u in enumerate(data) if bot.getChatMember(chat_id, u[0]).status=='left']
            print(out)
            if len(out)!=0:
                out.sort(key=lambda tup: tup[0], reverse=True)
                for i,pid in out:
                    bot.sendMessage(chat_id, "Вот этот пидор: {}".format(pid[1]))
                    print("Удаляем пидора {}".format(data[i]))
                    del data[i]
            user_count=count
        if user:
            resid=[u for u in data if int(u[0])==user.id]
            #resnick=[u for u in data if u[3]==user.username]
            #resname=[u for u in data if u[1]==user.first_name]
            #print("что-то написал {}".format(user))
            if len(resid)==0:
                print(data['id'])
                data.append([user.id, user.first_name, user.last_name, user.username])
                print("resid {}".format(resid))
                print("Добавлен пользователь {}".format(user))
                with open('db.csv', 'w') as f:
                    f.write(data.csv)


def ducation(bot,update):
    print("ducation called")
    global ducati
    ducati =True

def ducatioff(bot,update):
    print("ducatioff called")
    global ducati
    ducati=False

def invite(bot,update):
    chat_id = update.message.chat.id
    print("invite called")
    bot.sendMessage(chat_id, bot.exportChatInviteLink(chat_id))

def pin(bot, update):
    print("pin called")
    chat_id = update.message.chat.id
    msg = update.message

    pinmsg="@%s: %s" % (msg.from_user.username,msg.text.split('/pin ')[1])
    msgid=bot.sendMessage(update.message.chat_id, pinmsg)
    bot.pinChatMessage(chat_id,msgid.message_id,disabe_notification=True)

def unpin(bot, update):
    
    print("unpin called")
    chat_id = update.message.chat.id
    msg = update.message

    bot.unpinChatMessage(chat_id)

def setusercount(bot, update):

    print("setusercount called")
    chat_id = update.message.chat.id
    msg = update.message
    global user_count
    user_count=bot.getChatMembersCount(chat_id)
    bot.sendMessage(chat_id, "Вас тут {}. Счетчик обновлен".format(user_count), reply_to_message_id=msg.message_id)

def showcsv(bot, update):
    print("showcsv called")
    global data
    chat_id = update.message.chat.id
    msg = update.message
    bot.sendMessage(chat_id, "Добавлено пользователей {} \n\n {}".format(len(data),data["username"]), reply_to_message_id=msg.message_id)

def setusercountjob(bot, job):
    print("setusercountjob called")
    global user_count
    user_count=bot.getChatMembersCount(-1001344267689)
    print("Вас тут {}. Счетчик установлен".format(user_count))

    
        
    


def pin_urgent(bot, update):
    print("pin called")
    chat_id = update.message.chat.id
    msg = update.message
    pinmsg="@%s: %s" % (msg.from_user.username,msg.text.split('/pin')[1])
    msgid=bot.sendMessage(update.message.chat_id, pinmsg)
    bot.pinChatMessage(chat_id,msgid.message_id,disabe_notification=False)

def initiate(bot, update):
    
    pass

def minute(bot, job):
    pass


def main():
    # Create the Updater and pass it your bot's token.
    #get db or create one
    global data
    if os.path.isfile('db.csv'):
        with open('db.csv') as db:
            data=tablib.Dataset().load(db.read())
            print("Loading DB: {}".format(db))
    else:
        data=tablib.Dataset()
        data.headers = ['id', 'first_name','last_name','username']
    print("data: \n{}".format(data))


    updater = Updater("285330075:AAExk55uSXqmJ_iw-x3zIPne7rC6Iukqync")
    j=updater.job_queue
    j.run_once(setusercountjob, 0)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("pin", pin))
    dp.add_handler(CommandHandler("unpin", unpin))
    dp.add_handler(CommandHandler("pinurgent", pin_urgent))
    dp.add_handler(CommandHandler("setphoto", setphoto))
    dp.add_handler(CommandHandler("title", title))
    dp.add_handler(CommandHandler("ducation", ducation))
    dp.add_handler(CommandHandler("ducatioff", ducatioff))
    dp.add_handler(CommandHandler("invite", invite))
    dp.add_handler(CommandHandler("setusercount", setusercount))
    dp.add_handler(CommandHandler("showcsv", showcsv))
    #dp.add_handler(MessageHandler([Filters.photo], photosave))
    # Message handlers
    dp.add_handler(MessageHandler([Filters.status_update], welcome))
    #dp.add_handler(MessageHandler([Filters.status_update.left_chat_member], fuckoff))
    dp.add_handler(MessageHandler([Filters.text], text))

    # log all errors
    dp.add_error_handler(error)

                    
    # Start the Bot
    updater.start_polling()

    updater.idle()
         
if __name__ == '__main__':
    main()
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
