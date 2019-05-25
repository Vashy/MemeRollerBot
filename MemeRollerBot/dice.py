import requests
import re
import logging
import random
from enum import Enum


logging.basicConfig(level='DEBUG', format='%(asctime)s [%(levelname)s] : %(message)s')

# bot_token = ''
normal_roll = r'(?:/r|/roll)\s+(?:(\d*d\d+)|(\d+))(?:([+-])((\d*d\d+)|(\d+)))*'
multi_roll = r'(?:/r|/roll)\s+\d*d\d+[+-]\d+(?:/[+-]\d+)+'


class TokenKind(Enum):
    ROLL=r'\d*d\d'
    NUMBER=r'\d+'
    OPERATOR=r'[+-/]'


def parse(text: str) -> (str, str):

    # Multiattack roll match
    match_multi_roll = re.search(multi_roll, text)
    if match_multi_roll:
        value = match_multi_roll.group(0)
        logging.debug('Matched multi roll: \'' + value + '\', match length: ' + str(len(value)))
        logging.debug('Roll descriptor: \'' + text[len(value):len(text)].strip() + '\'')
        return value, text[len(value):len(text)].strip()

    # Normal match
    match = re.search(normal_roll, text)
    if not match_multi_roll and match:
        value = match.group(0)
        logging.debug('Matched normal roll: \'' + value + '\', match length: ' + str(len(value)))
        logging.debug('Roll descriptor: \'' + text[len(value):len(text)].strip() + '\'')
        return value, text[len(value):len(text)].strip()

    return False, ''

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


def get_kind(text: str) -> TokenKind:
    for kind in TokenKind: # returns TokenKind value or False if no matches
        if re.search(kind.value, text):
            return kind
    return False

def compute(tokens: list) -> (int, list):
    """Expected input for `tokens`:

    `[roll/number, operator?, roll/number?, operator?, roll/number? ...]`

    Odd number of elements in tokens
    """
    result, local_steps, token_kind = get(tokens[0])
    steps = [get_step(local_steps, token_kind)]
    index = 1
    while index < len(tokens)-1:
        operator, _, _ = get(tokens[index])
        second, local_steps, token_kind = get(tokens[index+1])
        if operator == '+':
            result += second
            steps.append('+')
        elif operator == '-':
            result -= second
            steps.append('-')
        steps.append(get_step(local_steps, token_kind))
        index += 2
    return result, steps

def get(value) -> (int, list, TokenKind):
    kind = get_kind(value)

    # Dice roll, format r'\d*d\d+'
    if kind == TokenKind.ROLL:
        split = value.split('d')
        # Normal split, result of dice format r'\d+d\d+' (e.g. '6d6')
        if len(split[0]) > 0:
            result, steps = process_roll(int(split[0]), int(split[1]))
            return result, steps, TokenKind.ROLL
        # Check for '', result of dice format r'd\d+' (e.g. 'd20')
        else:
            result, steps = process_roll(1, int(split[1]))
            return result, steps, TokenKind.ROLL

    # Constant
    if kind == TokenKind.NUMBER:
        return int(value), [value], TokenKind.NUMBER

    # + or -
    if get_kind(value) == TokenKind.OPERATOR:
        return value, [value], TokenKind.OPERATOR

    # get_kind() returned False
    else:
        raise TypeError

def get_step(steps: list, token_kind: TokenKind) -> str:
    if token_kind == TokenKind.ROLL:
        result = '('
        for step in steps:
            result = ''.join([
                result,
                str(step),
                '+',
            ])
        result = result[:-1] # Removes the last '+'
        return ''.join([result, ')'])
    # Single element list
    return steps[0]

def roll(roll_expr: str) -> (int, list):
    return compute(tokenize(roll_expr))


def process_roll(iterations, value) -> (int, list):
    result = 0
    steps = []
    for _ in range(iterations):
        random_roll = random.randint(1, int(value))
        result += random_roll
        steps.append(random_roll)
    return result, steps

# logging.debug(tokenize("/r 1d20+23+17"))
# logging.debug(tokenize("/roll 1d20+12"))
# logging.debug(tokenize("/roll 1d20+12"))
# logging.debug(tokenize("/roll d20"))
# logging.debug(tokenize("/roll 1d20-12+1d4-4"))
# logging.debug(get('1d20'))
# logging.debug(get('4d20'))

# dice_roll = tokenize('/roll 1d20+13')
# logging.debug(compute(dice_roll))

# dice_roll = tokenize('/roll 1d20-4d4+12')
# logging.debug('roll: ' + str(compute(dice_roll)))
# parse('/r 1d20+12-2+4 ancd asdoasid oiasd ')
# parse('/r 1d20+12/+7/+2 ancd asdoasid oiasd    ')

# logging.debug(roll('/r 1d20+14'))

# logging.debug(get_step([1, 4, 5], token_kind=TokenKind.ROLL))