import logging
import data_reader
from round_trip import *
import numpy as np
import random

class SetsMinHash(data_reader.Sets):
    """
    在 Sets 基础上实现 minHash 算法
    """

    def get_hash_function(self, U):
        """
        返回一个数组，表示 [0, U-1] 到 [0, U-1] 的映射
        """
        hash_func = [i for i in range(U)]
        random.shuffle(hash_func)
        # print('hash_func', hash_func)
        return hash_func

    def run(self, n, c):
        """
        c 为阈值
        """
        logging.warning(f'哈希函数个数 n = {n}，阈值 c = {c}')
        log = []
        # 初始化 minHash 表
        num_of_rows = n
        num_of_cols = num_of_sets = self.get_num_of_sets()
        minHash_table = np.full((num_of_rows, num_of_cols), 0xFFFFFFFF)

        # 将 dict_keys 转换为可索引的 list
        # 有序的 set 编号
        dict_keys_list = list(self.sets.keys())
        # 有序的全集 list
        complete_set_list = list(self.complete_set)
        # i 表示 h_1, h_2, ...
        for i in range(n):
            hash_func = self.get_hash_function(self.get_U())
            # u 表示当前选取的全集中的元素的索引
            u = 0
            # e 表示 a, b, c, d, ...
            for e in self.complete_set:
                # print(f'考虑全集中的第 {u} 个元素 {e}，它被映射为 {hash_func[u]}')
                # k 表示 1, 2, ..., m
                for k in range(num_of_sets):
                    keyk = dict_keys_list[k]
                    setk = self.sets[keyk]
                    if e in setk:
                        # print(f'元素 {e} 属于集合 {keyk}')
                        minHash_table[i][k] = min(minHash_table[i][k], 
                            hash_func[u])
                        # print(minHash_table)
                u += 1

        # print('minHash_table', minHash_table)

        # 统计每两个集合之间的相似度，存入 log
        for i in range(num_of_sets):
            for j in range(i+1, num_of_sets):
                # https://stackoverflow.com/a/4455154/8242705
                # https://stackoverflow.com/a/25490688/8242705
                similarity = np.sum(minHash_table[:,i] == minHash_table[:,j])
                # print(f'第 {i} 个集合与第 {j} 个集合相同行数为 {similarity}')
                similarity = similarity / n
                if (similarity >= c):
                    log.append(
                        [dict_keys_list[i], dict_keys_list[j], similarity]
                    )
        logging.warning(log)
        return log

        
if __name__ == "__main__":
    # round_trip('demo', 'minHash', c=0, n=20)
    round_trip('linux_distinct', 'minHash', c=0, n=1000)
    # roundTrip('Delicious_out', 0)
    # roundTrip('AOL_out', 0)
    # import cProfile
    # import re
    # cProfile.run("roundTrip('linux_distinct', 0)")
