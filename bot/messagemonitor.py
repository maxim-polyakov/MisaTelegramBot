import bot
from bot import subfunctions
from bot import bototrain
from sqlalchemy import create_engine

@bot.boto.message_handler(content_types=['text'])
def get_user_text(message):

    def neurodesc():
        bpred = bot.Predictors.Binary()
        mpred = bot.Predictors.Multy()
        if bpred.predict(text, bot.mapa.himapa,
                         './models/binary/himodel.h5',
                         './tokenizers/binary/hitokenizer.pickle',
                         '') == "Приветствие":

            ra = bot.Answers.RandomAnswer()
            bot.boto.send_message(
                message.chat.id, ra.answer(), parse_mode='html',)

        elif(bpred.predict(text, bot.mapa.qumapa,
                           './models/binary/qumodel.h5',
                           './tokenizers/binary/qutokenizer.pickle',
                           'qu') == "Вопрос"):

            if(mpred.predict(text) == "Дело"):
                bot.boto.send_message(
                    message.chat.id, "Я в порядке", parse_mode='html')

            elif(mpred.predict(text) == "Погода"):
                bot.boto.send_message(
                    message.chat.id, "Погода норм", parse_mode='html')
            else:
                bot.boto.send_message(
                    message.chat.id, "Вопрос без классификации",
                    parse_mode='html')

        elif(bpred.predict(text, bot.mapa.commandmapa,
                           './models/binary/commandmodel.h5',
                           './tokenizers/binary/thtokenizer.pickle',
                           'command') == "Команда"):

            bot.commands.commandsdesition(
                bot.boto, message, tstr)

        elif(bpred.predict(text, bot.mapa.thmapa,
                           './models/binary/thmodel.h5',
                           './tokenizers/binary/thtokenizer.pickle',
                           '') == "Благодарность"):

            bot.boto.send_message(message.chat.id, "Не за что",
                                  parse_mode='html')
        else:
            
            if(mpred.predict(text) == "Дело"):
                bot.boto.send_message(
                    message.chat.id, "Утверждение про дела", parse_mode='html')

            elif(mpred.predict(text) == "Погода"):
                bot.boto.send_message(
                    message.chat.id, "Утверждение про погоду", parse_mode='html')
            else:
                bot.boto.send_message(
                    message.chat.id, "Нет классификации",
                    parse_mode='html')

# ______________________________________________________________________________
    inpt = message.text.split(' ')

    text = []
    print(message.text)
    pr = bot.Models.TextPreprocessers.CommonPreprocessing()
    for txt in text:
        conn = bot.NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        
        data = {'text': pr.preprocess_text(txt), 'agenda': ''}
        df = bot.pd.DataFrame()
        new_row = bot.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql('validset', con = engine, schema = 'public', index=False, if_exists='append')

    if(pr.preprocess_text(inpt[0]) == "мис" or inpt[0].lower() == "misa"):
        tstr = message.text.replace(inpt[0], '')
        text.append(tstr)
        

        try:
            neurodesc()
        except:
            bot.boto.send_message(message.chat.id, 'А?', parse_mode='html')
        
    elif(message.text == "👍"):
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')
    elif(message.text == "👎"):
        bot.boto.send_message(message.chat.id, "😒", parse_mode='html')
