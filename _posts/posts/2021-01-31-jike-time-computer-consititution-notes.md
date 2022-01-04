---
layout: post
title: Jike Time Computer Consititution Notes
updated: 2021-01-31
category: posts
---

课程来源: [深入浅出计算机组成原理-徐文浩](https://time.geekbang.org/column/intro/100026001)

<!--more-->

## PREFACE 

### Von Neumann Architecture/ Princeton Architecture

冯·诺依曼体系/普林斯顿架构, 即**存储程序计算机**, 冯·诺依曼基于当时在秘密开发的EDVAC写了一篇报告 [First Draft of a Report on the EDVAC(First Draft)](https://en.wikipedia.org/wiki/First_Draft_of_a_Report_on_the_EDVAC).

> Von Neumann describes a detailed design of a "very high speed automatic digital computing system." He divides it into six major subdivisions: a central arithmetic part, CA, a central control part, CC, memory, M, input, I, output, O, and(slow)external memory, R, such as punched cards, Teletype tape, or magnetic wire or steel tape.
>
> The CA will perform addition, subtraction, multiplication, division and square root. Other mathematical operations, such as logarithms and trigonometric functions are to be done with table look up and interpolation, possibly biquadratic. He notes that multiplication and division could be done with logarithm tables, but to keep the tables small enough, interpolation would be needed and this in turn requires multiplication, though perhaps with less precision.
>
> Numbers are to be represented in binary notation. He estimates 27 binary digits(he did not use the term "bit," which was coined by Claude Shannon in 1948)would be sufficient(yielding 8 decimal place accuracy)but rounds up to 30-bit numbers with a sign bit and a bit to distinguish numbers from orders, resulting in 32-bit word he calls a minor cycle. Two’s complement arithmetic is to be used, simplifying subtraction. For multiplication and division, he proposes placing the binary point after sign bit, which means all numbers are treated as being between −1 and +1 and therefore computation problems must be scaled accordingly.<sup>[1](#j1)</sup>

- 包含算术逻辑单元(Arithmetic Logic Unit, ALU)和处理器寄存器(Processor Register)的**处理器单元 (Processing Unit)/ 数据通路(Datapath)/ 运算器**. 
- 包含指令寄存器(Instruction Reigster)和程序计数器(Program Counter)的 **控制器单元(Control Unit/CU)** .
    - **PU+CU=CPU**, **Central Processing Unit, 中央处理器**
- 存储数据(Data)和指令(Instruction)的 **内存**(Memory) . 以及更大容量的 **外部存储**.
- **各种 输入和输出设备 输入和输出设备 , 以及对应的输入和输出机制**.
    - 通过主板上的 **南桥(SouthBridge)**芯片组, 来控制和CPU之间的通信
    - 以前的主板上通常也有“北桥”芯片, 用来作为“桥”, **连接CPU和内存、显卡之间的通信**. 不过, 随着时间的变迁, 现在的主板上的“北桥”芯片的工作, 已经被移到了CPU的内部.

以上一共五部分. 以下为补充:

- **主板 (Motherboard)**: 主板的 芯片组 (Chipset)和 总线 (Bus)解决了CPU和内存之间如何通信的问题. 芯片组控制了数据传输的流转, 也就是数据从哪里到哪里的问题. 总线则是实际数据传输的高速公路. 因此,  **总线速度(Bus Speed)**决定了数据能传输得多快. 
    - 主板都带了内置的显卡
- **显卡(Graphics Card)**
    - **GPU(Graphics Processing Unit, 图形处理器)**
- 冯·诺依曼体系是一个“ 可编程 ”计算机, 也是一个“ 存储 ”计算机. 
    - **不能存储程序**的计算机: **Plugboard**, 插线板式的计算机, 但是是"可编程"的.
- 图灵机 (Turing Machine)& 冯·诺依曼机 ?

### Map

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/co-map.webp)

### Performance

- **性能**: 响应频率挂钩.
    - **响应时间(Response time) / 执行时间(Execution time)**: 想要提升响应时间这个性能指标, 你可以理解为让计算机“跑得更快”
- **吞吐率(Throughput) / 带宽(Bandwidth)**
    - **SPEC(Standard Performance Evaluation Corporation)**的第三方机构, 专门用来指定各种“跑分”的规则. 
        - 这些程序丰富多彩, 有编译器、解释器、视频压缩、人工智能国际象棋等等, 涵盖了方方面面的应用场景. 
        - https://www.spec.org/cpu2017/results/cpu2017.html
- **计时**
    - Wall Clock Time / Elapsed Time不“准”
        - CPU多任务带来的额外干扰更强
        - 读取数据消耗在网络 / 硬盘 上.
        - 满载 / 降频 运行状态.
    - `time` command.

```shell
$ time seq 1000000 | wc -l
# 1000000
# real 0m0.101s
# user 0m0.031s
# sys 0m0.016s
```

- 晶振: 晶体振荡器(Oscillator Crystal), 计数器.
- **程序的 CPU 执行时间 = CPU 时钟周期数(CPU Cycles) × 时钟周期时间(Clock Cycle)**
    - **CPU 时钟周期数 = 指令数 × 每条指令的平均时钟周期数(Cycles Per Instruction, CPI)"** 不同的指令需要的 Cycles 是不同的. 
    - **程序的 CPU 执行时间 = 指令数 × CPI × Clock Cycle Time**
        - **时钟周期时间**, 主频, CPU 的一个“钟表”能够识别出来的最小的时间间隔. 比如 80386 主频只有 33MHz
        - **每条指令的平均时钟周期数 CPI**, 就是一条指令到底需要多少 CPU Cycle. 在后面讲解CPU 结构的时候, 我们会看到, 现代的 CPU 通过流水线技术(Pipeline), 让一条指令需要的 CPU Cycle 尽可能地少. 因此, 对于 CPI 的优化, 也是计算机组成和体系结构中的重要一环. 
        - **指令数**, 代表执行我们的程序到底需要多少条指令、用哪些指令. 这个很多时候就把挑战交给了编译器. 同样的代码, 编译成计算机指令时候, 就有各种不同的表示方式. 
- 跑分如何“作弊”?

### Promote

- **CPU**, 超大规模集成电路(Very-Large-Scale Integration, VLSI)都是一个个晶体管组合而成的, 通电让晶体管里面的“开关”不断地去“打开”和“关闭”, 来组合完成各种运算和功能. 
- **功耗问题**: 
    - **功耗 ~= 1/2 × 负载电容 × 电压的平方 × 开关频率 × 晶体管数量**
        - **晶体管数量**: 制程变小, 提高主频.
            - 从1978年Intel发布的8086 CPU开始, 计算机的主频从5MHz开始, 不断提升. 1980年代中期的80386能够跑到40MHz, 1989年的486能够跑到100MHz, 直到2000年的奔腾4处理器, 主频已经到达了1.4GHz. 
            - 奔腾4的主频虽高(2.4GHz), 性能只和基于奔腾3架构的奔腾M 1.6GHz处理器差不多, 代表**“主频时代”的终结**. 
        > 软件工程师们 写程序不考虑性能, 等明年CPU性能提升一倍, 到时候性能自然就不成问题了...
        - **电压**: 
            - 从5MHz主频的 8086 到 5GHz 主频的 Intel i9, CPU的电压已经从5V左右下降到了1V左右
            - 我们CPU的主频提升了1000倍, 但是功耗只增长了40倍. 
        - **并行优化**: 堆核, 通过提升“吞吐率”而不是“响应时间”, 来达到目的
            - ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/cpu-parallel.webp)
            - **限制**
                - 需要进行额外的计算, 本身可以分解成几个可以并行的任务, 不会影响最后的结果. 
                - 需要能够分解好问题, 并确保几个人的结果能够汇总到一起. 
                - 在“汇总”这个阶段, 是没有办法并行进行的, 还是得顺序执行. 
            - **阿姆达尔定律(Amdahl’s Law)**
                - **优化后的执行时间 = 受优化影响的执行时间 / 加速倍数 + 不受影响的执行时间**
                    - 不受影响的执行时间: 如最后汇总的时间不能通过并行被优化.
- 原则: 
    - **加速大概率事件**: 整个计算过程中, 工程师们通过用GPU替代CPU, 甚至是TPU, 加速 相似重复的复杂运算.
    - **流水线**: 把CPU指令执行的过程进行拆分, 细化运行.
    - **预测**: 通过预先猜测下一步该干什么, 提前进行运算, 也是让程序跑得更快一点的办法. 
        - CPU和存储系统设计方法
            - “局部性原理”
            - “分支和冒险”




## Instruction & Operate

### Paper Tape Programing

- **打孔卡(Punched Card)编程**
- **计算机指令集(Instruction Set)**: CPU各自支持的语言
- **存储程序型计算机(Stored-program Computer)**: 程序指令存储在存储器里面的计算机
- **指令和机器码**:  

| 指令类型           | 示例指令          | 示例汇编代码      | 含义                         | 注释                                                         |
| :------------------: | :-----------------: | :-----------------: | :----------------------------: | :------------------------------------------------------------: |
| **算术类指令**     | `add`             | `add $s1, $s2, $s3` | `$s1=$s2+$s3`                | 加减乘除. 将s2和s3寄存器中的数相加后的结果放 到寄存器s1中    |
| **逻辑类指令**     | `or`              | `or $s1, $s2, $s3` | `$s1=$s2I $s3`               | 逻辑上的与或非, 将s2和s3寄存器中的数按位取或后的结 果放到寄存器s1中 |
| **数据传输指令**   | `load word`       | `load $s1, 10($s2)` | `$s1=memory[$s2+10]`      | 给变量赋值、在内存里读写数据, 取s2寄存器中的数,加上10偏移量后, 找到内存中的字,存入到s1寄存器中 |
| **条件分支指令**   | `branch on equal` | `beq $s1, $s2, 10` | `if($s1 == $s2)goto PC+4+10` | “if / else”, 如果s1和s2寄存器内的值相等,从程序 计数器往后跳10 |
| **无条件跳转指令** | `jump`            | `j 1000`          | `go to 1000`                 | 调用函数的时候, 其实就是发起了一个无条件跳转指令. 跳转到1000这个目标地址 |

- [**MIPS**](https://www.mips.com/mipsopen/)是一组由MIPS技术公司在80年代中期设计出来的CPU指令集. 目前开源. 

<table cellspacing="0" border="0">
 <tr>
        <td height="26" align="left" valign=bottom><font color="#000000"><b>指令类型</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>6位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>5位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>5位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>5位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>5位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>6位</b></font></td>
  <td align="left" valign=bottom><font  color="#000000"><b>解释</b></font></td>
 </tr>
 <tr>
  <td height="51" align="left" valign=bottom><font color="#000000">R</font></td>
  <td align="left" valign=bottom><font color="#000000">opcode</font></td>
  <td align="left" valign=bottom><font color="#000000">rs</font></td>
  <td align="left" valign=bottom><font color="#000000">rt</font></td>
  <td align="left" valign=bottom><font color="#000000">rd</font></td>
  <td align="left" valign=bottom><font  color="#000000">shamt<br>位移量</font></td>
  <td align="left" valign=bottom><font  color="#000000">funct<br>功能码</font></td>
  <td align="left" valign=bottom><font  color="#000000">算术操作、逻辑操作</font></td>
 </tr>
 <tr>
  <td height="51" align="left" valign=bottom><font color="#000000">I</font></td>
  <td align="left" valign=bottom><font color="#000000">opcode</font></td>
  <td align="left" valign=bottom><font color="#000000">rs</font></td>
  <td align="left" valign=bottom><font color="#000000">rt</font></td>
  <td colspan=3 align="left" valign=bottom><font  color="#000000">address/immediate地址/立即数</font></td>
  <td align="left" valign=bottom><font  color="#000000">数据传输、条件分支、<br>立即数操作</font></td>
 </tr>
 <tr>
  <td height="26" align="left" valign=bottom><font color="#000000">J</font></td>
  <td align="left" valign=bottom><font color="#000000">opcode</font></td>
  <td colspan=5 align="left" valign=bottom><font  color="#000000">target address目标地址</font></td>
  <td align="left" valign=bottom><font  color="#000000">无条件跳转</font></td>
 </tr>
</table>

- **R指令**: 算术和逻辑操作, 里面有读取和写入数据的寄存器的地址. 如果是逻辑位移操作, 后面还有位移操作的位移量, 而最后的功能码, 则是在前面的操作码不够的时候, 扩展操作码表示对应的具体指令的. 
- **I指令**: 数据传输、条件分支, 以及在运算的时候使用的并非变量还是常数的时候. 这个时候, 没有了位移量和操作码, 也没有了第三个寄存器, 而是把这三部分直接合并成了一个地址值或者一个常数. 
- **J指令**: 跳转指令, 高6位之外的26位都是一个跳转后的地址. 



- 以一个简单的加法算术指令`add $t0,$s1,$s2`,对应的MIPS指令里opcode是0, rs代表第一个寄存器s1的地址是17, rt代表第二个寄存器s2的地址是18, rd 代表目标的临时寄存器t0的地址, 是8. 因为不是位移操作, 所以位移量是0. 把这些数字拼在一起, 就变成了一个MIPS的加法指令. 

| 指令       | 格式 | opcode | rs    | rt    | rd    | shamt | funct  |
| ---------- | ---- | ------ | ----- | ----- | ----- | ----- | ------ |
| add        | R    | 0      | 17    | 18    | 8     | 0     | 32     |
| 二进制表示 | -    | 0      | 10001 | 10010 | 01000 | 00000 | 100000 |

- 十六进制为: `0X02324020`

- 对应纸带设计为:

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/paper-program-example.webp)



### Goto & If ... Else

指令跳转：原来if...else就是goto

- CPU是如何执行指令
    - 逻辑上, 我们可以认为, CPU其实就是由一堆寄存器组成的. 而寄存器就是CPU内部, 由多个触发器(Flip-Flop)或者锁存器(Latches)组成的简单电路. 
        - 触发器和锁存器, 其实就是两种不同原理的数字电路组成的逻辑. 
    - N个触发器或者锁存器, 就可以组成一个N位(Bit)的寄存器, 能够保存N位的数据. 比方说, 我们用的64位Intel服务器, 寄存器就是64位的. 

- **PC寄存器/指令地址寄存器( Program Counter Register / Instruction Address Register )**: 存放下一条需要执行的计算机指令的内存地址
- **指令寄存器( Instruction Register )**: 存放当前正在执行的指令. 
- **条件码寄存器( Status Register )**: 用里面的一个一个标记位(Flag), 存放CPU进行算术或者逻辑计算的结果. 
    - Goto 使用: 零标志条件码(对应的条件码是ZF, Zero Flag).
        - Intel的CPU还有
            - 进位标志(CF, Carry Flag)
            - 符号标志(SF, Sign Flag)
            - 溢出标志(OF, Overflow Flag)
    - **goto**语句: 虽然我们在用高级语言开发程序的时候反对使用goto, 但是实际在机器指令层面, 无论是if…else…也好, 还是for/while也好, 都是用和goto相同的跳转到特定指令位置的方式来实现的. 
- 其他寄存器我们通常根据存放的数据内容来给它们取名字, 比如**整数寄存器**、**浮点数寄存器**、**向量寄存器**和**地址寄存器等等**. 有些寄存器既可以存放数据, 又能存放地址, 我们就叫它通用寄存器. 
- **指令**
    - **顺序**: 一个程序的一条条指令, 在内存里面是连续保存的, 也会一条条顺序加载. 
    - **跳转**: 会修改PC寄存器里面的地址值. 这样, 下一条要执行的指令就不是从内存里面顺序加载的了. 事实上, 这些跳转指令的存在, 也是我们可以在写程序的时候, 使用if…else条件语句和while/for循环语句的原因. 

```cpp
// test.c
 #include<time.h>
 #include<stdlib.h>
 int main(){
  srand(time(NULL));
    int r = rand()% 2;
 int a = 10;
  if(r == 0){
      a = 1;
  }else{
      a = 2;
  }
}
//$ gcc -g -c temp.cpp 
//$ objdump -d -M intel -S temp.o 
```

其中 **分支语句部分**.

```cpp
 if(r == 0){
  37: 83 7d f8 00           cmp    DWORD PTR [rbp-0x8],0x0
      //DWORD PTR 表示数据类型是32位的整数
      //[rbp-0x8] 是一个寄存器的地址
      //cmp指令的比较结果, 会存入到条件码寄存器当中去
  3b: 75 09                 jne    46 <main+0x46>
      //jump if not equal, 查看对应的零标志位判断跳转 46 的位置(汇编代码行号). 
        a = 1;
  3d: c7 45 fc 01 00 00 00  mov    DWORD PTR [rbp-0x4],0x1
  44: eb 07                 jmp    4d <main+0x4d>
 }else{
        a = 2;
  46: c7 45 fc 02 00 00 00  mov    DWORD PTR [rbp-0x4],0x2 
      //PC寄存器赋值为 46 之后. CPU加载指令, 赋0x02到寄存器中, PC寄存器自增继续执行.
 }
}    
  4d: b8 00 00 00 00        mov    eax,0x0
      //eax代表累加寄存器, 表示一个占位符用于if上部分分支结束的跳转, 无实际作用
  52: c9                    leave  
  53: c3                    ret    
```



- 除了if…else的条件语句和for/while的循环之外, 大部分编程语言还有switch…case这样的条件跳转语句. switch…case编译出来的汇编代码也是这样使用jne指令进行跳转吗？对应的汇编代码的性能和写很多if…else有什么区别呢？你可以试着写一个简单的C语言程序, 编译成汇编代码看一看

### Function Call

- **Stack**
    - **由来**: 多层函数调用里简单只记录一个地址也是不够的. 因为函数一层又一层的调用并没有数量上的限制. CPU里的寄存器不能记录下所有函数调用返回的地址, 
    - 反编译代码: 

```cpp
//function_example.c
#include<stdio.h>

int static add(int a, int b){
 return a+b;
}

int main(){
    int x = 5;
 int y = 10;
 int u = add(x, y);
} 
```

其中 **函数调用部分**: 

```cpp
int static add(int a, int b){
   0: f3 0f 1e fa           endbr64
       
       //stack push start
   4: 55                    push   rbp
       //rbp:栈帧指针(Frame Pointer), 存放了当前栈帧位置的寄存器
   5: 48 89 e5              mov    rbp,rsp
       //rsp:栈指针(Stack Pointer), 将rsp的值复制到rbp里, 而rsp始终会指向栈顶(最下面)
       //rbp这个栈帧指针指向的返回地址, 变成当前最新的栈顶, 也就是add函数的返回地址
       //stack push over
       
   8: 89 7d fc              mov    DWORD PTR [rbp-0x4],edi
   b: 89 75 f8              mov    DWORD PTR [rbp-0x8],esi
 return a+b;
   e: 8b 55 fc              mov    edx,DWORD PTR [rbp-0x4]
  11: 8b 45 f8              mov    eax,DWORD PTR [rbp-0x8]
  14: 01 d0                 add    eax,edx
}
      //stack pop start
  16: 5d                    pop    rbp
      //将当前的栈顶出栈
  17: c3                    ret    
      //将程序的控制权返回到出栈后的栈顶, 即main函数的返回地址
      //stack pop over
 
      //......
      
  3c: e8 bf ff ff ff        call   0 <_ZL3addii>
  41: 89 45 fc              mov    DWORD PTR [rbp-0x4],eax
      //......
```

- **Stack Situation**: 栈顶在逐渐变小.

  ![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/stack-function-call.webp)
  
  -  **栈帧 (Stack Frame, 快照)**: 函数所占用的所有内存空间
  
- **函数内联进行性能优化**

    - 把一个实际调用的函数产生的指令, 直接插入到的位置, 来替换对应的函数调用指令. 但是如果被调用的函数里, 没有调用其他函数, 这个方法还是可以行得通的, 不会产生无穷的调用.
        - 除了依靠编译器的自动优化, 你还可以在定义函数的地方, 加上inline的关键字, 来提示编译器对函数进行内联
        - **叶子函数(或叶子过程)**: 没有调用其他函数, 只会被调用的函数
    - **优点**: CPU需要执行的指令数变少了, 根据地址跳转的过程不需要了, 压栈和出栈的过程也不用了 
    - **局限**: 如果一个函数在很多地方都被调用了, 那么就会把复用的程序指令在调用它的地方完全展开很多次, 占用的空间就会变大.

```cpp
#include<stdio.h>
#include<time.h>
#include<stdlib.h>
int static add(int a, int b){
     return a+b;
}
int main(){
     srand(time(NULL));
     int x = rand()% 5
     int y = rand()% 10;
     int u = add(x, y)
     printf("u = %d\n", u)
}
// $ gcc -g -c -O temp.cpp
// $ objdump -d -M intel -S temp.o
// 反编译获取
//     return a+b;
//  5b: 01 da                 add    edx,ebx
```





### ELF & Static Link

我们再仔细看一下objdump出来的两个文件的代码, 会发现两个程序的地址都是从0开始的. 如果地址是一样的, 程序如果需要通过call指令调用函数的话, 它怎么知道应该跳转到哪一个文件里呢？

这么说吧, 无论是这里的运行报错, 还是objdump出来的汇编代码里面的重复地址, 都是因为 add_lib.o 以及 link_example.o并不是一个 可执行文件 (Executable Program), 而是 目标文件 (Object File). 只有通过链接器(Linker)把多个目标文件以及调用的各种函数库链接起来, 我们才能得到一个可执行文件. 

我们通过gcc的-o参数, 可以生成对应的可执行文件, 对应执行之后, 就可以得到这个简单的加法调用函数的结果. 

- 在Linux下, 可执行文件和目标文件所使用的都是一种叫 ELF (Execuatable and Linkable File Format)的文件格式, 中文名字叫 **可执行与可链接文件格式** , 不仅存放了编译成的汇编指令, 还保留了很多别的数据. 
    - **符号表 (Symbols Table)**: 函数/变量 名称和它们对应的地址. 符号表相当于一个地址簿, 把名字和地址关联了起来. 
    - **文件头(File Header)**: 把各种信息, 分成一个一个的Section保存起来. 表示这个文件的基本属性比如是否是可执行文件, 对应的CPU、操作系统等等. 除了这些基本属性之外, 大部分程序还有这么一些Section：
        - `.text Section`: 代码段或者指令段(Code Section), 用来保存程序的代码和指令；
        - `.data Section`: 数据段(Data Section), 用来保存程序里面设置好的初始化数据信息；
        - `.rel.text Secion`: 重定位表(Relocation Table). 重定位表里, 保留的是当前的文件里面, 哪些跳转地址其实是我们不知道的. 比如上面的 link_example.o 里面, 我们在main函数里面调用了add 和 printf 这两个函数, 但是在链接发生之前, 我们并不知道该跳转到哪里, 这些信息就会存储在重定位表里；
        - `.symtab Section`: 符号表(Symbol Table). 符号表保留了我们所说的当前文件里面定义的函数名称和对应地址的地址簿
- **过程**: 链接器会扫描所有输入的目标文件, 然后把所有符号表里的信息收集起来, 构成一个全局的符号表. 然后再根据重定位表, 把所有不确定要跳转地址的代码, 根据符号表里面存储的地址, 进行一次修正. 最后, 把所有的目标文件的对应段进行一次合并, 变成了最终的可执行代码. 在链接器把程序变成可执行文件之后, 要装载器去执行程序就容易多了. 装载器不再需要考虑地址跳转的问题, 只需要解析 ELF 文件, 把对应的指令和数据, 加载到内存里面供CPU执行就可以了. 
- Windows的可执行文件格式是一种叫作 PE (Portable Executable Format)的文件格式. Linux下的装载器只能解析ELF格式而不能解析PE格式. 

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/co-software-run.webp)

### 640K Memory Enough?

> 640K ought to be enough for anyone. --Bill Gates

- **程序装载挑战**
    - **装载条件**
        - 可执行程序加载后占用的内存空间应该是连续的
        - 我们需要同时加载很多个程序, 并且不能让程序自己规定在内存中加载的位置
    - **办法**: 维护一个虚拟内存到物理内存的映射表, 这样实际程序指令执行的时候, 会通过虚拟内存地址, 找到对应的物理内存地址, 然后执行. 因为是连续的内存地址空间, 所以我们只需要维护映射关系的起始地址和对应的空间大小就可以了. 
        - **虚拟内存地址(Virtual Memory Address)**: 指令里用到的内存地址
        - **物理内存地址(Physical Memory Address)**: 实际在内存硬件里面的空间地址
-  **内存分段**  
    - **分段(Segmentation)**: 找出一段连续的物理内存和虚拟内存地址进行映射的方法
    - **局限**
        - **内存碎片 (Memory Fragmentation)**
            - **内存交换 (Memory Swapping)**: 不连续内存无法加载程序, 因为硬盘和内存速度差异, 可能造成机器卡顿    
- **内存分页**
    - **分页(Paging)**: 当需要进行内存交换的时候, 让需要交换写入或者从磁盘装载的数据更少一点
        - 分页是把整个物理内存空间切成一段段固定尺寸的大小
            - **页(Page):** 这样一个连续并且尺寸固定的内存空间
            - 在Linux下, 我们通常只设置成4KB. 
                - ```shell
                    $ getconf PAGE_SIZE
                    ```
        - 分页的方式使得我们在加载程序的时候, 不再需要一次性都把程序加载到物理内存中. 
            - 当要读取特定的页, 却发现数据并没有加载到物理内存里的时候, 就会触发一个来自于CPU的 缺页错误 (Page Fault). 我们的操作系统会捕捉到这个错误, 然后将对应的页, 从存放在硬盘上的虚拟内存里读取出来, 加载到物理内存里. 这种方式, 使得我们可以运行那些远大于我们实际物理内存的程序. 同时, 这样一来, 任何程序都不需要一次性加载完所有指令和数据, 只需要加载当前需要用到就行了

> 这些技术和方法, 对于我们程序的编写、编译和链接过程都是透明的. 这也是我们在计算机的软硬件开发中常用的一种方法, 就是 加入一个 间接层



### Dynomtic Link

- **动态链接(Dynamic Link)** 
    - 对象: 加载到内存中的 共享库(Shared Libraries). 
        - Windows下, `.dll`(Dynamic-Link Libary, DLL, 动态链接库). 
        - Linux下, 这些共享库文件就是.so文件, 也就是Shared Object(一般我们也称之为动态链接库)
- **静态链接 (Static Link)**
    - 相对地址
- **PLT & GOT**
- `Continued To Be...`



### Binary Encode

- **字符集**: 字符的一个集合
  - 第一版《新华字典》里面出现的所有汉字, 这是一个字符集
  - Unicode: 一个包含了150种语言的14万个不同的字符集. 
- **字符编码**: 对字符集用二进制表示. 
  - Unicode可以用UTF-8、UTF-16, 乃至UTF-32来进行编码成二进制 
- “锟斤拷”
  - 如果我们想要用Unicode编码记录一些文本, 特别是一些遗留的老字符集内的文本, 但是这些字符在Unicode中可能并不存在. 于是, Unicode会统一把这些字符记录为U+FFFD这个编码.
  - 如果用UTF-8的格式存储下来, 就是\xef\xbf\xbd. 如果连续两个这样的字符放在一起, \xef\xbf\xbd\xef\xbf\xbd, 这个时候, 如果程序把这个字符, 用GB2312的方式进行decode, 就会变成“锟斤拷”. 
- “烫烫烫”
  - 如果调试器默认使用MBCS字符集. “烫”在里面是由0xCCCC来表示的
  - 0xCC又恰好是未初始化的内存的赋值. 

### 电路

- 继电器

### 加法器

### 乘法器

### 浮点数

## Processor

### CPU

- 指令周期(Instruction Cycle)
    - **Fetch(取指)**: 从PC寄存器里找到对应的指令地址再从内存里把具体的指令加载到指令寄存器中, 后把PC寄存器自增
      - 控制器 (Control Unit) 控制寻址
    - **Decode(指令译码)**: 将指令寄存器里面的指令解析成操作, 是R,I,J中的哪一种指令, 具体要操作哪些寄存器、数据或者内存地址
      - 控制器 (Control Unit) 控制解码
    - **Execute(执行指令)**: 也就是实际运行对应的R,I,J这些特定的指令, 进行算术逻辑操作、数据传输或者直接的地址跳转
      - 算术逻辑单元(ALU): 
        - 算术操作、逻辑操作的R型指令
        - 数据传输、条件分支的I型指令
      - 控制器: 一个简单的无条件地址跳转
      - ALU计算(指令执行) -> 内存访问 -> 数据写回 
- **数据通路**
    - **操作元件/组合逻辑元件(Combinational Element)**, ALU. 在特定的输入下, 根据下面的组合电路的逻辑, 生成特定的输出. 
    - **存储元件/状态元件(State Element)**, 如寄存器, 无论是通用寄存器还是状态寄存器, 其实都是存储元件. 
- **桥梁**: 数据总线  
- **控制器**
    - 一方面, 所有CPU支持的指令, 都会在控制器里面, 被解析成不同的输出信号. 我们之前说过, 现在的Intel CPU支持2000个以上的指令. 这意味着, 控制器输出的控制信号, 至少有2000种不同的组合. 
- **硬件电路**
    - 组合逻辑电路(Combinational Logic Circuit): ALU 
    - 时序逻辑电路 (Sequential Logic Circuit)
        - 好处
            - **自动运行**: 时序电路接通之后可以不停地开启和关闭开关, 进入一个自动运行的状态. 这个使得我们上一讲说的, 控制器不停地让PC寄存器自增读取下一条指令成为可能. 
            - **存储**: 通过时序电路实现的触发器, 能把计算结果存储在特定的电路里面, 而不是像组合逻辑电路那样, 一旦输入有任何改变, 对应的输出也会改变. 
            - **时序协调**: 无论是程序实现的软件指令, 还是到硬件层面, 各种指令的操作都有先后的顺序要求. 时序电路使得不同的事件按照时间顺序发生. 
    - 存储数据的触发器/锁寸其电路: Latch / Data/Delay Flip-flop
    - 计数器电路: pc寄存器 自加
    - 译码器电路
- 时钟信号 (Clock Signal): 下图将开关A的打开就可以产生01信号.

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/clock-signal-circuit.webp)

- 反馈电路 (Feedback Circuit): 把电路的输出信号作为输入信号, 再回到当前电路的电路构造方式
- D触发器实现存储

......

### Pipeline 流水线设计

- **周期分类**:
  - 指令周期
  - 机器周期/CPU周期
  - 时钟周期(主频倒数)

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/cycle-vs.webp)

- 指令数×CPI×时钟周期
- **单指令周期处理器(Single Cycle Processor)**: 在一个时钟周期内(时间固定), 处理器正好能处理一条指令(时间相关于门延迟,位数,复杂度)
  - **局限性**: 局限于执行时间最长的指令上
  - CPI: 1
- **指令流水线(Instruction Pipeline)**: 拆分成小步骤需要的时间, 而不是以等待的整个指令执行完成才能执行下一跳指令
  - 一个CPU时钟周期, 可以认为是完成一条简单指令的时间
  - **步骤**: 虽然执行一条指令的时钟周期变成了5, 但是我们可以把CPU的主频提得更高了, 取指令（IF）-指令译码（ID）-指令执行（EX）-内存访问（MEM）-数据写回（WB） 
  - **提升**: 只要保障一个最复杂的流水线级的操作, 在一个时钟周期内完成就好了 
    - 不需要确保最复杂的那条指令在时钟周期里面执行完成
  - **好处**: CPU “吞吐率” 提升
  - **性能成本**: 流水线带来的多一级写入到流水线寄存器的操作上(overhead)
- **Pentium 4 VS Athlon**
  - Pentium 4: 
    - NetBurst架构
    - 20级流水线(2000年)
    - 2004年, 代号Prescott流水线31级
    - 功耗问题
  - Athlon:
    - K7架构
    - 因为一个Pipeline Stage, 就需要一个时钟周期在这种情况下, 31个Stage的3GHz主频的CPU, 其实和11个Stage的1GHz主频的CPU, 性能是差不多的

```
int a = 10 + 5; //指令 1
int b = a * 2; //指令 2
float c = b * 1.0f; //指令 3
//abc 相互依赖
```

- 冒险(Hazard): 结构间的依赖问题
  - 数据冒险、结构冒险、控制冒险 结构冒险、控制冒险 等其他的依赖问题. 
  - 解决方案: 流水线越长越难解决
    - 乱序执行: 把后面没有依赖关系的指令放到前面来执行
    - 分支预测
- SPEC, IPC(Instruction Per Cycle)来衡量CPU执行指令的效率
  - SPEC
  - IPC: CPI(Cycle Per Instruction)的倒数

问题:

> 这一讲, 我们说CPU好像一个永不停歇的机器, 一直在不停地读取下一条指令去运行. 那为什么CPU还会有满载运行和Idle闲置的状态呢？请你自己搜索研究一下这是为什么, 并在留言区写下你的思考和答案. 

CPU 还会有满载运行和 Idle 闲置的状态, 指的系统层面的状态. 即使是idle空闲状态, cpu也在执行循环指令

> 现在我们的CPU主频非常高了, 通常在几GHz了, 但是实际上我们的晶振并不能提供这么高的频率, 而是通过“外频+倍频“的方式来实现高频率的时钟信号. 请你研究一下, 倍频和分频的信号是通过什么样的电路实现的？


> 一个CPU的时钟周期, 可以认为是完成一条简单指令的时间. 在这一讲之后, 你觉得这句话正确吗？为什么？在了解了CPU的流水线设计之后, 你是怎么理解这句话的呢？

> 你能找找我们在程序的执行过程中, 其他的依赖情况么？这些依赖情况又属于我们说的哪一种冒险呢？

### harzard 冒险和预测

https://zh.coursera.org/lecture/comparch/structural-hazard-lB2xV

- 冒险: 资源冲突, 如键盘锁键(薄膜键盘并非都有独立线路)
  - 分类:
    - 结构冒险(Structural Harzard)
      - 哈佛架构([Harvard Architecture](https://en.wikipedia.org/wiki/Harvard_architecture))
        - 哈佛大学设计 [Mark I 型计算机](https://en.wikipedia.org/wiki/Harvard_Mark_I)
      - 混合架构(Hybrid Architeture): 在CPU内部的高速缓存部分进行了区分
        - 指令缓存(Instruction Cache) 
        - 数据缓存(Data Cache)
    - 数据冒险(Data Harzard)
      - 数据依赖分类
        - 先写后读(Read After Write, RAW): 数据依赖(Data Dependency)
        - 先读后写(Write After Read, WAR): 反依赖(Anti-Dependency)
        - 写后再写(Write After Write, WAW): 输出依赖(Output Dependency)
      - 流水线停顿(Pipeline Stall) / 流水线冒泡（Pipeline Bubbling)
        - 插入一个NOP操作: 不仅要在当前指令里面，所有后续指令也要插入???
    - 控制冒险(Control Harzard)
- 操作数前推(Operand Forwarding)/操作数旁路(OperandBypassing)

......
- hazard是“危”也是“机”
- CPU里的“线程池”
- 今天下雨了, 明天还会下雨么？

### Superscalar和VLIW：如何让CPU的吞吐率(IPC,（Instruction Per Clock)超过1？

- 程序的CPU执行时间 = 指令数 × CPI × Clock Cycle Time
- 最佳情况下，IPC也只能到1。因为无论做了哪些流水线层面的优化，即使做到了指令执行层面的乱序执行，CPU仍然只能在一个时钟周期里面，取一条指令
实际上，

整数和浮点数计算的电路，在CPU层面也是分开的。
- 80386: 387芯片, 专门的浮点数计算的电路
  - 386sx和386dx这两种芯片可以选择。386dx就是带了387浮点数计算芯片的，而sx就是不带浮点数计算芯片的。
  - 我们会有多个ALU。这也是为什么，在 第24讲 讲乱序执行的时候，你会看到，其实指令的执行阶段，是由很多个功能单元（FU）并（Parallel）进行的

为什么取指令和指令译码不行呢？

- 多发射 （Mulitple Issue）和 超标量 （Superscalar）
  - 动态多发射处理器
    - 依赖关系的检测
  - 通过增加硬件的,一次性从内存里取出多条指令，然后分发给多个并行的指令译码器，进行译码，然后对应交给不同的功能单元去处理。
  - 指令执行 / 取指令 / 指令译码: 并行
- 安腾(Itanium):18年退出市场.
  - 超长指令字设(VLIW): 编译器来优化指令数\CPI
  - 显式并发指令运算(Explicitly Parallel Instruction Computer)
  - “向前兼容”
    - 安腾处理器的指令集和x86是不同的。
    - 增加一个指令包里包含的指令数量, 要重新编译(交换指令顺序 + NOP, 编译器)

> 在超长指令字架构的CPU里面，我之前给你讲到的各种应对流水线冒险的方案还是有效的么？操作数前推、乱序执行，分支预测能用在这样的体系架构下么？安腾CPU里面是否有用到这些相关策略呢？

### SIMD：加速矩阵乘法

- 解决“冒险”、提升并发的方案，本质上都是一种 指令级并行(Instruction-level parallelism, IPL)的技术方案
- **超线程 （Hyper-Threading）/同时多线程 （Simultaneous Multi-Threading, SMT）技术**: 把一个物理层面CPU核心，“伪装”成两个逻辑层面的CPU核心, 硬件层面增加电路(通常只在CPU核心的添加10%左右的逻辑功能), 使得我们可以在一个CPU核心内部，维护两个不同线程的指令的状态信息
  - 同一时间点上，一个CPU核心只会运行一个线程的指令，所以其实没有真正的指令并行运行
  - **目的**: 在一个线程A的指令，在流水线里停顿的时候，让另外一个线程去执行指令。因为这个时候，CPU的译码器和ALU就空出来了，那么另外一个线程B，就可以拿来干自己需要的事情。这个线程B可没有对于线程A里面指令的关联和依赖。
  - **局限**: 只在特定的应用场景下效果比较好。一般是在那些各个线程“等待”时间比较长的应用场景下。比如，我们需要应对很多请求的数据库应用，就很适合使用超线程。各个指令都要等待访问内存数据，但是并不需要做太多计算
  - 4核心8线程: 物理4核, 逻辑8核心
- 单指令多数据流(SIMD, Single Instruction Multiple Data): 在Intel发布Pentium处理器的时候, 被引入的指令集MMX(Matrix Math eXtensions, 矩阵数学扩展)
  - 多指令多数据(MIMD, Multiple Instruction Multiple Data)
  - Instructions: CPU所支持的指令集
    - Python 中 NumPy 直接用到了SIMD指令，能够并行进行向量的操作
  - 获取数据和执行指令的时候，都做到了并行
    - 在从内存里面读取数据的时候，SIMD是一次性读取多个数据
  - 对象: 在计算层面存在大量“数据并行”（Data Parallelism）的计算, 向量运算/矩阵运算
  - 用处: 过去进行图片、视频、音频的处理, 近年常在进行机器学习算法的计算
    - CPU第一次有能力进行多媒体处理。这也正是拜SIMD和MMX所赐

> 超线程这样的技术，在什么样的应用场景下最高效？你在自己开发系统的过程中，是否遇到超线程技术为程序带来性能提升的情况呢？

......

异常和中断：程序出错了怎么办？
CISC和RISC：为什么手机芯片都是ARM？
GPU(上)：为什么玩游戏需要使用GPU？
GPU(下)：为什么深度学习需要使用GPU？
FPGA和ASIC：计算机体系结构的黄金时代
解读TPU：设计和拆解一块ASIC芯片
理解虚拟机：你在云上拿到的计算机是什么样的？

## 原理篇：存储与I/O系统(17讲)

存储器层次结构全景：数据存储的大金字塔长什么样？
局部性原理：数据库性能跟不上, 加个缓存就好了？
高速缓存(上)：“4毫秒”究竟值多少钱？
高速缓存(下)：你确定你的数据更新了么？
MESI协议：如何让多核CPU的高速缓存保持一致？
理解内存(上)：虚拟内存和内存保护是什么？
理解内存(下)：解析TLB和内存保护
总线：计算机内部的高速公路
输入输出设备：我们并不是只能用灯泡显示“0”和“1”
理解IO_WAIT：I/O性能到底是怎么回事儿？
机械硬盘：Google早期用过的“黑科技”
SSD硬盘(上)：如何完成性能优化的KPI？
SSD硬盘(下)：如何完成性能优化的KPI？
DMA：为什么Kafka这么快？
数据完整性(上)：硬件坏了怎么办？
数据完整性(下)：如何还原犯罪现场？
分布式计算：如果所有人的大脑都联网会怎样？

## 应用篇

- 大型DMP系统
  - MongoDB并不是什么灵丹妙药
  - SSD拯救了所有的DBA
- Disruptor
  - CPU高速缓存的风驰电掣
  - 不需要换挡和踩刹车的CPU, 有多快？

答疑与加餐(5讲)


![](https://z3.ax1x.com/2021/06/28/RNt0kn.png)

<div id="j1">[1]. https://en.wikipedia.org/wiki/First_Draft_of_a_Report_on_the_EDVAC#Synopsis </div>