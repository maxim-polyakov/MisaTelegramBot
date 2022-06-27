import bot

from Bot_module import Monitors


@bot.boto.message_handler(commands=['testmonitor'])
def get_user_text(message):
    print('here')
    tmon = Monitors.TestMonitor()
    
    tmon.monitor()
    bot.boto.send_message(message.chat.id, "ready", parse_mode='html')

@bot.boto.message_handler(content_types=['text'])
def get_user_text(message):

    mon = Monitors.MessageMonitor(message)
    mon.monitor()
    
