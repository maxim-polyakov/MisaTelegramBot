import telebot
import pandas as pd
import NLP
import prediction
import mapa
import subfunctions

    # Классификация
boto = telebot.TeleBot('5301739662:AAG4EZfZtvPkku9b9eymTHZW6EITYyKuAbc')


@boto.message_handler(commands = ['start'])
def start(message):
    mess = f'Hi, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    boto.send_message(message.chat.id, mess ,  parse_mode='html')

@boto.message_handler(commands = ['trainadd'])
def get_user_text(message):
    read = pd.read_excel('./datasets/dataset.xlsx')
    tstr = message.text.replace('/trainadd ','')    
    out = tstr.split('|')
    idx = 0
    for i in range(0,len(mapa.himapa)):
        if(out[1] == mapa.himapa[i]):
            idx = i
    data =  {'text': NLP.libraries.preprocess_text(out[0]),'agenda': out[1], 'hi': idx}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('./datasets/dataset.xlsx',index=False)
    
    boto.send_message(message.chat.id, 'text: ' + out[0] + ' agenda: '+ out[1], parse_mode='html')

@boto.message_handler(commands = ['dataset'])
def get_user_text(message):
    read = pd.read_excel('./datasets/dataset.xlsx')
    df = pd.DataFrame(read)
    for fram in df:
        boto.send_message(message.chat.id, fram, parse_mode='html')


@boto.message_handler(commands = ['hitrain'])
def get_user_text(message):
    NLP.ishitrain()
    boto.send_message(message.chat.id, "trained" , parse_mode='html')
@boto.message_handler(commands = ['qutrain'])
def get_user_text(message):
    NLP.isqutrain()
    boto.send_message(message.chat.id, "trained" , parse_mode='html')
@boto.message_handler(commands = ['thtrain'])
def get_user_text(message):
    NLP.thtrain()
    boto.send_message(message.chat.id, "trained" , parse_mode='html')
@boto.message_handler(commands = ['multyclasstrain'])
def get_user_text(message):
    NLP.multyclasstrain()
    boto.send_message(message.chat.id, "trained" , parse_mode='html') 


 
@boto.message_handler(commands = ['multyclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/multyclasesset.xlsx','questionclass')
    boto.send_message(message.chat.id, "cleaned" , parse_mode='html') 
@boto.message_handler(commands = ['hiclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/dataset.xlsx','hi')
    boto.send_message(message.chat.id, "cleaned" , parse_mode='html') 
@boto.message_handler(commands = ['quclean'])
def get_user_text(message):
    NLP.QuestionsetCleaner('./datasets/questionset.xlsx')
    boto.send_message(message.chat.id, "cleaned" , parse_mode='html') 
    
@boto.message_handler(commands = ['thclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/thanksset.xlsx','thanks')
    boto.send_message(message.chat.id, "cleaned" , parse_mode='html') 


@boto.message_handler()
def get_user_text(message):
  
        text = []
        read = pd.read_excel('./validset/validset.xlsx')
        data =  {'text': NLP.libraries.preprocess_text(message.text),'agenda': ''}
        df = pd.DataFrame(read)
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_excel('./validset/validset.xlsx',index=False)
        text.append(message.text)
        
        if prediction.Hipredict(text) == "Приветствие":
            subfunctions.add(message.text, './recognized_sets/recognized_hi.xlsx',"Приветствие")
            boto.send_message(message.chat.id, mapa.randanswhi(), parse_mode='html') 
        elif(prediction.QuPpredict(text) == "Вопрос"):
            subfunctions.quadd(message.text, './recognized_sets/recognized_qu.xlsx',"Вопрос")
            
            if(prediction.MultyPpredict(text) == "Дело"):
               boto.send_message(message.chat.id, "Я в порядке" , parse_mode='html') 
            elif(prediction.MultyPpredict(text) == "Погода"):
                boto.send_message(message.chat.id, "Погода норм" , parse_mode='html') 
            else:
                boto.send_message(message.chat.id, "Вопрос без классификации" , parse_mode='html') 
        elif(prediction.ThPpredict(text) == "Благодарность"):
            subfunctions.quadd(message.text, './recognized_sets/recognized_th.xlsx',"Благодарность")
            boto.send_message(message.chat.id, "Не за что" , parse_mode='html')
        else:
            boto.send_message(message.chat.id, "Нет класса" , parse_mode='html') 
  #    try:
 #   except:
 #       boto.send_message(message.chat.id, '!?', parse_mode='html')
        
boto.polling(none_stop=True)