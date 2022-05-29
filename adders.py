import core
#import messagemonitor
#import bototrain
#import botoclean
#import pyTelegramBotAPI




#______________________________________________________________________________
@core.boto.message_handler(commands=['trainadd'])
def get_user_text(message):
    read = core.pd.read_excel('./datasets/dataset.xlsx')
    tstr = message.text.replace('/trainadd ', '')
    out = tstr.split('|')
    idx = 0
    for i in range(0, len(core.mapa.himapa)):
        if(out[1] == core.mapa.himapa[i]):
            idx = i
    data = {'text': core.NLP.libraries.preprocess_text(
        out[0]), 'agenda': out[1], 'hi': idx}
    df = core.pd.DataFrame(read)
    new_row = core.pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('./datasets/dataset.xlsx', index=False)

    core.boto.send_message(message.chat.id, 'text: ' +
                      out[0] + ' agenda: ' + out[1], parse_mode='html')




@core.boto.message_handler(commands=['dataset'])
def get_user_text(message):

    read = core.pd.read_excel('./datasets/dataset.xlsx')
    df = core.pd.DataFrame(read)
    for fram in df:
        core.boto.send_message(message.chat.id, fram, parse_mode='html')



#______________________________________________________________________________


