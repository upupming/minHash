# 随机算法实验 1 - 随机算法的优越性

<style>
/* Code word wrap for printing PDF */
pre div {
    white-space: pre-wrap;
    word-break: break-all;
}

section.eqno > span {
    width: 5em;
    text-align: right;
}

html,body {
  font-family: 'SimSun' 'Times New Roman';
}
</style>

<center>

主讲教师: 骆吉洲

姓名: 李一鸣    学号: 1160300625    日期: 2019 年 3 月 30 日

</center>

- [随机算法实验 1 - 随机算法的优越性](#%E9%9A%8F%E6%9C%BA%E7%AE%97%E6%B3%95%E5%AE%9E%E9%AA%8C-1---%E9%9A%8F%E6%9C%BA%E7%AE%97%E6%B3%95%E7%9A%84%E4%BC%98%E8%B6%8A%E6%80%A7)
  - [实验目的](#%E5%AE%9E%E9%AA%8C%E7%9B%AE%E7%9A%84)
  - [实验内容](#%E5%AE%9E%E9%AA%8C%E5%86%85%E5%AE%B9)
  - [实验设计](#%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1)
    - [Naive 算法](#naive-%E7%AE%97%E6%B3%95)
    - [minHash 算法](#minhash-%E7%AE%97%E6%B3%95)
  - [实验过程](#%E5%AE%9E%E9%AA%8C%E8%BF%87%E7%A8%8B)
    - [数据输入格式](#%E6%95%B0%E6%8D%AE%E8%BE%93%E5%85%A5%E6%A0%BC%E5%BC%8F)
    - [数据输出格式](#%E6%95%B0%E6%8D%AE%E8%BE%93%E5%87%BA%E6%A0%BC%E5%BC%8F)
  - [实验结果](#%E5%AE%9E%E9%AA%8C%E7%BB%93%E6%9E%9C)
    - [对比](#%E5%AF%B9%E6%AF%94)
    - [Naive 算法](#naive-%E7%AE%97%E6%B3%95-1)
    - [minHash 算法](#minhash-%E7%AE%97%E6%B3%95-1)

## 实验目的

- 进一步理解随机算法的概念
- 进一步理解随机算法简洁性
- 进一步理解随机算法高效性
- 观察 Hash 函数个数对算法性能的影响
- 根据实验结果，得出最佳的经验参数设置
- 规范书写实验报告

## 实验内容

- 输入：

    全集 $U$，集族 $R=\{r_1, \cdots, r_n\}, 阈值 c \in (0, 1]$

- 输出：

    任意两个集合之间的相似度定义为 $\text{sim}(r, s) = \frac{|r \cap s|}{|r \cup s|}$

    输出所有满足 $\text{sim}(r, s) \ge c$ 的所有组合 $<r, s> \in R \times R$，$<r, s>$ 与 $<r, s>$ 不重复出现。

- 问题: $n$ 取何值才能让概率可靠地逼近 $\text{sim}(A,B)$ ?
- 问题: 能否建立 false negative 与 $n$ 之间的关系？用实验得出经验公式来回答上述问题，绘制成图像比较直观。

1. 实现 Naive 算法
2. 实现 minHash 算法
3. 比较两种算法的运行结果是否一致
4. 设置不同Hash函数个数，查看运行效率差别
5. 设置不同Hash函数个数，比较返回结果差别
6. 总结得出确保最佳效果的Hash函数个数
7. 更换数据集，重复上述结果，得出一致的结论
8. 撰写实验报告

## 实验设计

### Naive 算法

Naive 算法的思想很简单，利用双重循环，两两之间计算集合的交集的元素个数和并集的元素个数，并相除得到 $\text{sim}$。

计算两个元素之间的并集、交集可以使用 C++ 的 [set_union](http://www.cplusplus.com/reference/algorithm/set_union/) 和 [set_intersection](http://www.cplusplus.com/reference/algorithm/set_intersection/)，它们的时间复杂度都是 `2*(count1+count2)-1`（`countX` 表示第 `X` 个集合中元素的个数）。

用 $m$ 表示 $R$ 中集合的个数，$s$ 表示每个集合的元素个数（为了简化计算，认为所有集合元素个数都是 $s$），算法总的时间复杂度为：

$$
\begin{aligned}
T_{naive}(m, s)
&= C_m^2 2 \cdot [2 (s+s)-1] \\
&= \frac{m(m-1)2(2s-1)}{2} \\
&= O(m^2s)
\end{aligned}
$$

可见直接使用 Naive 的代价是非常高的。

### minHash 算法

定理 1：

用 $\text{minHash}_P(A)$ 表示全集的随机排列 P 中首个属于 A 的行。那么有

$$
P[\text{minHash}_P(A)=\text{minHash}_P(B)] = \text{sim}(A, B)

\tag{1}
$$

$\text{minHash}_P$ 计算的示例的参见下图（1 表示元素在集合中，0 表示不在）：

![20190429024112.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429024112.png)

定理 1 的证明：

证明过程确实是比较巧妙的，不得不说自己很难想到。

1. 对于都是 0 的元素（如上面的 b），可以直接删除，因为它们在 A、B 中均不存在。删除之后再进行分析，后续每一行两列只有都是 1，或者是一个 1 一个 0 的情况。
    > 这样的『b』在实际中是可能出现的，比如一个生成集合的程序规定了全集中有 b，但是实际生成的任何一个集合中都不包含 b，虽然这个概率较小（随着 $n,m$ 的增加而越来越小），但是还是有可能的。
2. 将 $\text{sim}(A, B)$ 进行量化
    $$
    \begin{aligned}
    \text{sim}(A, B)
    &= \frac{两列都为 1}{两列都为 1 + 只有 1 列为 1} \\
    &= \frac{a}{a+b}
    \end{aligned}
    $$
3. 对于排列中的所有情况，我们只考虑第一行的元素，$\text{minHash}_P(A)=\text{minHash}_P(B)$ 表示第一行的元素同在两个集合中，对 $a$ 的贡献为 1，否则，对 b 的贡献为 1。
4. 综合上述分析，有：

    $$
    \begin{aligned}
    \text{sim}(A, B)
    &= \frac{a}{a+b} \\
    &= \frac{n[\text{minHash}_P(A)=\text{minHash}_P(B)]}{n[\text{minHash}_P(A)=\text{minHash}_P(B)] + n[\text{minHash}_P(A)\neq\text{minHash}_P(B)]} \\
    &= P[\text{minHash}_P(A)=\text{minHash}_P(B)]
    \end{aligned}
    $$

基于定理 1，我们提出了新的计算集合相似度的 minHash 算法。算法的一个运行例子如下：

1. 随机生成哈希函数 $h_i: U \to [0:U-1]$ 用来模拟第 $i$ 次取定的随机排列，$i \in [1,n]$

    比如现在选了 4 个随机排列：
    ![20190429031814.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429031814.png)

2. 定义 `minHash(i, k)` 函数表示排列 $h_i$ 下集合 $A_k$ 的 minHash 值。

    最开始需要初始化 minHash 值表，将表中的每一项初始化为无穷大。

    第一轮计算排列 $h_1$ 下所有集合的 minHash 值：

    ![20190429032436.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429032436.png)

        For 全集 U 中的每个元素（这里是 a, b, c, d） e，找到其 hash 值 h[1](e)
            For 每一个集合 A[k]
                如果此元素在集合 A[k] 中，而且其哈希值小于表中的哈希值，则进行更新

    如此重复，直到执行完所有的排列。

3. 对任意集合 $A, B$，计算估计的相似度：

    $$
    \widehat{\text{sim}}(A, B) = \frac{A、B两列相等行数}{n}
    $$

    > 由于可能出现空集，这个时候表中的值就是无穷大，由于空集与任意集合的相似度都为 0，所以遇到无穷大与其他元素比较时，直接认为不相等（即使两个都是无穷大）。

4. 输出满足条件 $\widehat{\text{sim}}(r, s) \ge c$ 的集合组 $<r, s>$。

设全集 $u$ 中元素的个数为 $u$，算法总的时间复杂度为：

$$
\begin{aligned}
T(n,u,m)
&= n \cdot u \cdot m + C_m^2 \cdot n = O(mnu+m^2n)
\end{aligned}
$$

相比于 Naive 算法，minHash 算法的性能优势主要体现在当 $s$ 太大时，能以更快的速度获取 minHash 值来进行估算。$s$ 的取值一般随着集合的数量而增加，导致 Naive 算法性能变差，而 minHash 算法则依赖 $n$ 的选取大小，$n$ 越大，结果越精确，但时间复杂度也越高。我们的目的就是用实验计算 $n$ 与 false negative 之间的关系。

## 实验过程

### 数据输入格式

集合数据从文件读入，文件的格式为很多行，每一行的格式为 `<集合编号 i> <元素编号j>`，表示第 $i$ 个集合包含了第 $j$ 个元素。比如一个输入例子如下：

```txt
1 1
1 10
10 86
10 87
10000 198
100000 217
```

第一行表示有一个集合的编号为 1，其中有一个元素 1。

输入中可能有完全相同的两行，对于后续出现的已经在集合中的元素，算法中再进行加入时会忽略。

> 注意到集合编号并不是按照顺序来的，我们可以只在遇到新的之前没遇到过的集合编号时，才新建集合，而不是使用编号来 顺序分配集合。

一个 `Sets` 类中维护一个名为 `sets` 的 dictionary 方便快速由集合编号定位到集合，集合的总个数直接由 `sets` 的大小确定，实现相应的 `get` 函数来获取集合数量。

### 数据输出格式

首先输出每个集合所有的集合元素，然后对每个集合，输出其与其他集合的相似度信息，如果满足大于等于 $c$ 的条件，输出一行 `similarity(i, j) >= c`。

下面是使用课件中的 demo 进行运行得到的输出文件格式。

```txt
编号为 1 的集合的所有元素如下
	[ 1 4 ]

编号为 2 的集合的所有元素如下
	[ 1 3 4 ]


==== Begin 集合 1 ====
2 2/3=0.6666666666666666
similarity(1, 2) >= 0
==== End 集合 1 ====

==== Begin 集合 2 ====
==== End 集合 2 ====
```

由于实际测试发现 python 的 logging 比较耗时，如果把 log 操作嵌套在算法的双重循环内部的话，对于 10000 行的文件，占用了 22 秒内的 18.5 秒，因此实际运行时大文件时并不会输出这么多信息。

![20190429204429.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429204429.png)

经过优化之后，仅打印单纯的集合对，采用数组存储当前所有的 log 信息，在算法结束之后再打印，这样运行一遍 10000 行的文件只需要 1.379 秒，profiler 输出如下：

![20190429210736.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429210736.png)

日志文件大小为 1.32MB，截图如下：

![20190429210940.png](https://picgo-1256492673.cos.ap-chengdu.myqcloud.com/img/20190429210940.png)

## 实验结果

实测显示 `linux_distinct` 测试样例一共有 337509 个集合，这样进行双重循环即使不进行任何操作也运行不完，我特意进行了下面的测试。

```py
import time

def round_trip(limit):
    a = time.time()
    for i in range(limit):
        for j in range(limit):
            pass
    b = time.time()
    print(limit, b - a)

for limit in range(0, 10000, 1000):
    round_trip(limit)
```

```txt
1000 0.03597760200500488
2000 0.13292551040649414
3000 0.28983116149902344
4000 0.5486869812011719
5000 0.7975189685821533
6000 1.2402865886688232
7000 1.62306809425354
8000 2.1377904415130615
9000 2.932292938232422
```

按照这个趋势，330000 的双重循环需要 0.0359 * 330^2 = 3909s = 50min，这个时间完全接受不了，因此在所有的测试用例中都选取前 10000 行来进行测试。

### 对比

### Naive 算法


|测试样例|运行时间/秒|日志文件大小|
|-------|---------|---------|
|demo|忽略不计|忽略不计|
|linux_distinct，前 10000 行|0.670|1361KB|
|Delicious_out，前 10000 行|0.265|410KB|
|AOL_out，前 10000 行|0.01|2KB|

### minHash 算法

实际写代码时使用的是 [`shuffle`](https://stackoverflow.com/a/976918/8242705) 来生成随机排列的，这就遇到了一个问题，前后生成的两个随机排列可能是相同的，但是，可以证明，任何一个随机排列产生两次或多次的概率也是相同的，因此不会影响到概率的估计。

|测试样例|运行时间/秒|日志文件大小|
|-------|---------|---------|
|demo|忽略不计|忽略不计|
|linux_distinct，前 10000 行，n=1000|53|1751KB|
|Delicious_out，全部内容|0.265|410KB|
|AOL_out，全部内容|0.01|2KB|


