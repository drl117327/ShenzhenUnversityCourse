import numpy as np
import matplotlib.pyplot as plt
import EpsilonGreedy

class ThompsonSampling(EpsilonGreedy.Solver):
    """汤普森采样算法"""
    def __init__(self, bandit):
        super(ThompsonSampling, self).__init__(bandit)
        # 列表，表示每根拉杆奖励为1的次数
        self._a = np.ones(self.bandit.K)
        # 列表，表示每根拉杆奖励为0的次数
        self._b = np.ones(self.bandit.K)
    
    def run_one_step(self):
        # 按照Beta分布采样一组奖励样本
        samples = np.random.beta(self._a, self._b)
        # 选出采样奖励最大的拉杆
        k = np.argmax(samples)
        r = self.bandit.step(k)
        self.reward += r
        self.rewards.append(self.reward)
        # 更新Beta分布的第一个参数
        self._a[k] += r
        # 更新Beta分布的第二个参数
        self._b[k] += (1 - r)
        return k

if __name__ == "__main__":
    np.random.seed(1)
    bandit_10_arm = EpsilonGreedy.BernoulliBandit(10)
    np.random.seed(1)
    thompson_sampling_solver = ThompsonSampling(bandit_10_arm)
    thompson_sampling_solver.run(5000)
    print('汤普森采样算法的累积懊悔为：', thompson_sampling_solver.regret)
    print('汤普森采样算法的累积奖励为：', thompson_sampling_solver.reward)
    EpsilonGreedy.plot_results([thompson_sampling_solver], ["ThompsonSampling"], "ThompsonSampling")
