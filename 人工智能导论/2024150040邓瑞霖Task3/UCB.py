import numpy as np
import matplotlib.pyplot as plt
import EpsilonGreedy

class UCB(EpsilonGreedy.Solver):
    """UCB算法"""
    def __init__(self, bandit, coef, init_prob=1.0):
        super(UCB, self).__init__(bandit)
        self.total_count = 0
        self.estimates = np.array([init_prob] * self.bandit.K)
        self.coef = coef # UCB系数

    def run_one_step(self):
        self.total_count += 1
        ucb = self.estimates + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * (self.counts + 1)))
        # 选择上置信界最大的拉杆
        k = np.argmax(ucb)
        r = self.bandit.step(k)
        self.reward += r
        self.rewards.append(self.reward)
        self.estimates[k] += 1. /(self.counts[k] + 1) * (r - self.estimates[k])
        return k
    
if __name__ == "__main__":
    np.random.seed(1)
    bandit_10_arm = EpsilonGreedy.BernoulliBandit(10)
    np.random.seed(1)
    coef = 1 # 控制不确定性比重的系数
    UCB_solver = UCB(bandit_10_arm, coef)
    UCB_solver.run(5000)
    print('上置信界算法的累积懊悔为：', UCB_solver.regret)
    print('上置信界算法的累积奖励为：', UCB_solver.reward)
    EpsilonGreedy.plot_results([UCB_solver], ["UCB"], "UCB")

