---
layout: post
title: When They are Talking Compound
updated: 2022-05-26
category: thoughts
comment_link: https://github.com/bGZo/blog/issues/7
---

## Compound / 复利 / 利滚利 / 驴打滚

我们可以通过减少复利的时间间隔, 来达到利息的最大化. (PS: 有上限)

## 复利和自然对数 e 的关系

### 自然对数的底 / 欧拉数 e 

- 假设有这样一个式子
  $\begin{align}  (1 + \frac{1}{n} )^n = x  \tag{1} \end{align}$

  - 当 $n=1$ 时, $x=2$
  
  - 当 $n \rightarrow \infty$ 时, 得到 $x = e = 2.7 1828 1828 45 90 45 ...$ 即 $e = \lim_{n \rightarrow \infty} (1+\frac{1}{n})^n$

- 泰勒展开: $e = \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + ...$

### 复利

单利即一年到头结算利息. 而多利则将一年分为多次结算利息. 即我们可以得到一个公式:

$\begin{align}  PV \times ( 1 + \frac{r}{n} ) ^ n = FV  \tag{2} \end{align}$

- $PV(Present Value)$ 为初值

- $r$ 为名义利率

- $n$ 为期数

- $FV(Future Value)$ 为终值 

则我们假设有 100 的本金, 银行说明具有 $10\%$ 的利率

- 月复利$(n=12)$: $100 \times ( 1 + \frac{0.1}{12} )^{12} = 110.47$

- 日复利$(n=365)$: $100 \times ( 1 + \frac{0.1}{365} )^{356} = 110.51$

- 连续复利 ($n \rightarrow \infty$), 此时 $(2)$ 后半部分 $(1 + \frac{r}{n} )^n = e ^ r$, 存在上限. 

后记: 我们可以将 周期内的固定 利率/回报率 定义为 $i(interest)$, 则 $(2)$ 将简化为:

$\begin{align}  PV \times ( 1 + i ) ^ n = FV \tag{3} \end{align}$

 从而得到回报率公式 

$\begin{align} \sqrt[n]{ ( \frac{FV}{PV} ) } - 1 \tag{4} \end{align}$


## 复利的谎言

- 不确定性: 世界是随机的. 复利是一种虚幻的确定性, **“确定性”的判断，本质而言，其实只是某种信念**.
- 连续性: 时间的连续无法作用事件连续发生.
- 回报对称性
  - 财富的委托代理机制的权利和责任是不对称的
    - > 代理人只会考虑如何尽可能地延长游戏的时间，以便自己能够获得更多的业绩提成，而不会考虑委托人的总体回报水平。--塔勒布《非对称风险》
  - 不懂期望值会导致**概率与赔付**之间的不对称
    - 重视概率忽视赔付在肥尾条件下会导致更大的问题
    - 肥尾条件下对实际分布估计的微小偏离都可能带来巨大的赔付偏差
    - > 由于存在非线性关系，市场参与者的概率预测误差和最终赔付误差完全是两类分布，概率预测误差是统计量，在0到1之间，因此误差分布是薄尾的，而赔付的误差分布是肥尾的。 塔勒布
- 现实不均匀
  - 不确定性的一部分，正是分布的“不均匀”
  - 正态分布/幂律分布/肥尾分布
- 幂律分布: 幂律表示的是两个量之间的函数关系，其中一个量的相对变化会导致另一个量的相应幂次比例的变化，且与初值无关：表现为一个量是另一个量的幂次方
- 肥尾分布: 相对于正态分布或指数分布表现出较大偏度或峰度的概率分布
- 预测, 下注, 决策即算命
- 贝叶斯
  - 随时在根据当前境况重新判断；
  - 打出无记忆的牌；
  - 不介意自打嘴巴；
  - 勇于自我更新。
- 长期主义
  - **大数定律**: 样本数量越多，则其算术平均值就有越高的概率接近期望值
- 复利神话, 一场反智的智力贩卖
  - 做正确的事情
  - 过于偏重把事情做正确
- 複利效應最有用的地方是在於投資自己成長、建立習慣、思考和練習的部分

## Refs

- [Compound interest - Wikipedia](https://en.wikipedia.org/wiki/Compound_interest )
- [李永乐老师讲自然对数的底e - YouTube](https://www.youtube.com/watch?v=2a6gDHfWQGA )
- [富人投資 | 复利效应並不會幫你致富？- YouTube](https://www.youtube.com/watch?v=uiYxUU-ejRc )
- [复利的谎言-Wechat Offical Acount](https://mp.weixin.qq.com/s/1pJSuOSrNIj4KPB0F8O54A )
