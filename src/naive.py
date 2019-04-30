import logging
import data_reader
from round_trip import *

class SetsNaive(data_reader.Sets):
    """
    在 Sets 基础上实现 Naive 算法
    """
    def run(self, c):
        """
        c 为阈值

        返回一个数组，数组中的每个元素为一个二维数组，表示一个满足条件的集合对
        """
        logging.warning(f'阈值 c = {c}')
        log = []
        num_of_sets = self.get_num_of_sets()
        # 将 dict_keys 转换为可索引的 list
        dict_keys_list = list(self.sets.keys())
        for i in range(num_of_sets):
            keyi = dict_keys_list[i]
            seti = self.sets[keyi]
            logging.info(f'==== Begin 集合 {keyi} ====')
            for j in range(i+1, num_of_sets):
                keyj = dict_keys_list[j]
                setj = self.sets[keyj]
                intersection = seti & setj
                union = seti | setj
                similarity = len(intersection) / len(union)
                logging.info(f'{keyj} {len(intersection)}/{len(union)}={similarity}')
                
                if similarity >= c:
                    # logging.warning(f'similarity({keyi}, {keyj}) >= {c}')
                    log.append(
                        [keyi, keyj, similarity]
                    )
            logging.info(f'==== End 集合 {keyi} ====\n')
        logging.warning(log)
        return log

if __name__ == "__main__":
    round_trip('demo', 'naive', 0)
    round_trip('linux_distinct', 'naive', 0)
    round_trip('Delicious_out', 'naive', 0)
    round_trip('AOL_out', 'naive', 0)