import logging
from pathlib import Path
import cProfile, pstats, io
from naive import *
from minHash import *

# See https://osf.io/upav8/
def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


@profile
def round_trip(case_name, algorithm, c, n=0):
    """
    运行一遍算法，case_name 必须对应 data 文件夹中的文件的 basename

    algorithm 算法类型

    c 是指定的阈值
    """
    fileh = logging.FileHandler(f'log/{algorithm}_{case_name}.log', 'w', encoding='utf-8')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(message)s')
    fileh.setFormatter(formatter)

    log = logging.getLogger()  # root logger
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fileh)      # set the new handler
    log.setLevel(logging.WARNING)

    case_filepath = Path(f'./data/{case_name}.txt').absolute()
    
    if algorithm == 'naive':
        # Naive 算法太慢，因此只运行前 10000 行
        case_sets = SetsNaive(case_filepath, 10000)
        case_sets.run(c)
    elif algorithm == 'minHash':
        case_sets = SetsMinHash(case_filepath)
        case_sets.run(n, c)
    