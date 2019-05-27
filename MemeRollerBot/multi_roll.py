import logging
from dice import get_kind, TokenKind, process_roll, get_step
from roller import Roller


class MultiDiceRoller(Roller):
    @staticmethod
    def tokenize_delimiters() -> list:
        return ['+', '-', '/']

    @staticmethod
    def get(value) -> (int, list, TokenKind):
        kind = get_kind(value)

        # Dice roll, format r'\d*d\d+'
        if kind == TokenKind.ROLL:
            split = value.split('d')
            # Normal split, result of dice format r'\d+d\d+' (e.g. '6d6')
            if split[0]:
                result, steps = process_roll(int(split[0]), int(split[1]))
                return result, steps, TokenKind.ROLL

            # Check for '', result of dice format r'd\d+' (e.g. 'd20')
            result, steps = process_roll(1, int(split[1]))
            return result, steps, TokenKind.ROLL

        # Constant
        if kind == TokenKind.NUMBER:
            return int(value), [value], TokenKind.NUMBER

        # get_kind() returned False
        else:
            raise TypeError

    @staticmethod
    def compute(tokens: list) -> (int, list):

        # First element: roll
        result, local_steps, token_kind = get(tokens[0])
        steps = [get_step(local_steps, token_kind)]

        # Second element: +/-
        operator, local_steps, token_kind = get(tokens[1])
        steps.append(get_step(local_steps, token_kind))

        # Third element: first attack
        first_value, local_steps, token_kind = get(tokens[2])
        steps.append(get_step(local_steps, token_kind))

        index = 1
        while index < len(tokens)-1:
            raise NotImplementedError

if __name__ == "__main__":
    print(MultiDiceRoller.tokenize('/r 1d20+14/+7/+2'))
