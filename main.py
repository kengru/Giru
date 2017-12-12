from bhandler import bHandler
import datetime

giru = bHandler('487860520:AAEgLKKYShLi9iut4v0Zl5HLnrUf8sNF418')
answersTo = ('Hola')
now = datetime.datetime.now()

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        giru.get_updates(new_offset)
        last_update = giru.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in answersTo and today == now.day and 6 <= hour < 12:
            giru.send_message(last_chat_id, 'Saludo  {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in answersTo and today == now.day and 12 <= hour < 17:
            giru.send_message(last_chat_id, 'Buena tarde {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in answersTo and today == now.day and 17 <= hour < 23:
            giru.send_message(last_chat_id, 'Buena noche  {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
