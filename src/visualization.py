import matplotlib.pyplot as plt
from naive import *
from minHash import *
import logging
logging.getLogger().setLevel(logging.ERROR)

def save_to_file(filename):
    plt.savefig(Path(f'./figures/{filename}.svg').absolute())

def cal_false_positive(real, estimization, c):
    # 必须都包含了所有的组合情况
    assert len(real) == len(estimization)
    total = 0
    false_positive = 0
    length = len(real)
    for i in range(length):
        total += 1
        # false but report as positive
        if real[i][2] < c and estimization[i][2] >= c:
            false_positive += 1
    return false_positive / total

if __name__ == "__main__":    
    case_name = 'linux_distinct'
    case_filepath = Path(f'./data/{case_name}.txt').absolute()

    naive_tester = SetsNaive(case_filepath, 10000)
    result_naive = naive_tester.run(0)

    n_max = 100
    n_step = 10
    n_trips = n_max // n_step
    # 总共 100/10 = 10 个结果，每个结果是一个二维数组，长度未知
    minHash_tester = SetsMinHash(case_filepath, 10000)
    results_minHash = np.empty((n_trips, len(result_naive), 3))
    false_positives = np.empty((n_trips))
    
    for i in range(n_trips):
        n = n_step * (i+1)
        result_minHash = minHash_tester.run(n, 0)
        results_minHash[i] = result_minHash
        false_positives[i] = cal_false_positive(result_naive, result_minHash, 0.5)
    plt.plot(np.arange(n_step, n_max+n_step, n_step), false_positives)

    plt.legend()
    plt.title('False positive - n curve')
    plt.xlabel('n')
    plt.ylabel('False positive')
    save_to_file('result')
