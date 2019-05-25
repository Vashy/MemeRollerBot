import unittest
import random

import dice


class TestDice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        random.seed(123)

    def test_parse(self):
        expr, text = dice.parse('/r 1d20+15 abcd')
        self.assertEqual(expr, '/r 1d20+15')
        self.assertEqual(text, 'abcd')

        expr, text = dice.parse('/roll 1d20+17/+12/+7 text text ')
        self.assertEqual(expr, '/roll 1d20+17/+12/+7')
        self.assertEqual(text, 'text text')

        expr, text = dice.parse('/invalid text')
        self.assertFalse(expr)
        self.assertEqual(text, '')

    def test_tokenize(self):
        lst = dice.tokenize('/r 1d20+17-2d2+4d4')
        self.assertIn('1d20', lst)
        self.assertEqual(lst[1], '+')
        self.assertEqual(lst[3], '-')
        self.assertEqual(lst[5], '+')
        self.assertIn('17', lst)
        self.assertIn('2d2', lst)

    def test_get_kind(self):
        kind = dice.get_kind('1d2')
        self.assertEqual(kind, dice.TokenKind.ROLL)
        self.assertNotEqual(kind, dice.TokenKind.NUMBER)

        kind = dice.get_kind('123')
        self.assertEqual(kind, dice.TokenKind.NUMBER)

        kind = dice.get_kind('+')
        self.assertEqual(kind, dice.TokenKind.OPERATOR)
        kind = dice.get_kind('-')
        self.assertEqual(kind, dice.TokenKind.OPERATOR)

        kind = dice.get_kind('asbdasd')
        self.assertFalse(kind)

    def test_compute(self):
        result, steps = dice.compute(['1d4', '+', '17', '-', '2d6'])
        self.assertEqual(result, 14)
        self.assertEqual(steps[0], '(1)')
        self.assertEqual(steps[1], '+')
        self.assertEqual(steps[2], '17')
        self.assertEqual(steps[3], '-')
        self.assertEqual(steps[4], '(3+1)')

    def test_get(self):
        result, steps, kind = dice.get('15')
        self.assertEqual(result, 15)
        self.assertEqual(steps, ['15'])
        self.assertEqual(kind, dice.TokenKind.NUMBER)

        result, steps, kind = dice.get('4d5')
        self.assertEqual(result, 9)
        self.assertEqual(steps, [4,3,1,1])
        self.assertEqual(kind, dice.TokenKind.ROLL)

        result, steps, kind = dice.get('+')
        self.assertEqual(result, '+')
        self.assertEqual(steps, ['+'])
        self.assertEqual(kind, dice.TokenKind.OPERATOR)

        result, steps, kind = dice.get('-')
        self.assertEqual(result, '-')
        self.assertEqual(steps, ['-'])
        self.assertEqual(kind, dice.TokenKind.OPERATOR)

        self.assertRaises(
            TypeError,
            dice.get,
            'abcdsdw'
        )

    def test_get_step(self):
        res = dice.get_step(['2d6', '15'], token_kind=dice.TokenKind.ROLL)
        self.assertEqual(res, '(2d6+15)')

    def test_process_roll(self):
        result, steps = dice.process_roll(2, 15)
        self.assertEqual(result, 16)
        self.assertIn(7, steps)
        self.assertIn(9, steps)


if __name__ == "__main__":
    unittest.main()
