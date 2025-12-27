import numpy as np
import matplotlib.pyplot as plt

class BernoulliBandit:
    """伯努利多臂老虎机,输入K表示拉杆个数"""
    def __init__(self, K):
        # 随机生成K个0~1的数，作为拉动每根拉杆的获奖
        self.probs = np.random.uniform(size=K)
        # 获取概率最大的拉杆
        self.best_idx = np.argmax(self.probs)
        # 最大的获奖概率
        self.best_prob = self.probs[self.best_idx]
        self.K = K
    
    def step(self, K):
        # 当玩家选择了K号拉杆后,根据拉动该老虎机的K号拉杆获得奖励的概率返回1（获奖）或0（未获奖）
        if np.random.rand() < self.probs[K]:
            return 1
        else:
            return 0

class Solver:
    """多臂老虎机算法基本框架"""
    def __init__(self, bandit):
        self.bandit = bandit
        self.counts = np.zeros(self.bandit.K)  # 每根拉杆的尝试次数
        self.regret = 0  # 当前步的累积懊悔
        self.reward = 0  # 当前步的累积奖励
        self.actions = []  # 维护一个列表，记录每一步的动作
        self.regrets = []  # 维护一个列表，记录每一步的累积懊悔
        self.rewards = []  # 维护一个列表，记录每一步的奖励

    def update_regret(self, k):
        # 计算累积懊悔并保存,k为本次动作选择的拉杆的编号
        self.regret += self.bandit.best_prob - self.bandit.probs[k]
        self.regrets.append(self.regret)

    def run_one_step(self):
        # 返回当前动作选择哪一根拉杆,由每个具体的策略实现
        raise NotImplementedError

    def run(self, num_steps):
        # 运行一定次数,num_steps为总运行次数
        for _ in range(num_steps):
            k = self.run_one_step()
            self.counts[k] += 1
            self.actions.append(k)
            self.update_regret(k)

def plot_results(solvers, solver_names, way):
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    for idx, solver in enumerate(solvers):
        time_list = range(len(solver.regrets))
        plt.plot(time_list, solver.regrets, label=solver_names[idx])
    plt.xlabel('Time steps')
    plt.ylabel('Cumulative regrets')
    plt.title('%d-armed bandit' % solvers[0].bandit.K)
    plt.legend()
    plt.subplot(1, 2, 2)
    for idx, solver in enumerate(solvers):
        time_list = range(len(solver.rewards))
        plt.plot(time_list, solver.rewards, label=solver_names[idx])
    plt.xlabel('Time steps')
    plt.ylabel('Cumulative rewards')
    plt.title('%d-armed bandit' % solvers[0].bandit.K)
    plt.legend()
    plt.savefig('MAB_' + way + '.png')
    plt.show()

class EpsilonGreedy(Solver):
    """ epsilon贪婪算法,继承Solver类 """
    def __init__(self, bandit, epsilon=0.01, init_prob=1.0):
        super(EpsilonGreedy, self).__init__(bandit)
        self.epsilon = epsilon
        # 初始化拉动所有拉杆的期望奖励估值
        self.estimates = np.array([init_prob] * self.bandit.K)

    def run_one_step(self):
        if np.random.random() < self.epsilon:
            k = np.random.randint(0, self.bandit.K)  # 随机选择一根拉杆
        else:
            k = np.argmax(self.estimates)  # 选择期望奖励估值最大的拉杆
        r = self.bandit.step(k)  # 得到本次动作的奖励
        self.estimates[k] += 1. / (self.counts[k] + 1) * (r - self.estimates[k])
        self.reward += r
        self.rewards.append(self.reward)
        return k


if __name__ == "__main__":
    np.random.seed(1)  # 设定随机种子,使实验具有可重复性
    K = 10
    bandit_10_arm = BernoulliBandit(K)
    np.random.seed(1)
    # 不同epsilon值的epsilon-贪心算法
    # epsilon_greedy_solver = EpsilonGreedy(bandit_10_arm, epsilon=0.01)
    # epsilon_greedy_solver.run(5000)
    # print('epsilon-贪心算法的累积懊悔为:', epsilon_greedy_solver.regret)
    # print('epsilon-贪心算法的累积奖励为:', epsilon_greedy_solver.reward)
    # plot_results([epsilon_greedy_solver], ["EpsilonGreedy"], "EpsilonGreedy")
    np.random.seed(0)
    epsilons = [1e-4, 0.01, 0.1, 0.25, 0.5]
    epsilon_greedy_solver_list = [
        EpsilonGreedy(bandit_10_arm, epsilon=e) for e in epsilons
    ]
    epsilon_greedy_solver_names = ["epsilon={}".format(e) for e in epsilons]
    for solver in epsilon_greedy_solver_list:
        solver.run(5000)

    plot_results(epsilon_greedy_solver_list, epsilon_greedy_solver_names, "EpsilonGreedy_Compare")