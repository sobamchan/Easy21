import env
from collections import defaultdict
from random import random
from random import choice
from tqdm import tqdm
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from pprint import pprint


N0 = 1000


class MC(object):

    def __init__(self):
        self.env = env.Easy21()
        self.V = defaultdict(lambda: 0)
        self.NS = defaultdict(lambda: 0)
        self.NA = defaultdict(lambda: 0)
        self.S = defaultdict(lambda: 0)
        self.Q = defaultdict(lambda: 0)
        self.RI = 0
        self.hit_n = 0
        self.stick_n = 0

    def init_N(self):
        self.NS = defaultdict(lambda: 0)
        self.NA = defaultdict(lambda: 0)

    def pick_action(self, d, p):
        d_sum = self.env.sum_cards(d)
        p_sum = self.env.sum_cards(p)
        hit_v = self.Q[d_sum, p_sum, 'hit']
        stick_v = self.Q[d_sum, p_sum, 'stick']
        return 'hit' if hit_v >= stick_v else 'stick'

    def eps_geedy(self, d, p):
        d_sum = self.env.sum_cards(d)
        p_sum = self.env.sum_cards(p)
        eps = N0 / (N0 + self.NS[d_sum, p_sum])
        # eps = 0.1
        if random() < eps:
            self.RI += 1
            action = choice(['hit', 'stick'])
            self.hit_n += 1 if action == 'hit' else 0
            self.stick_n += 1 if action == 'stick' else 0
            return action
        else:
            action = self.pick_action(d, p)
            self.hit_n += 1 if action == 'hit' else 0
            self.stick_n += 1 if action == 'stick' else 0
            return action

    def one_episode(self, i):
        d, p, e, r = self.env.init()
        # self.init_N()
        total_reward = 0
        elap_step = 0
        episode_exp = []
        while not e:
            action = self.eps_geedy(d, p)
            dn, pn, e, r = self.env.step(action, d, p)
            total_reward += r
            d_sum = self.env.sum_cards(d)
            p_sum = self.env.sum_cards(p)
            self.NS[d_sum, p_sum] += 1
            self.NA[d_sum, p_sum, action] += 1
            episode_exp.append([d_sum, p_sum, action, r])
            elap_step += 1
            # if i % 1000 == 1:
            #     print(action)
            #     print('dealer before sum: ', d_sum)
            #     print('dealer before cards: ', d)
            #     print('player before sum: ', p_sum)
            #     print('player before cards: ', p)
            #     print()
            #     print('dealer after sum: ', self.env.sum_cards(dn))
            #     print('dealer after cards: ', dn)
            #     print('player after sum: ', self.env.sum_cards(pn))
            #     print('player after cards: ', pn)
            #     print()
            #     print(e)
            #     print(r)
            #     input()
            d = deepcopy(dn)
            p = deepcopy(pn)

        g = total_reward
        for d_sum, p_sum, action, r in episode_exp:
            diff = g - self.Q[d_sum, p_sum, action]
            self.Q[d_sum, p_sum, action] += \
                diff / self.NA[d_sum, p_sum, action]

        return total_reward

    def learn(self, args):
        total_reward = 0
        iter_n = args.i
        episode_rewards_accum = []
        for i in tqdm(range(iter_n), total=iter_n):
            reward = self.one_episode(i)
            total_reward += reward
            episode_rewards_accum.append(total_reward)

        print('avg win: ', total_reward / iter_n)
        # print(set(list(self.Q.values())))
        # print(set(list(self.NA.values())))
        # print(set(list(self.NS.values())))
        # print('random choise ratio', self.RI / iter_n)
        # print('hit n:', self.hit_n)
        # print('stick n:', self.stick_n)
        # pprint(self.Q)

        if args.p1:
            X = []
            Y = []
            Z = []
            for k, v in self.Q.items():
                X.append(k[0])
                Y.append(k[1])
                Z.append(v)
            fig = plt.figure()
            ax = Axes3D(fig)
            ax.scatter3D(np.ravel(X), np.ravel(Y), np.ravel(Z))
            plt.show()
        if args.p2:
            X = range(len(episode_rewards_accum))
            Y = episode_rewards_accum
            plt.bar(X, Y)
            plt.savefig('./episode_rewards_accum_{}.png'.format(str(iter_n)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int)
    parser.add_argument('-p1', type=int, default=0)
    parser.add_argument('-p2', type=int, default=0)
    args = parser.parse_args()
    mc = MC()
    mc.learn(args)
