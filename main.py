import bot
import sys
from bot import adders
from bot import botoclean
from bot import bototrain
from bot import messagemonitor
# ______________________________________________________________________________


if __name__ == "__main__":
    
    # boto.polling(none_stop=True)
    bot.boto.remove_webhook()
    bot.time.sleep(1)
    bot.boto.set_webhook(url = sys.argv[1])
 #   bot.boto.set_webhook(url = 'https://4aba-31-204-109-41.eu.ngrok.io')
    bot.app.run(host=bot.APP_HOST, port=bot.APP_PORT, debug=False)
