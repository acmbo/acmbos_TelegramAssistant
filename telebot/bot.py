# -*- coding: utf-8 -*-

import time
import pandas as pd
import sqlite3
from ebayDB.item import item
import ebayDB.sqlitedb as edb
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)




# Setup wokring skript 
from ebayDB.telebot.settings import TELEGRAMTOKEN, dbpath
ebayitem = None
Lastediteditem = -1
currentIndex = 0




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)





def start_ebay(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        'Ich werde jetzt einen Ebay Gegenstand für dich aufnehmen und speichern '
        'Sende /cancel um Gespräch zu beenden.\n'
        'Wie ist der Name des Gegenstand?'
    )
    global ebayitem
    global currentIndex 
    
    ebayitem = None
    
    from ebayDB.sqlitecommands import rowcount
    currentIndex = rowcount(dbpath, 'ebayitem')
    
    return 'name'




def name(update: Update, context: CallbackContext) -> int:
    #user = update.message.from_user
    update.message.reply_text(
        'Hat der Gegenstand einen Typ zum einordnen? \n'
        'Sende /skip um die Frage zu überspringen',
        reply_markup=ReplyKeyboardRemove(),
    )
    
    global ebayitem
    global currentIndex
    
    ebayitem = item(currentIndex, update.message.text)

    return 'typeofitem'




def typeofitem(update: Update, context: CallbackContext) -> int:
    
    #user = update.message.text
    update.message.reply_text(
        'Willst du dem Gegenstand ein Bild hinzufügen '
        'oder mit /skip zum nächsten Schritt übergehen.\n',
        reply_markup=ReplyKeyboardRemove(),
    )
    
    global ebayitem
    ebayitem.type = update.message.text
    
    return 'photo'




def photo(update: Update, context: CallbackContext) -> int:
    
    global ebayitem
    
    #catching message
    #user = update.message.from_user
    timing = '_'.join(map(str,[time.localtime().tm_year,time.localtime().tm_mon,
                       time.localtime().tm_mday,
                       time.localtime().tm_hour, time.localtime().tm_min,
                      time.localtime().tm_sec])) 
    
    #Saving Photo
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('ebayDB/img/{itemname}_{timing}.jpg'.format(itemname=ebayitem.idx,
                                                             timing=timing))
    
    ebayitem.addpic('ebayDB/img/{itemname}_{timing}.jpg'.format(itemname=ebayitem.idx,
                                                             timing=timing))
    
    #logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Willst du ein weiteres Bild hinzufügen ' 
        'oder mit /skip zum nächsten Schritt übergehen.\n'
    )
    return 'photo'




def skip_photo(update: Update, context: CallbackContext) -> int:
    
    #user = update.message.from_user
    #logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'Füge die Maße des Gegenstands hinzu oder sende /skip.'
    )
    return 'sizeofitem'
   




def sizeofitem(update: Update, context: CallbackContext) -> int:
    #user = update.message.from_user
    global ebayitem

    try:
        ebayitem.setsize(update.message.text, outFormat = 'cm')
        update.message.reply_text(
        'Füge eine Beschreibung zum Gegenstand hinzu oder sende /skip.',
        reply_markup=ReplyKeyboardRemove(),
        )
    except:
        update.message.reply_text(
        'Bei der Eingabe der Maße ist ein Fehler aufgetreten.'
        ' Versuche es nochmal oder sende /skip.',
        reply_markup=ReplyKeyboardRemove(),
        )
        return 'sizeofitem'

    return 'Beschreibung'





def skip_size(update: Update, context: CallbackContext) -> int:
    #user = update.message.from_user
    #logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'Füge eine Beschreibung zum Gegenstand hinzu oder sende /skip.'
    )
    return 'Beschreibung'





def bio(update: Update, context: CallbackContext) -> int:
    
    global ebayitem
    global Lastediteditem
    
    #user = update.message.from_user
    #logger.info("Bio of %s: %s", user.first_name, update.message.text)
    
    ebayitem.description = update.message.text
    update.message.reply_text('Danke für Infos. Der Gegenstand ist jetzt gespeichert!\n')
    
    #Set correct idx for the item
    ebay_item_idx = edb.insertVAl(ebayitem, dbpath)
    ebayitem.idx = ebay_item_idx
    Lastediteditem = ebay_item_idx
    
    for photopath in ebayitem.pictures:
        edb.insertPhoto(dbpath, ebayitem.idx, ebayitem.name, photopath)
    
    
    return ConversationHandler.END




def cancel(update: Update, context: CallbackContext) -> int:
    #user = update.message.from_user
    #logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Gegenstand wird verworfen. Danke für das Gespräch!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END




def ebay_convhandler():
    '''
    Convhandler mit States:
        -start() führt zu name(0)
        -name(0) führt zu type(1)
        -type(1) führt zu photo(2)
        -photo(2) führt zu photo(2)
        -photo(2) kann geskippt werdern zu beschriebung(3)
        
    '''
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('addebay', start_ebay)],
    states={
        'name': [MessageHandler(Filters.text & ~Filters.command, name)],
        'typeofitem': [MessageHandler(Filters.text & ~Filters.command, typeofitem)],
        'photo': [MessageHandler(Filters.photo, photo),
                   CommandHandler('skip', skip_photo)],
        'sizeofitem': [MessageHandler(Filters.text & ~Filters.command, sizeofitem),
                   CommandHandler('skip', skip_size)],
        'Beschreibung': [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler


def ebay_delete_convhandler():
    '''
    Convhandler mit States:
        -dellastitem() 
        -NextState(0) 
        
    '''
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('dellastitem', dellastitem_start)],
    states={
        'NextState': [MessageHandler(Filters.regex('^(Ja|Nein)$'), dellastitem_end)],
        },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler




def dellastitem_start(update: Update, context: CallbackContext) -> None:
    """Deleteitesm from last conversation state 1"""

    reply_keyboard = [['Ja', 'Nein']]

    update.message.reply_text(
        'Den Gegenstand aus letzter Konversation finden und löschen? \n ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    
    return 'NextState'


def dellastitem_end(update: Update, context: CallbackContext) -> None:
    """Deleteitesm from last conversation state 2"""

    if update.message.text=='Ja':

        global Lastediteditem
        
        if Lastediteditem == -1:
            update.message.reply_text('Keinen Gegenstand aus letzter Konversation gefunden \n',
                                      reply_markup=ReplyKeyboardRemove(),)
        else:
            update.message.reply_text('Gegenstand wird gelöscht \n',
                                      reply_markup=ReplyKeyboardRemove(),)
            try:
                from ebayDB.sqlitecommands import deleterowbyid
                deleterowbyid(dbpath, 'ebayitem', Lastediteditem)
                update.message.reply_text('Löschvorgang erfolgreich! \n')
                
            except:
                update.message.reply_text('Ein Fehler beim Löschen ist aufgetretten. \n')
            
    else:
        update.message.reply_text('Löschvorgang abgebrochen \n'),
    
    return ConversationHandler.END







def allebayitems(update: Update, context: CallbackContext) -> None:
    """Returns alls ebayitems"""
    update.message.reply_text('Das sind alle Gegenstände in der Ebay Database: \n')
    
    cnx = sqlite3.connect(dbpath)
    df = pd.read_sql_query("SELECT * FROM ebayitemsbotview", cnx)
    cnx.close()

    update.message.reply_text(df.to_string(index=False))




def deleteitem(update: Update, context: CallbackContext):
    '''Deletes item mentioned in context in ebaydb by searching by name'''
    try: 
        nameofitem = "'" + ' '.join(context.args) + "'"
        
        from ebayDB.sqlitecommands import deleterowbynamecol
        deleterowbynamecol(dbpath, 'ebayitem', nameofitem)
        update.message.reply_text(str(nameofitem))
        
    except:
        update.message.reply_text('Fehler im Command \n')
    
    
    
    
    
def deleteitembyid(update: Update, context: CallbackContext):
    '''Deletes item mentioned in context in ebaydb by searching by id'''
    try: 
        nameofitem = int(context.args[0])
        
        from ebayDB.sqlitecommands import deleterowbyid
        deleterowbyid(dbpath, 'ebayitem', nameofitem)
        update.message.reply_text(str(nameofitem))
    except:
        update.message.reply_text('Fehler im Command \n')





def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAMTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    ebay_handler = ebay_convhandler()
    ebay_delete_handler = ebay_delete_convhandler()


    dispatcher.add_handler(ebay_handler)
    dispatcher.add_handler(ebay_delete_handler)
    
    dispatcher.add_handler(CommandHandler("allebayitems", allebayitems))
    dispatcher.add_handler(CommandHandler("delitem", deleteitem))
    dispatcher.add_handler(CommandHandler("delitembyid", deleteitembyid))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()