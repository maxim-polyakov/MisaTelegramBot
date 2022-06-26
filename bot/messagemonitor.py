import bot

from Bot_module import Monitors

@bot.boto.message_handler(content_types=['text'])
def get_user_text(message):

    mon = Monitors.MessageMonitor(message)
    mon.monitor()