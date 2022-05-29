import core
import adders
import bototrain
import botoclean

import messagemonitor


#______________________________________________________________________________


@core.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    trainer = core.NLP.Multy()
    trainer.multyclasstrain('train')
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')

if __name__ == "__main__":
    
    #boto.polling(none_stop=True)
    core.boto.remove_webhook()
    core.time.sleep(1)
    core.boto.set_webhook(url = core.WEB_HOOK_URL)
    core.app.run(host = core.APP_HOST, port = core.APP_PORT, debug = False)



