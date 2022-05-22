import rpa as r


def founder(boto, message, reply_markup):
    r.init()
    r.url('https://www.google.com')
    r.type('//*[@name="q"]', 'decentralisation[enter]')
    boto.send_message(message.chat.id, r.read('result-stats'),
                      parse_mode='html', reply_markup=reply_markup)
    r.snap('page', 'results.png')
    r.close()