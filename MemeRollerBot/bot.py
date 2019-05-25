import time

import telepot
from telepot.loop import MessageLoop

import dice

bot = telepot.Bot('TOKEN')


def handle(msg):
    content_type, _, chat_id, _, msg_id = telepot.glance(msg, long=True)
    dice.logging.debug(f'Received message from {msg["from"]["username"]} ({chat_id})')

    if content_type == 'text':
        roll_expression, roll_desc = dice.parse(msg['text'])
        if roll_expression:
            result, steps = dice.roll(roll_expression)
            response = build_msg(msg['from']['username'], result, steps, roll_desc)
            bot.sendMessage(chat_id, response, reply_to_message_id=msg_id, parse_mode='markdown')

def build_msg(username, result, steps, roll_desc):
    final_msg = ''.join([
        username,
        f' rolled *{roll_desc}*:\n`',
    ])
    for step in steps:
        final_msg = ''.join([
            final_msg,
            str(step),
            # ' ',
        ])
    final_msg = ''.join([
        final_msg,
        '=`\n',
        f'*{result}*'
    ])
    return final_msg

MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(1)
