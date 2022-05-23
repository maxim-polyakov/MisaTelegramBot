import rpa as r


def founder(boto, message, reply_markup, inptmes):
    r.init()
    r.url('https://ru.wikipedia.org/')
    r.type('//*[@name="search"]', inptmes + '[enter]')
    boto.send_message(message.chat.id, r.read('p'),
                      parse_mode='html')
    r.snap('page', 'results.png')
    r.close()