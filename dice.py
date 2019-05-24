import requests
import re
import logging
import random
from enum import Enum


logging.basicConfig(level='DEBUG', format='%(asctime)s [%(levelname)s] : %(message)s')

# bot_token = ''

class token_kind(Enum):
    ROLL=r'\d*d\d'
    NUMBER=r'\d+'
    OPERATOR=r'[+-]'

def roll(text) -> str:
    "/r 1d20+4"


def tokenize(text: str, prefix=True) -> list:
    # Only if prefix is True, discard the first element (i.e. /roll)
    if prefix:
        split = text.split(maxsplit=1)
        text = split[1] # Discards /r, /roll, ecc

    token_list = []
    prev_index = 0
    index = 0
    for character in text:
        index += 1

        # Splits when a operator char is encountered
        if character == '+' or character == '-':
            token_list.append(text[prev_index:index-1])
            token_list.append(character)
            prev_index = index
    token_list.append(text[prev_index:])
    logging.debug(token_list)
    return token_list


def get_kind(text: str) -> token_kind:
    for kind in token_kind: # returns token_kind value or False if no matches
        if re.search(kind.value, text):
            return kind
    return False

def compute(tokens: list) -> int:
    """Expected input for `tokens`:

    `[roll/number, operator?, roll/number?, operator?, roll/number? ...]`

    Odd number of elements in tokens
    """
    result = get(tokens[0])
    index = 1
    while index < len(tokens)-1:
        operator = get(tokens[index])
        second = get(tokens[index+1])
        if operator == '+':
            result += second
        elif operator == '-':
            result -= second
        index += 2
    return result

def get(value):
    kind = get_kind(value)

    # Dice roll, format r'\d*d\d+'
    if get_kind(value) == token_kind.ROLL:
        split = value.split('d')
        # Normal split, result of dice format r'\d+d\d+' (e.g. '6d6')
        if len(split[0]) > 0:
            return int(split[0]) * random.randint(1, int(split[1]))
        # Check for '', result of dice format r'd\d+' (e.g. 'd20')
        else:
            return random.randint(1, int(split[1]))

    # Constant
    if get_kind(value) == token_kind.NUMBER:
        return int(value)

    # + or -
    if get_kind(value) == token_kind.OPERATOR:
        return value

    # get_kind() returned False
    else:
        raise TypeError


# logging.debug(tokenize("/r 1d20+23+17"))
# logging.debug(tokenize("/roll 1d20+12"))
# logging.debug(tokenize("/roll 1d20+12"))
# logging.debug(tokenize("/roll d20"))
# logging.debug(tokenize("/roll 1d20-12+1d4-4"))
# logging.debug(get('1d20'))
# logging.debug(get('4d20'))

dice_roll = tokenize('/roll 1d20+13')
logging.debug(compute(dice_roll))

dice_roll = tokenize('/roll 1d20-4d4+12')
logging.debug('roll: ' + str(compute(dice_roll)))
