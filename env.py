from random import choice
from copy import deepcopy


class Card(object):

    def __init__(self, init=False):
        self.number = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        if init:
            self.is_black = True
        else:
            self.is_black = choice([True, True, False])

    def value(self):
        n = self.number
        return n if self.is_black else -n

    def __str__(self):
        return str(self.value())

    def __repr__(self):
        return str(self.value())


# class State(object):
#
#     def __init__(self):
#         self.d_first = None
#         self.p_sum = None


class Easy21(object):

    def __init__(self):
        pass

    def is_bust(self, cards):
        s = self.sum_cards(cards)
        return True if s > 21 or s < 1 else False

    def sum_cards(self, cards):
        s = 0
        for card in cards:
            s += card.value()
        return s

    def init(self):
        return [Card(True)], [Card(True)], False, 0

    def step(self, action, d_cards, p_cards):
        if action == 'hit':
            p_cards_new = deepcopy(p_cards)
            p_cards_new.append(Card())
            if self.is_bust(p_cards_new):
                # print('got {}... busted!'.format(self.sum_cards(p_cards)))
                return d_cards, p_cards_new, True, -1
            return d_cards, p_cards_new, False, 0

        if action == 'stick':
            d_sum = 0
            d_cards_new = deepcopy(d_cards)
            while 0 <= d_sum < 17:
                d_cards_new.append(Card())
                d_sum = self.sum_cards(d_cards_new)
            if self.is_bust(p_cards):
                return d_cards_new, p_cards, True, -1
            if self.is_bust(d_cards):
                return d_cards_new, p_cards, True, 1
            p_sum = self.sum_cards(p_cards)
            if p_sum > d_sum:
                return d_cards_new, p_cards, True, 1
            elif p_sum < d_sum:
                return d_cards_new, p_cards, True, -1
            else:
                return d_cards_new, p_cards, True, 0
