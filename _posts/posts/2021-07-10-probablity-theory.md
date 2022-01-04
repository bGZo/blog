---
layout: post
title: Probablity Theory Notes
updated: 2021-06-10
category: posts
---

总的来说. 今天概率论考完了, 总还是对受到的教育有很多遗憾的, 因为自己确实什么都没有学到, 总是在期末前做几套同同学要来的卷子, 然后直接上去考, 没有什么自己的思考和联系, 总还是别扭.

- **"生日问题" / "生日悖论"**: 这学期最有意思, 也最有实践意义的就是第一节课 -- 引入概率论中提到的一个简单问题: "生日问题". 
  - **问题**: *假设一年有 n 天(365/355), 要使两个人生日相等的概率的人数应该为多少?*
  - 思路: 问题转化为 `1-P(两两各不相等)` 的概率问题
  - 得到: `(假设一年365天)`  1 - 365! / 365<sup>n</sup> \* (365-n)!  (*推导过程详细见: https://zh.wikipedia.org/wiki/%E7%94%9F%E6%97%A5%E5%95%8F%E9%A1%8C*), 或者 <img  src="https://latex.codecogs.com/svg.image?\prod_{k=1}^{n-1}(1-\frac{k}{365})"  title="\prod_{k=1}^{n-1}(1-\frac{k}{365})" />
  - 进一步统计计算:
  - ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/1280px-Birthday_paradox_approximation.svg.webp)
  - | *n*  | *p*（*n*）                       |
    | ---- | -------------------------------- |
    | 10   | 12%                              |
    | 20   | 41%                              |
    | 30   | 70%                              |
    | 50   | 97%                              |
    | 100  | 99.99996%                        |
    | 200  | 99.9999999999999999999999999998% |
    | 300  | 1 −（7×10<sup>−73</sup>）        |
    | 350  | 1 −（3×10<sup>−131</sup>）       |
  | ≥366 | 100%                             |
  
- 随机变量也是一个函数, 是事件到抽象的约束, 一种映像关系
  
- 概率分布 与 概率
  - 概率分布
  - 概率
    - 概率 质量/分布 函数(PMF): <img src="https://latex.codecogs.com/svg.image?P_{i}=P(x_{i})=p(X=x_{i})" title="P_{i}=P(x_{i})=p(X=x_{i})" />
    - 概率 密度 函数(PDF) => 累计分布函数(CDF)(单调有界右连续)
    - ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/637615279826892268.webp)

- 证明连续性
  - ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/637615264057320450.webp)
  
- 超几何分布实质是不放回抽样. 几何分布实质是二项分布的具体某例.
  - 移步知乎: https://www.zhihu.com/question/38191693/answer/75277085
  
- **矩**的含义
  - 力矩=力臂×力
    - **意义**
      - 一阶原点距 -> 平均值; 二阶原点矩 -> 平均能量; 
      - 一阶中心矩 -> 0; 二阶中心矩 -> 方差; 三阶中心矩也叫偏度; 四阶中心矩也叫峭度或者峰度
    - 移步知乎: 
    - https://zhuanlan.zhihu.com/p/57802400
  
- 为什么连续型随机变量的概率密度函数不一定连续
  
- https://www.zhihu.com/question/437683132
  
- 卷积(convolution)为什么叫「卷」积(「convolut」ion)？
  
- https://www.zhihu.com/question/54677157
  
- 三大公理
  - 非负公理
  - 规范公理
  - 可加公理

- 相容 独立 互斥
  - ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/Screenshot%202021-07-10%20151353.webp)
  - 移步知乎: https://zhuanlan.zhihu.com/p/36607363

- 中心极限定理与大数定律
  - 大数定律 -> 样本收敛于总体均值
- 中心极限定理 -> 总体趋于正态分布
  - 移步知乎:
    - https://www.zhihu.com/question/22913867
  
- 有没有懂统计的，标准误为什么等于标准差除以根号n，求公式推导过程？
  - https://www.zhihu.com/question/21744800 
  
- 为什么样本均值的标准差是总体均值标准差除以根号n?
  - https://www.zhihu.com/question/33394664
  
- 为什么样本方差（sample variance）的分母是 n-1？
  -  https://www.zhihu.com/question/20099757/answer/312670291
  
- 伽玛(gamma) 分布？
  - (做题层的) **性质**:
    - <img  src="https://latex.codecogs.com/svg.image?\tau&space;(x)=\int_{0}^{&plus;\infty}&space;t^{x-1}&space;e^{-t}&space;dt,&space;x>0"  title="\tau (x)=\int_{0}^{+\infty} t^{x-1} e^{-t} dt, x>0" />
    - <img  src="https://latex.codecogs.com/svg.image?\tau&space;(x&plus;1)=x\tau(x),&space;\forall&space;x>0"  title="\tau (x+1)=x\tau(x), \forall x>0" />
    - <img  src="https://latex.codecogs.com/svg.image?\tau&space;(1)=1,&space;\tau(\frac{1}{2})=\sqrt{\pi}"  title="\tau (1)=1, \tau(\frac{1}{2})=\sqrt{\pi}" />
    - <img  src="https://latex.codecogs.com/svg.image?\tau&space;(n)=(n-1)!,\forall&space;n\in&space;N_{&plus;}"  title="\tau (n)=(n-1)!,\forall n\in N_{+}" />
  - 更多专业化的解答移步知乎: 
    - https://www.zhihu.com/question/34866983
    - https://www.zhihu.com/question/31407058

- <img src="https://latex.codecogs.com/svg.image?Var(x)=D(x)" title="Var(x)=D(x)" />
- 若随机变量X的分布函数 <img src="https://latex.codecogs.com/svg.image?F_{x}(X)" title="F_{x}(X)" /> 为严格单调增的连续函数, 那么有 <img src="https://latex.codecogs.com/svg.image?Y=F_{x}(X)\sim&space;U(0,1)" title="Y=F_{x}(X)\sim U(0,1)" />, 如 <img src="https://latex.codecogs.com/svg.image?U&space;=&space;1-&space;e^{-\lambda&space;X}&space;\sim&space;U(0,1)" title="U = 1- e^{-\lambda X} \sim U(0,1)" />

