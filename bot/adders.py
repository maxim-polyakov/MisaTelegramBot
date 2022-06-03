import bot
#import messagemonitor
#import bototrain
#import botoclean
#import pyTelegramBotAPI




#______________________________________________________________________________
@bot.boto.message_handler(commands=['trainadd'])
def get_user_text(message):
    read = bot.pd.read_excel('./datasets/dataset.xlsx')
    tstr = message.text.replace('/trainadd ', '')
    out = tstr.split('|')
    idx = 0
    for i in range(0, len(bot.mapa.himapa)):
        if(out[1] == bot.mapa.himapa[i]):
            idx = i
    data = {'text': bot.NLP.libraries.preprocess_text(
        out[0]), 'agenda': out[1], 'hi': idx}
    df = bot.pd.DataFrame(read)
    new_row = bot.pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('./datasets/dataset.xlsx', index=False)

    bot.boto.send_message(message.chat.id, 'text: ' +
                      out[0] + ' agenda: ' + out[1], parse_mode='html')




@bot.boto.message_handler(commands=['dataset'])
def get_user_text(message):

    read = bot.pd.read_excel('./datasets/dataset.xlsx')
    df = bot.pd.DataFrame(read)
    for fram in df:
        bot.boto.send_message(message.chat.id, fram, parse_mode='html')



#______________________________________________________________________________


