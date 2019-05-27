from abc import ABC, abstractstaticmethod
import logging

class Roller(ABC):
    @abstractstaticmethod
    def tokenize_delimiters() -> list:
        pass

    @classmethod
    def tokenize(cls, text: str, prefix=True) -> list:
        if prefix:
            split = text.split(maxsplit=1)
            text = split[1].strip()

        token_list = []
        prev_index = 0
        index = 0
        for character in text:
            index += 1

            # Splits when a operator char is encountered
            if character in cls.tokenize_delimiters():
                if prev_index != index - 1: # case two near symbols
                    token_list.append(text[prev_index:index-1])
                token_list.append(character)
                prev_index = index
        token_list.append(text[prev_index:])
        logging.debug(token_list)
        return token_list

    @abstractstaticmethod
    def get(value):
        pass
