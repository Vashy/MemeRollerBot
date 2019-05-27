import time
import os

import logging

import telepot
from telepot.loop import MessageLoop

import dice as dice


logging.basicConfig(level='DEBUG', format='%(asctime)s [%(levelname)s] : %(message)s')


if not os.environ['BOT_TOKEN']:
    raise EnvironmentError("BOT_TOKEN variable not set")

BOT = telepot.Bot(os.environ['BOT_TOKEN'])


def handle(msg):
    content_type, _, chat_id, _, msg_id = telepot.glance(msg, long=True)
    logging.debug(f'Received message from {msg["from"]["username"]} ({chat_id})')

    if content_type == 'text':
        roll_expression, roll_desc = dice.parse(msg['text'])
        if roll_expression:
            result, steps = dice.roll(roll_expression)
            response = build_msg(msg['from']['username'], result, steps, roll_desc)
            BOT.sendMessage(chat_id, response, reply_to_message_id=msg_id, parse_mode='markdown')

def build_msg(username: str, result, steps, roll_desc):

    final_msg = f'*{username}*'
    if roll_desc:
        final_msg = ''.join([
            final_msg,
            f' rolled *{roll_desc}*:\n`',
        ])
    else:
        final_msg = ''.join([
            final_msg,
            f' rolled:\n`',
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

MessageLoop(BOT, handle).run_as_thread()

logging.info('-----------------------')
logging.info('Launching MemeRollerBot')
logging.info('-----------------------')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nbye')
