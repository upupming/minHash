import numpy as np
import logging

class Set:
    def __init__(self, id):
        self.id = id
        self.set = {}
    def add(self, item_id):
        """
        Add a new item to the set.
        """
        self.set.add(item_id)

class Sets:

    def __init__(self, filepath, lines_limit=None):
        """
        读取文件并初始化成员变量用来保存集族
        """
        # 集族，维护成 dictionary 方便由集合编号快速获取集合
        self.sets = {}
        # 全集
        self.complete_set = set()
        with open(filepath, 'r') as inp:
            if lines_limit != None:
                lines = inp.readlines(lines_limit)
            else:
                lines = inp.readlines()
            for line in lines:
                # logging.info(line)
                [set_id, item_id] = np.fromstring(line, dtype=int, sep=' ')
                self.add_item_to_set(set_id, item_id)
                self.complete_set.add(item_id)
            # logging.info(self.str())
    def add_item_to_set(self, set_id, item_id):
        """
        If the set_id does not exist, it will be created.
        If the item_is has been added before, ignore it.
        """
        if not set_id in self.sets:
            # 创建 `set_id` 对应的集合
            self.sets[set_id] = set()
        # 快速索引到 `set_id` 对应的集合
        self.sets[set_id].add(item_id)
    def str(self):
        res = ''
        # 经过 profile 发现字符串连接比较耗时
        # for set_id in self.sets:
        #     res += f'编号为 {set_id} 的集合的所有元素如下\n'
        #     res += '\t['
        #     for item_id in self.sets[set_id]:
        #         res += f' {item_id}'
        #     res += ' ]\n\n'
        return res
    def get_num_of_sets(self):
        return len(self.sets)
    def get_U(self):
        """
        全集大小
        """
        return len(self.complete_set)