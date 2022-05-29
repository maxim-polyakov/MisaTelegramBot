import core
import messagemonitor
import bototrain
import botoclean
import adders

if __name__ == "__main__":
    #boto.polling(none_stop=True)
    core.boto.remove_webhook()
    core.time.sleep(1)
    core.boto.set_webhook(url = core.WEB_HOOK_URL)
    core.app.run(host = core.APP_HOST, port = core.APP_PORT, debug = False)



