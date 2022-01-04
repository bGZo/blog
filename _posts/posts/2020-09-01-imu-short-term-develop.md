---
layout: post
title: IMU Short Term Develop
updated: 2020-09-01
category: posts
---

该怎么去面对自己在一个月的时间里没有好好写好 "学生选课系统" 这一个简单的 `Cpp` 程序, 这篇文章鸽了很久, 我多少希望自己逃避这个对我造成不小阴影的时间段, 我不知道那些跟着联盟导师团伙做项目的同学增长了多少知识, 但我在一个月的时间里缺乏真的效率很低, 多次心态接近低到零点爆炸, 甚至开始怀疑自己是不是真的适合这门学科. 说多了也只是为自己的低能找借口开脱, 我总结以下几个方面, 附带一些槽点, 诚恳总结如下:

- 总结:
  - 前期进度开发出现问题时, 一定要即时和其他成员进行反馈, **不可以拖延**, 像现在的工作岗位一样, 工作时间拖延, 那就占用你的成长时间来弥补.
  - 代码**预处理**太多造成冗余项过多, 难以维护, 以及**整体逻辑结构**必须在实施前去实现一下, 这样可以在码字的时候为以后做更多的打算. 实际开发中走一步看一步造成了不断地修改重复代码及标记变量, 而后再去维护更多的函数, 维护再度提升一个量级. 写代码的时候必须**警惕过多的预处理**, 一定有更好的方式.
  - **尽量用更省力的库**, 不要重复造不必要的轮子. 在实际开发中, 我曾避免使用可托容的 `vector`, 而用双数组来代替之, 复杂度提升一个量级, 何苦呢?
  - 做好最坏的打算, 不要想着在一个染缸里摸鱼. 实际开发中因为太卷, 大家走一步看一步, 前期不必要的要求到后期都成为了必要项. 这样子强制让人一起绕着卷王加班的情景真是和现 996 如出一辙.

<!--more-->

写代码, 后有些想法. 一为作业, 二来是为了记录.

##  1. <a name=''></a>功能概述

###  1.1. <a name='-1'></a>信息存储

**[效果/方式] :**  在系统开始时候, 进行信息的初始化, 包括学生信息, 老师信息, 班级信息, 课程信息的读入和写入. 而在退出系统的时候进行四个文件的全部写入. 

```cpp
#include<fstream>
int SystemInit(){
    ifstream infile;
    infile.open("./data/CourseInfo.in"); //初始化课程信息
    for(int i=0;i<Cnum;i++) 
        infile>>course[i];
    infile.close();
}        
```

###  1.2. <a name='-1'></a>登录/注册 功能

**[效果] :** 开头先进行注册或者登录, 注册成功后即可登录; 四部分代码全部具有初始密码, 具体为学生初始为"1", 老师为"2".如果是初次登录. 可以使用初始密码或者预设密码进行登录, 而再次登录则预设密码失效.

**[方式]** : 通过单个`int`变量计数器来判断该用户是不是初次登录.

```cpp
void Judge(){
...
    if(nowUsr==1){//学生
		nowStu=SuSearchStID(account);
		if(nowStu==-1)
			nowStu=SuSearchStName(account);
		if(nowStu==-1){
			cout<<"[Error] 没有找到你输入的账户，请检查输入后再进行登录\n";
			continue; 
		}
		StInitPassW="1";
		if(!StuInit && password==StInitPassW)flag=1;
		if(StuInit && password==StuAcc[nowStu].PassW)flag=1;
    }
    if(flag){
    	cout<<"恭喜你, 登录成功"<<endl;
    	PAUSE();
        return true;
     } 
}
```

###  1.3. <a name='-1'></a>初始化学生信息

**[效果]** : 学生名字初始化为"DFS100","DFS101","DFS102"......; 学号信息对应初始化为"100", "101", "102"等效果.

**[方式]** : 采用了 `sstring`里面的`stringstream`来进行学生信息(学号)的初始化, 相关代码如下:

```cpp
#include<sstream>
St::Student(){
    string Temp;
    stringstream ss;
    ss<<StInitTemp;
    Temp=ss.str();
    ID=Temp;
    StInitTemp++;
    Name="DFS"+Temp;
}
```

###  1.4. <a name='-1'></a>学生管理课程

####  1.4.1. <a name='-1'></a>选课

**[效果]** : 学生选择对应序号的课程.

**[方式]** : 在学生类中的 标记位数组 赋值为1, 表示这个位置的课程已经被学生选定. 如果之前没有选择这门课程, 选定课程的数量加1.

```cpp
void ChooseCourse(int a){//进行已有的课程的选择
    int num, flag;//flag查询课程下的学生是否选了这个课程
    char order;
    cin>>num;
    ...
    num=SearchRealCourseNum(num);//对序号进行再处理获得正确的数组下标
    if(!(StuAcc[a].course[num-1]))StuAcc[a].CCourse++;
    StuAcc[a].course[num-1]++;
    if(StuAcc[a].course[num-1]==2)
        cout<<"[Tip]: 你已经选择过该课程,请核对后再次选择!\n";
	...
}
```



####  1.4.2. <a name='-1'></a>退选/更换 课程

**[效果]** : 学生按序号退掉或者更换自己的课程.

**[方式]** : 在学生类中的 标记位数组 赋值为0, 表示这个位置的课程已经被学生删除, 如果之前确实选择过这门课程, 选定课程数量减1.如果是更换课程, 需要再选择一门课程, 并且选定课程数不变.

```cpp
void ChangeStCourse(int a){//换课
    int order, insteadnum, flag;
    char corder;
    SearchCourse(a);
    cout<<"请输入你想换的课程序号:\n";
    cin>>order;
    ...
    cout<<"输入你要选择的课程(取消请按-1):\n"; 
    cin>>insteadnum;
    ...
    insteadnum--;
    insteadnum=SearchRealCourseNum(insteadnum);
    StuAcc[a].course[flag]=0;
	StuAcc[a].course[insteadnum]++;
	...
    return;
}

void DeleteCCourse(int a){//根据学生数组打印学生课程; 拿课程去查学生, 选课的时候存上编号.
    int order,flag;
    char corder;
    cin>>order;
    ...
    order--;
    order=SearchRealCourseNum(order);
    if(StuAcc[a].course[order]) StuAcc[a].CCourse--;
    StuAcc[a].course[order]=0;
    ChangeCourseStu(a,order);
    ...
}
```

###  1.5. <a name='-1'></a>老师管理课程

####  1.5.1. <a name='-1'></a>加课

**[效果]** : 输入加入的课程, 如果已经存在就重新输入, 如果不存在就加入成功.

**[方式]** : 如果课程不存在在原来的数组中, 容错数组标记向后位移一位.存在则重新输入.

```cpp
void SuAddGrade(){//增加班级及选课情况
    cout<<"请输入想要增加的班级:\n";
    cin>>ErrGradecourse[AddGrade];
    if(IsGradeEx(ErrGradecourse[AddGrade])==-1){
        AddGrade++;
        cout<<"增加班级成功!";
    }
    else {
        cout<<"添加失败, 即将退出\n";
    }
}
```

####  1.5.2. <a name='-1'></a>删课

**[效果]** :  输入删除课程的序号, 如果输入合法则删除, 否则重新输入.

**[方式]** : 在课程的标记数组中赋值对应位置的值为1, 表示课程已经被销毁.

```cpp
void SuDelGrade(){//删除班级
    int step;
    SuShowGradeInfo();
    cout<<"请输入想要删除班级的序号\n";
    cin>>step;
    step--;
    step=FoundRealGrade(step);
    ...
    SuShowGradeInfo();
    cin>>step;
    step--;
    step=FoundRealGrade(step);
    SuMoveStGrade(step);
    GradeErr[step]=1;//标记班级已经删除
    cout<<"删除班级成功\n";
}
```



###  1.6. <a name='-1'></a>老师管理班级

####  1.6.1. <a name='-1'></a>增加班级

**[效果]** : 输入增加课程的序号, 如果输入合法则增加, 否则重新输入.

**[方式]** : 原数组标记结束位置后移一位, 写入课程, 不合法就继续

####  1.6.2. <a name='-1'></a>删除班级

**[效果]** : 输入删除班级的序号, 如果输入合法则删除, 否则重新输入.

**[方式]** : 

###  1.7. <a name='-1'></a>老师查看所有课程下的学生

**[效果]** : 查看所有课程下选择该课程的学生

**[方式]** : 因为第一种方式耦合读较高, 代码维护量成倍上升, 所以采用第二种方式.

+ 通过预处理在学生选择的时候就将下标存入一个二维数组, 后期访问二维数组即可, **复杂度O(n)**(n表示学生的选课操作, 基本等同于学生的数量)
+ 通过遍历打印课程, 再在学生中遍历查找是否选择了该课程, **遍历查找可以用位数组降低复杂度到O(1)**, 所以整体的**复杂度是O(n\*n)=O(n^2^)**

```cpp
void SuShowCourseAStudent(){//课程列表以及学生的信息
    int step=1;
    for(int i =0;i<Cnum;i++){
        if(SuDeleteCourse[i])
            continue;//课程已删除，返回主函数, 继续下一个
        cout<<"["<<step++<<"]"<<'\t'<<course[i]<<'\t';
        for(int j=0;j<CourseStuSum[i][0];j++){
            if(CourseStuSum[i][j+1]!=-1) //或者改成j<=以及j=1
                cout<<StuAcc[CourseStuSum[i][j+1]].name<<' ';
        }
        cout<<endl;
    }
    if(!Flag_ErrCourse) return;
    for(int j=0;j<Flag_ErrCourse;j++){
        cout<<"["<<step++<<"]"<<'\t'<<ErrCourse[j]<<'\t';
        for(int k=1;k<=CourseStuSum[j+Cnum][0];k++){
            if(CourseStuSum[j+Cnum][k]!=-1)
                cout<<StuAcc[CourseStuSum[Cnum+j][k]].name<<' ';
        }
        cout<<endl;
    }
}
```



###  1.8. <a name='-1'></a>老师查看所有的学生的选课信息

**[效果]** : 查看所有用户的个人资料和选课信息.

**[方式]** : 重用学生查询自己选课信息的函数.

```cpp
void SuShowAllStINfo(){ //展示所有学生的选课信息
    cout<<"名字\t"<<"学号\t"<<"班级\t"<<"选课数量\t"<<"选择的课程\n";
    for(int i=0;i<Studentnum;i++){
        cout<<StuAcc[i].name<<'\t'<<StuAcc[i].ID<<'\t'<<StuAcc[i].Grade<<'\t'<<StuAcc[i].CCourse<<'\t'<<'\t';
        for(int j=0 ;j<Cnum+Flag_ErrCourse;j++)
            if(StuAcc[i].course[j] && !SuDeleteCourse[j]){
                if(j<Cnum)
                    cout<<course[j]<<'\t';
                if(j>Cnum)
                    cout<<ErrCourse[j-Cnum]<<'\t';
            }
        cout<<endl;
    }
}
```



###  1.9. <a name='-1'></a>老师查询学生信息

**[效果]** : 根据学号或者姓名对学生进行查找, 因为学生有查重机制, 所以保证每一个学生的唯一性, 查找到后可以对学生进行学生本人的操作.

**[方式]** : 遍历学生的名字和学号, 直到找到该学生的位置为止, 然后可以和学生代码共用, 可以简化教师的封装复杂度, 高效利用重复代码.

```cpp
void SuSearchManStCourse(){//查询指定学生选课情况
    ...
    while(key){
        cout<< "查询到的学生是"<<StuAcc[flag].name<< "他的选课情况如下:\n";
        SearchCourse(flag);
        do{
            cout<<endl<<"请选择现在的操作:\n";
            PrintManStu();
            cin>>order;
            system("reset");
            if(order<-1||order>5)cout<<"请输入有效的命令以进行下一步操作\n";
        }while(order<-1||order>5);
        system("reset");
        if(order==-1) return;
        if(order==1) DeleteCCourse(flag);//删除选课信息
        if(order==2) SearchCourse(flag);//展示选课信息
        if(order==3) SwapCourse(flag);//更换课程信息
        if(order==4) ChangeSelfInfo(flag);//改变自己的资料
        if(order==5) SuChangeGradeInfo(flag);//管理员改变学生资料
    }
}
```



##  2. <a name='-1'></a>心得体会

###  2.1. <a name='-1'></a>预处理

- **[弊端]** : 受学习算法思维的影响, 在用数组设计代码的时候习惯引入了大量的预处理数组. 但是在后期维护功能时, 发现书写复杂度成倍增长, 在预处理数组在面对新需求整改的时候, 维护量基本上升到了整篇代码的量. 牵一发而动全身, 耦合度大, 维护起来笨重且容易忘记部分功能, 耗时久但效率极低. 所以在数组预处理上应该避重就轻.没有一劳永逸的预处理. 对于常用的预处理更是如此.
  
    ```cpp
    int CourseStuSum[Cnum+ErrCnum][Nnum];//记录课程下的学生序号
    int SuDeleteCourse[Cnum+ErrCnum];//老师要删除的课程序号
    int Flag_ErrCourse;//增加的课程
    char ErrGradecourse[Gradenum][GNamenum];//增加班级的信息
int GradeErr[Gradenum+Gradenum];//班级是否被删除
    int AddGrade;//增加班级的数量
    ```
    
- **[好处]** : 简化查找对应课程下的学生的代码复杂度, 在查找量巨大的时候可以减少查找的量. 降低时间和空间复杂度.
  
- 引入了宏定义来预处理输出化数组的大小, 如处理课程数量, 课名长度, 班级数量, 班级名字长度, 学生数量, 老师数量, 容错课程数量, 容错课名长度. 这些初始写代码不知道且需要快速确定的常量, 可以采用宏定义的方式快速确定下来, 在未来修改可以更容易修改.经过资料查找, 这个是C语言的典型处理方式, 而对于常量, 可以取而代之的C++做法是: `const int Cnum=5;`
  
    ```cpp
    #define Cnum 5 //课程数量
    #define Nnum 20 // 课名长度
    #define Gradenum 2 //班级数量
    #define GNamenum 20 //班级名字长度
    #define Studentnum 1 //学生数量
    #define Teachernum 1 //老师数量
    #define ErrCnum 5 //容错课程数量
    #define ErrNnum 20 //容错课名长度
    #define PAUSE() system("read -p '-->按任意键结束<--' var")//暂停函数
    ```
###  2.2. <a name='-1'></a>功能切离

虽然在写代码的初期进行了一部分的功能切离, 但是在区分必要打印信息和不必要打印信息上还存在差距.

自己总结出来的一些规律是:

+ 把核心逻辑代码变为函数放在外部; 其中重要的是, 对于被管理(权限比较低) 的用户, 应该尽量把权限变为 Public , 即放在全局环境中. 好处是可以供管理员(权限高) 重复调用, 提高代码的可重读性, 如:

    ```cpp
    # 面向过程中
    # 此函数常常显示课程信息, 所以经常被调用, 写成核心代码的形式可以重复调用.
    void ShowCourse(){ // 展示现在存有的课程
        int jnum, step=1;
        for(jnum=0; jnum<Cnum; jnum++){
            if(!SuDeleteCourse[jnum])
                cout<<"["<<step++<<"]\t"<<course[jnum]<<'\n';
        }
        if(!Flag_ErrCourse) return;
        for(int i=0;i<Flag_ErrCourse;i++){
            if(!SuDeleteCourse[jnum+i])
                cout<<"["<<step++<<"]\t"<<ErrCourse[i];
            cout<<'\n';
        }
    }
    
    # 类与对象中
    # 简单的打印课程函数, 检查标记数组封装在类中, 所以显得更加简洁干净.
    # 检查当course[i].GetCheckSelect()为1, 代表选中; 检查当::course[i].GetSuDelete()为0,表示没有被删除
    void St::SimpleSCourse(){
        string temp;
        for(int i=0 ;i<Cnum+Flag_ErrCourse;i++) 
            if(course[i].GetCheckSelect() && (!(::course[i].GetSuDelete())))
    			cout<< (::course[i].GetName()) <<'\t';
    }
    ```



###  2.3. <a name='-1'></a>数组利用位模式优化时间复杂度

**[方法]** : 在写 [选课, 课程预处理] 以及 [删除课程或者班级] 的时候使用同 [存储数组] 大小的标记数组 来标记课程的被选和删除情况, 如果对应位置的标记不为0 的时候就表示该位置的课程被选或者删除, 利用**数组下标的特殊性**可以进行**对应课程/班级/情况的记录**. 如:

```cpp
char course[Cnum][Nnum];//记录课程的名字和数量
char ErrCourse[ErrCnum][ErrNnum];//可以增加的课程即数量
int SuDeleteCourse[Cnum+ErrCnum];//老师要删除的课程序号
```



###  2.4. <a name='-1'></a>类与对象的高效和易维护

深刻体会了类与对象书写代码的方式处理了**程序功能的分离和归属**的特点. 尤其在增设了 班级(Grade) 和 课程(Course) 后, **无论是从逻辑上而言, 还是代码书写上, 不需要再考虑担心是否遗漏某部分功能**, 因为所有的功能全部封装在一个大类中, 结合注释的查找可以让书写的逻辑思路更加清晰, 而不是像结构体那样滑动半个屏幕找寻之前的定义而一头雾水的感觉. 以学生类型为例: 

```cpp
#面向过程, 查找函数与对应存储单元(数组)
//Student Operation, Show, Search , Delete
void ShowCourse();
int SearchRealCourseNum(int);
void ChangeCourseStu(int,int);
int TextStCourse(int,int);
void ChooseCourse(int);
...
char course[Cnum][Nnum];//记录课程的名字和数量
char ErrCourse[ErrCnum][ErrNnum];//可以增加的课程即数量
int CourseStuSum[Cnum+ErrCnum][Nnum];//记录课程下的学生序号
int SuDeleteCourse[Cnum+ErrCnum];//老师要删除的课程序号
int Flag_ErrCourse;//增加的课

# 类与对象
typedef class Student{//选择的指针占位符号, 选择存储的位置
private:
    string Name;//名字
    string ID;//学号
    string PassW;//密码
    int LoginNum;//初次登录验证密码
    int CCourse;//学生已经选择的课程数量
public:
    SG Grade;//班级序号
    SC course[Cnum+ErrCnum];//选择的课程编号(序号)最多的情况就是课程的数量选择的课程数 
    Student();//初始化学生名字为DFS1,DFS2...
    ~Student();
    int GetStNum();//搜索学生, 返回下标和名字.
    string GetName(){return Name;}
    string GetID(){return ID;}
    string GetPassW(){return PassW;}
    int GetLoginNum(){return LoginNum;}
    int GetCCourse(){return CCourse;}
    void ChooseCourse();//进行已有的课程的选择
    void SimpleChoose(int);//根据参数选择客场
    void SearchCourse();//学生查看自己的选课情况
    void SimpleSCourse();//横向展示自己的的课程
    void SwapCourse();//删除和更换学生选课
    void SimpleDelete(int);//根据参数删除课程
    void ChangeStCourse();//换课
    void DeleteCCourse();//根据学生数组打印学生课程; 拿课程去查学生, 选课的时候存上编号.
    void ChangeSelfInfo();//更改自己的名字, 密码以及ID
}St;
```

###  2.5. <a name='-1'></a>链表对动态的适应性

在删除课程, 班级的过程中, 如果使用的是链表的结构, 到最后是真的删除这个节点, 无法找回, 而正是因为链表的纯粹性, 所以在用链表写注册和删除的时候可以非常简便, 思路自然也很清晰. 而反观数组就不一样了, 在空间复杂度上要比链表多一倍的空间, 带来的好处是调用方便, 不必遍历整个链表从头查找,  所以在开头注册登录使用链表, 在后面选课运用数组是一个高明的选择. 



###  2.6. <a name='-1'></a>输入检查

**[效果]** : 对于不符合条件的情况, 重复输入. 

**[实现]** : 对于**需要容错的重复输入的情况**, 一种简单处理的做法是写成循环; 而另外一中高明的做法就是**写成模板, 或者函数**

```cpp
# 第一种情况:
do{
	cin>>order;
    if(!order) continue;
	if(order==-1) return;
	else cout<<"请重新输入!!!";
	system("reset");
}while(order<-1||order>3);
# 第二种情况:
int InputCheck(int DownLimit, int Uplimit){
    int order=-1;
    do{
        cin>>order;
        if(!order) continue;
        if(order==-1) break;
        if(order<DownLimit||order>Uplimit)
            cout<< "[Tip]: 输入有误,请重新输入\n";        
    }while(order<DownLimit || order>Uplimit); 
    return order;
}
```



##  3. <a name='-1'></a>更多参考

之前写程序的时候输错了一个特殊的键位, 导致程序进入死循环, 但是自己还是自己加了自检机制, 所以找来 ASKII 来记录自己的错误.  

###  3.1. <a name='ASKIIsup1j1sup'></a>ASKII<sup>[1](#j1)</sup>

控制字符（ Control Character）或者功能码（Function Code）。

| 二进制   | 十进制 | 十六进制 | 缩写/字符                                    | 解释                               |
| -------- | ------ | -------- | -------------------------------------------- | ---------------------------------- |
| 00000000 | 0      | 00       | NUL (NULL)                                   | 空字符                             |
| 00000001 | 1      | 01       | SOH (Start Of Headling)                      | 标题开始                           |
| 00000010 | 2      | 02       | STX (Start Of Text)                          | 正文开始                           |
| 00000011 | 3      | 03       | ETX (End Of Text)                            | 正文结束                           |
| 00000100 | 4      | 04       | EOT (End Of Transmission)                    | 传输结束                           |
| 00000101 | 5      | 05       | ENQ (Enquiry)                                | 请求                               |
| 00000110 | 6      | 06       | ACK (Acknowledge)                            | 回应/响应/收到通知                 |
| 00000111 | 7      | 07       | BEL (Bell)                                   | 响铃                               |
| 00001000 | 8      | 08       | BS (Backspace)                               | 退格                               |
| 00001001 | 9      | 09       | HT (Horizontal Tab)                          | 水平制表符                         |
| 00001010 | 10     | 0A       | LF/NL(Line Feed/New Line)                    | 换行键                             |
| 00001011 | 11     | 0B       | VT (Vertical Tab)                            | 垂直制表符                         |
| 00001100 | 12     | 0C       | FF/NP (Form Feed/New Page)                   | 换页键                             |
| 00001101 | 13     | 0D       | CR (Carriage Return)                         | 回车键                             |
| 00001110 | 14     | 0E       | SO (Shift Out)                               | 不用切换                           |
| 00001111 | 15     | 0F       | SI (Shift In)                                | 启用切换                           |
| 00010000 | 16     | 10       | DLE (Data Link Escape)                       | 数据链路转义                       |
| 00010001 | 17     | 11       | DC1/XON (Device Control 1/Transmission On)   | 设备控制1/传输开始                 |
| 00010010 | 18     | 12       | DC2 (Device Control 2)                       | 设备控制2                          |
| 00010011 | 19     | 13       | DC3/XOFF (Device Control 3/Transmission Off) | 设备控制3/传输中断                 |
| 00010100 | 20     | 14       | DC4 (Device Control 4)                       | 设备控制4                          |
| 00010101 | 21     | 15       | NAK (Negative Acknowledge)                   | 无响应/非正常响应/拒绝接收         |
| 00010110 | 22     | 16       | SYN (Synchronous Idle)                       | 同步空闲                           |
| 00010111 | 23     | 17       | ETB (End of Transmission Block)              | 传输块结束/块传输终止              |
| 00011000 | 24     | 18       | CAN (Cancel)                                 | 取消                               |
| 00011001 | 25     | 19       | EM (End of Medium)                           | 已到介质末端/介质存储已满/介质中断 |
| 00011010 | 26     | 1A       | SUB (Substitute)                             | 替补/替换                          |
| 00011011 | 27     | 1B       | ESC (Escape)                                 | 逃离/取消                          |
| 00011100 | 28     | 1C       | FS (File Separator)                          | 文件分割符                         |
| 00011101 | 29     | 1D       | GS (Group Separator)                         | 组分隔符/分组符                    |
| 00011110 | 30     | 1E       | RS (Record Separator)                        | 记录分离符                         |
| 00011111 | 31     | 1F       | US (Unit Separator)                          | 单元分隔符                         |
| 00100000 | 32     | 20       | (Space)                                      | 空格                               |
| 01111111 | 127    | 7F       | DEL (Delete)                                 | 删除                               |

- **NUL (0)**: NULL，空字符。本意为 **NOP**（中文意为空操作），此位置可以忽略一个字符。起源于**计算机早期的记录信息的纸带**，此处留个 NUL 字符，意思是先占位，以待后用。**后来NUL 被用于C语言中，表示字符串的结束**，当一个字符串中间出现 NUL 时，就意味着这个是一个字符串的结尾了。

- **SOH (1)**: Start Of Heading，标题开始。如果信息沟通交流主要以命令和消息的形式的话，SOH 就可以用于标记每个消息的开始。1963年，最开始 ASCII 标准中，把此字符定义为 Start of Message，后来又改为现在的 Start Of Heading。现在，**这个 SOH 常见于主从（master-slave）模式的 RS232 的通信中**，一个主设备，以 SOH 开头，和从设备进行通信。这样方便从设备在数据传输出现错误的时候，**在下一次通信之前，去实现重新同步（resynchronize）**。如果没有一个清晰的类似于 SOH 这样的标记，去标记每个命令的起始或开头的话，那么重新同步，就很难实现了。

- **STX (2) 和 ETX (3)**: STX 表示 Start Of Text，意思是“文本开始”；ETX 表示 End Of Text，意思是“文本结束”。**通过某种通讯协议去传输的一个数据（包），称为一帧的话，常会包含一个帧头，包含了寻址信息，即你是要发给谁，要发送到目的地是哪里，其后跟着真正要发送的数据内容**。而 STX，就用于标记这个数据内容的开始。接下来是要传输的数据，最后是 ETX，表明数据的结束。而中间具体传输的数据内容，ASCII 并没有去定义，它和你所用的传输协议有关。

| 帧头                | 数据或文本内容                                             |                     |                            |                   |
| ------------------- | ---------------------------------------------------------- | ------------------- | -------------------------- | ----------------- |
| SOH（表明帧头开始） | ......（帧头信息，比如包含了目的地址，表明你发送给谁等等） | STX（表明数据开始） | ......（真正要传输的数据） | ETX（表明数据结束 |

- **BEL (7)**: BELl，响铃。在 ASCII 编码中，BEL 是个比较有意思的东西。BEL 用一个可以听得见的声音来**吸引人们的注意**，既可以用于计算机，也可以用于周边设备（比如打印机）。注意，BEL 不是声卡或者喇叭发出的声音，而是蜂鸣器发出的声音，主要用于报警，比如硬件出现故障时就会听到这个声音，有的计算机操作系统正常启动也会听到这个声音。**蜂鸣器没有直接安装到主板上，而是需要连接到主板上的一种外设，现代很多计算机都不安装蜂鸣器了**，**即使输出 BEL 也听不到声音，这个时候 BEL 就没有任何作用了**。

- **BS (8)**: BackSpace，退格键。退格键**起初**的意思是在**打印机和电传打字机**上，往回移动一格光标，以起到**强调该字符**的作用。比如你想要打印一个 a，然后加上退格键后，就成了 aBS^。在机械类打字机上，此方法能够起到实际的强调字符的作用，但**对于后来的 CTR** 下时期来说，就**无法起到对应效果**了。而现代所用的退格键，不仅仅表示光标往回移动了一格，同时也删除了移动后该位置的字符。

- **HT (9)**: Horizontal Tab，水平制表符，相当于 Table/Tab 键。**水平制表符的作用是用于布局**，它控制输出设备前进到下一个表格去处理。而制表符 Table/Tab 的宽度也是灵活不固定的，只不过在多数设备上制表符 Tab 都预定义为 4 个空格的宽度。**水平制表符 HT 不仅能减少数据输入者的工作量，对于格式化好的文字来说，还能够减少存储空间，因为一个Tab键，就代替了 4 个空格**。

- **LF (10)**: Line Feed，直译为“给打印机等喂一行”，也就是“换行”的意思。**LF 是 ASCII 编码中常被误用的字符之一**。**LF 的最原始的含义是，移动打印机的头到下一行。而另外一个 ASCII 字符，CR（Carriage Return）才是将打印机的头移到最左边，即一行的开始（行首）**。很多串口协议和 MS-DOS 及 Windows 操作系统，也都是这么实现的。而**C语言和 Unix 操作系统将 LF 的含义重新定义为“新行”，即 LF 和 CR 的组合效果，也就是回车且换行的意思。从程序的角度出发，C语言和 Unix 对 LF 的定义显得更加自然，而 MS-DOS 的实现更接近于 LF 的本意。现在人们常将 LF 用做“新行（newline）”的功能，大多数文本编辑软件也都可以处理单个 LF 或者 CR/LF 的组合了**。

- **VT (11)**: Vertical Tab，垂直制表符。它类似于水平制表符 Tab，目的是为了减少布局中的工作，同时也减少了格式化字符时所需要存储字符的空间。VT 控制符用于跳到下一个标记行。说实话，还真没看到有些地方需要用 VT，因为一般在换行的时候都是用 LF 代替 VT 了。

- **FF (12)**: Form Feed，换页。设计换页键，是用来控制打印机行为的。当打印机收到此键码的时候，打印机移动到下一页。不同的设备的终端对此控制符所表现的行为各不同，有些会清除屏幕，有些只是显示`^L`字符，有些只是新换一行而已。例如，Unix/Linux 下的 Bash Shell 和 Tcsh 就把 FF 看做是一个清空屏幕的命令。

- **CR (13)**: Carriage return，回车，表示机器的滑动部分（或者底座）返回。CR 回车的原意是让打印头回到左边界，并没有移动到下一行的意思。随着时间的流逝，后来人们把 CR 的意思弄成了 Enter 键，用于示意输入完毕。在数据以屏幕显示的情况下，人们按下 Enter 的同时，也希望把光标移动到下一行，因此**C语言和 Unix 重新定义了 CR 的含义，将其表示为移动到下一行。当输入 CR 时，系统也常常隐式地将其转换为LF。**

- **SO (14) 和 SI (15)**: SO，Shift Out，不用切换；SI，Shift In，启用切换。早在 1960s 年代，设计 ASCII 编码的美国人就已经想到了，ASCII 编码不仅仅能用于英文，也要能用于外文字符集，这很重要，定义 Shift In 和 Shift Out 正是考虑到了这点。最开始，其意为在西里尔语和拉丁语之间切换。西里尔语 ASCII（也即 KOI-7 编码）将 Shift 作为一个普通字符，而拉丁语 ASCII（也就是我们通常所说的 ASCII）用 Shift 去改变打印机的字体，它们完全是两种含义。在拉丁语 ASCII 中，SO 用于产生双倍宽度的字符（类似于全角），而用 SI 打印压缩的字体（类似于半角）。

- **DLE (16)**: Data Link Escape，数据链路转义。有时候我们需要在通信过程中发送一些控制字符，但是总有一些情况下，这些控制字符被看成了普通的数据流，而没有起到对应的控制效果，ASCII 编码引入 DLE 来解决这类问题。如果数据流中检测到了 DLE，数据接收端会对数据流中接下来的字符另作处理。但是具体如何处理，ASCII 规范中并没有定义，只是弄了个 DLE 去打断正常的数据流，告诉接下来的数据要特殊对待。

- **DC1 (17)**: Device Control 1，或者 XON – Transmission on。这个 ASCII 控制符尽管原先定义为 DC1， 但是现在常表示为 XON，用于串行通信中的软件流控制。其主要作用为，在通信被控制符 XOFF 中断之后，重新开始信息传输。用过串行终端的人应该还记得，当有时候数据出错了，按 Ctrl+Q（等价于XON）有时候可以起到重新传输的效果。这是因为，此 Ctrl+Q 键盘序列实际上就是产生 XON 控制符，它可以将那些由于终端或者主机方面，由于偶尔出现的错误的 XOFF 控制符而中断的通信解锁，使其正常通信。

- **DC3 (19)**: Device Control 3，或者 XOFF（Transmission off，传输中断）。

- **EM (25)**: End of Medium，已到介质末端，介质存储已满。EM 用于，当数据存储到达串行存储介质末尾的时候，就像磁带或磁头滚动到介质末尾一样。其用于表述数据的逻辑终点，即不必非要是物理上的达到数据载体的末尾。

- **FS(28) : **File Separator，文件分隔符。FS 是个很有意思的控制字符，它可以让我们看到 1960s 年代的计算机是如何组织的。我们现在习惯于随机访问一些存储介质，比如 RAM、磁盘等，但是在设计 ASCII 编码的那个年代，大部分数据还是顺序的、串行的，而不是随机访问的。此处所说的串行，不仅仅指的是串行通信，还指的是顺序存储介质，比如穿孔卡片、纸带、磁带等。

    在串行通信的时代，设计这么一个用于表示文件分隔的控制字符，用于分割两个单独的文件，是一件很明智的事情。

- **GS(29)**: Group Separator，分组符。ASCII 定义控制字符的原因之一就是考虑到了数据存储。大部分情况下，数据库的建立都和表有关，表包含了多条记录。同一个表中的所有记录属于同一类型，不同的表中的记录属于不同的类型。而分组符 GS 就是用来分隔串行数据存储系统中的不同的组。值得注意的是，当时还没有使用 Excel 表格，ASCII 时代的人把它叫做组。

- **RS(30):** Record Separator，记录分隔符，用于分隔一个组或表中的多条记录。

- **US(31):** Unit Separator，单元分隔符。在 ASCII 定义中，数据库中所存储的最小的数据项叫做单元（Unit）。而现在我们称其字段（Field）。单元分隔符 US 用于分割串行数据存储环境下的不同单元。现在的数据库实现都要求大部分类型都拥有固定的长度，尽管有时候可能用不到，但是对于每一个字段，却都要分配足够大的空间，用于存放最大可能的数据。这种做法的弊端就是占用了大量的存储空间，而 US 控制符允许字段具有可变的长度。在 1960s 年代，数据存储空间很有限，用 US 将不同单元分隔开，能节省很多空间。

- **DEL (127):** Delete，删除。有人也许会问，为何 ASCII 编码中其它控制字符的值都很小（即 0~31），而 DEL 的值却很大呢（为 127）？这是由于这个特殊的字符是为纸带而定义的。在那个年代，绝大多数的纸带都是用7个孔洞去编码数据的。而 127 这个值所对应的二进制值为111 1111（所有 7 个比特位都是1），将 DEL 用在现存的纸带上时，所有的洞就都被穿孔了，就把已经存在的数据都擦除掉了，就起到了删除的作用。

###  3.2. <a name='VKTablesup2j2sup'></a>VK Table<sup>[2](#j2)</sup>

以下摘录 Window 系统 API 中VK_系列的常量的值.

```shell
Const VK_LBUTTON = &H1
Const VK_RBUTTON = &H2
Const VK_CANCEL = &H3
Const VK_MBUTTON = &H4       ' NOT contiguous with L RBUTTON
Const VK_BACK = &H8
Const VK_TAB = &H9
Const VK_CLEAR = &HC
Const VK_RETURN = &HD
Const VK_SHIFT = &H10
Const VK_CONTROL = &H11
Const VK_MENU = &H12
Const VK_PAUSE = &H13
Const VK_CAPITAL = &H14
Const VK_ESCAPE = &H1B
Const VK_SPACE = &H20
Const VK_PRIOR = &H21
Const VK_NEXT = &H22
Const VK_END = &H23
Const VK_HOME = &H24
Const VK_LEFT = &H25
Const VK_UP = &H26
Const VK_RIGHT = &H27
Const VK_DOWN = &H28
Const VK_SELECT = &H29
Const VK_PRINT = &H2A
Const VK_EXECUTE = &H2B
Const VK_SNAPSHOT = &H2C
Const VK_INSERT = &H2D
Const VK_DELETE = &H2E
Const VK_HELP = &H2F
' VK_A thru VK_Z are the same as their ASCII equivalents: 'A' thru 'Z'
' VK_0 thru VK_9 are the same as their ASCII equivalents: '0' thru '9'
Const VK_NUMPAD0 = &H60
Const VK_NUMPAD1 = &H61
Const VK_NUMPAD2 = &H62
Const VK_NUMPAD3 = &H63
Const VK_NUMPAD4 = &H64
Const VK_NUMPAD5 = &H65
Const VK_NUMPAD6 = &H66
Const VK_NUMPAD7 = &H67
Const VK_NUMPAD8 = &H68
Const VK_NUMPAD9 = &H69
Const VK_MULTIPLY = &H6A
Const VK_ADD = &H6B
Const VK_SEPARATOR = &H6C
Const VK_SUBTRACT = &H6D
Const VK_DECIMAL = &H6E
Const VK_DIVIDE = &H6F
Const VK_F1 = &H70
Const VK_F2 = &H71
Const VK_F3 = &H72
Const VK_F4 = &H73
Const VK_F5 = &H74
Const VK_F6 = &H75
Const VK_F7 = &H76
Const VK_F8 = &H77
Const VK_F9 = &H78
Const VK_F10 = &H79
Const VK_F11 = &H7A
Const VK_F12 = &H7B
Const VK_F13 = &H7C
Const VK_F14 = &H7D
Const VK_F15 = &H7E
Const VK_F16 = &H7F
Const VK_F17 = &H80
Const VK_F18 = &H81
Const VK_F19 = &H82
Const VK_F20 = &H83
Const VK_F21 = &H84
Const VK_F22 = &H85
Const VK_F23 = &H86
Const VK_F24 = &H87
Const VK_NUMLOCK = &H90
Const VK_SCROLL = &H91
'  VK_L VK_R - left and right Alt, Ctrl and Shift virtual keys.
'  Used only as parameters to GetAsyncKeyState() and GetKeyState().
'  No other API or message will distinguish left and right keys in this way.
Const VK_LSHIFT = &HA0
Const VK_RSHIFT = &HA1
Const VK_LCONTROL = &HA2
Const VK_RCONTROL = &HA3
Const VK_LMENU = &HA4
Const VK_RMENU = &HA5
Const VK_ATTN = &HF6
Const VK_CRSEL = &HF7
Const VK_EXSEL = &HF8
Const VK_EREOF = &HF9
Const VK_PLAY = &HFA
Const VK_ZOOM = &HFB
Const VK_NONAME = &HFC
Const VK_PA1 = &HFD
Const VK_OEM_CLEAR = &HFE
```



###  3.3. <a name='PAUSEsup3j3sup'></a>PAUSE<sup>[3](#j3)</sup>

1. >  Using `system("pause");` is Ungood Practice™ because
    >
    > - It's completely **unnecessary**.
    >     To keep the program's console window open at the end when you run it from Visual Studio, use Ctrl+F5 to run it without debugging, or else place a breakpoint at the last right brace `}` of `main`. So, no problem in Visual Studio. And of course no problem at all when you run it from the command line.
    > - It's problematic & annoying
    >     when you run the program from the command line. For interactive execution you have to press a key at the end to no purpose whatsoever. And for use in automation of some task that `pause` is very much undesired!
    > - It's not portable.
    >     Unix-land has no standard `pause` command.

2. > It's frowned upon because it's a platform-specific hack that has nothing to do with actually learning programming, but instead to get around a feature of the IDE/OS - the console window launched from Visual Studio closes when the program has finished execution, and so the new user doesn't get to see the output of his new program.
    >
    > Bodging in System("pause") runs the Windows command-line "pause" program and waits for that to terminate before it continues execution of the program - the console window stays open so you can read the output.
    >
    > A better idea would be to put a breakpoint at the end and debug it, but that again has problems.


综上来说,

1. Window 的系统调用开销是比较大的, 所以运行的速度是有些慢的.
2. 黑客程序常用此函数容易造成安全漏洞
3. 书写的简洁程度
4. 程序的可移植性

取而代之, 在 Linux 系统可以用

```cpp
system("read -p 'Press Enter to continue...' var");
```

因为这个暂停操作是涉及到系统读取一个字符的操作, 所以常常和`read`, `echo`等命令有关. 自然实现的方法是多种多样的. 以后可以单独写一篇博客. 哈哈, 其他的功能操作.参考<sup>[4](#j4)</sup><sup>[5](#j5)</sup><sup>[6](#j6)</sup>; Pause函数使用<sup>[7](#j7)</sup>.

这里罗列一下看到的 Window 的等效函数,对于Linux 下的C程序一般是通过终端（Terminal）来运行，程序关闭后会留下输出结果，所以不需要暂停功能<sup>[8](#j8)</sup>:

```cpp
#include<conio.h>
getchar();getchar();
getch();
```

###  3.4. <a name='Define'></a>Define

参考:

1. https://www.cnblogs.com/alantu2018/p/8465911.html
2. https://zhuanlan.zhihu.com/p/93753907

###  3.5. <a name='std::ios_base'></a>std::ios_base

The class `ios_base` is a multipurpose class that serves as the base class for all I/O stream classes. It maintains several kinds of data: 

1) state information: stream status flags

2) control information: flags that control formatting of both input and output sequences and the imbued locale

3) private storage: indexed extensible data structure that allows both long and void* members, which may be implemented as two arbitrary-length arrays or a single array of two-element structs or another container.

4) callbacks: arbitrary number of user-defined functions to be called from imbue(), copyfmt(), and ~ios_base()

Typical implementation holds member constants corresponding to all values of fmtflags, iostate, openmode, and seekdir shown below, member variables to maintain current precision, width, and formatting flags, the exception mask, the buffer error state, a resizeable container holding the callbacks, the currently imbued locale, the private storage, and a static integer variable for xalloc().

https://blog.csdn.net/yangbomoto/article/details/80782633?utm_source=blogxgwz4

1. badbit表示发生系统级的错误，如不可恢复的读写错误。通常情况下一旦badbit被置位，流就无法再使用了。

2. failbit 表示发生可恢复的错误，如期望读取一个数值，却读出一个字符等错误。这种问题通常是可以修改的，流还可以继续使用。

3. 当到达文件的结束位置时，eofbit 和 failbit 都会被置位。

4. goodbit 被置位表示流未发生错误。如果badbit failbit 和eofbit 任何一个被置位，则检查流状态的条件会失败。

对应的bad(), fail(), eof(), good()能检查对应位是否被置位，返回1表示被置位。但是，badbit被置位时，fail()也会返回1。所以使用good()和fail()是确定流能否使用的正确方法。。实际上，流当做条件使用的代码就等价于！fail()。而且eof() 和bad() 操作只能表示特定的错误。

ios::bad: http://www.cplusplus.com/reference/ios/ios/bad/


###  3.6. <a name='Font'></a>Font

可以找到适合自己的字体, 可以参考这个网站<sup>[9](#j9)</sup>: https://www.programmingfonts.org/#cascadia-code



##  4. <a name='Afterwords'></a>Afterwords

最后, 可能是疫情隔离我与世界太久的缘故, 我已经忘记了如何和世界相处.所以造成这一切的后果之后我不能过分消极, 困难的到来不是为了停留, 而是过去, 我始终羡慕那些 逢山开路，遇水架桥 的人, 而这条心路是我不得不修炼的地方, 关于如何和这个世界相处, 如何约法三章......

---

后加: 这篇文章的主体部分, 本以为是要提交的代码迭代文档, 但是其实不是, 真正交上去的知识一个Word文件, 里面的示意图我花了有一个晚上, 但坦白的说是屁用没有......我真的越来越恶心于这里的教学方式, 相对比的是我更加羡慕那一直拿Git交作业的学生, 但这应该是未来的工作模式, 不是吗? 更多关于写文档的正确理论基础, 我会在后续学习软件工程导论这门课后释出.

<div id="j1">1. C语言中文网.</div>
<div id="j2">2. https://tieba.baidu.com/p/829777521</div>
<div id="j3">3. https://stackoverflow.com/questions/1107705/systempause-why-is-it-wrong</div>
<div id="j4">4. https://askubuntu.com/questions/108258/what-is-the-bash-equivalent-of-doss-pause-command</div>
<div id="j5">5. https://stackoverflow.com/questions/92802/what-is-the-linux-equivalent-to-dos-pause</div>
<div id="j6">6. https://stackoverflow.com/questions/92802/what-is-the-linux-equivalent-to-dos-pause</div>
<div id="j7">7. https://blog.csdn.net/m0_46198325/article/details/104331838</div>
<div id="j8">8. http://c.biancheng.net/cpp/html/3103.html</div>
<div id="j9">9. https://www.zhihu.com/question/20299865</div>
