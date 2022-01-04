---
layout: post
title: Stackover C++ Hot Hit
updated: 2021-01-21
category: posts
---

问题皆来源于下面的两个链接<sup>[1](#j1)</sup>, 本文做了部分的摘录, 感谢翻译：

1. https://stackoverflow.com/questions/tagged/c%2b%2b?tab=Votes
2. https://stackoverflow.com/questions/tagged/c?tab=Votes

<!--more-->

## QUESTIONS 问题

- 分支预测（Branch Prediction）导致有序数的效率提高.

```java
import java.util.Arrays;
import java.util.Random;

public class Main{
    public static void main(String[] args){
        // Generate data
        int arraySize = 32768;
        int data[] = new int[arraySize];

        Random rnd = new Random(0);
        for (int c = 0; c < arraySize; ++c)
            data[c] = rnd.nextInt() % 256;

        // !!! With this, the next loop runs faster
        Arrays.sort(data);

        // Test
        long start = System.nanoTime();
        long sum = 0;

        for (int i = 0; i < 100000; ++i){
            // Primary loop
            for (int c = 0; c < arraySize; ++c){
                if (data[c] >= 128)
                    sum += data[c];
            }
        }

        System.out.println((System.nanoTime() - start) / 1000000000.0);
        System.out.println("sum = " + sum);
    }
}
```

- `-->`: `--`(后减) + `>`

```c++
#include <stdio.h>
int main(){
    int x = 10;
    while (x --> 0) { //执行的顺序就是：先 x > 0，然后 x--, 表示从x到0.
        printf("%d ", x);
    }
}
```

- 引用 & 指针
    - 重复绑定对象
    - 空间占用
    - 多层嵌套
    - 赋值->`NULLPTR`
    - 相关算数运算 [本质内存地址相关计算]
    - (间址)访问用的符号不一样: `./*/->`, 共三个符号
    - 绑定临时对象, 指针容易引起 **段错误**.
    - 引用用于函数的参数和返回值, 指针不可以.
        - **C++ 标准并没有明确要求编译器该如何实现引用，但是基本上所有编译器在底层处理上都会把引用当作指针来处理。**

- 遍历字符串中的单词

```cpp
//001
#include <sstream>
#include <string>
....
	string s = "Somewhere down the road";
    istringstream iss(s);

    do{
        string subs;
        iss >> subs;
        cout << "Substring: " << subs << endl;
    } while (iss);

//002
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
....
    string sentence = "And I feel fine...";
    istringstream iss(sentence);
    copy(istream_iterator<string>(iss),
         istream_iterator<string>(),
         ostream_iterator<string>(cout, "\n"));
/*
vector<string> tokens;
copy(istream_iterator<string>(iss),
     istream_iterator<string>(),
     back_inserter(tokens));
*/ /*
vector<string> tokens{istream_iterator<string>{iss},
                      istream_iterator<string>{}};
*/

```

- `explicit`: 拒绝隐式转换（implicit conversion）.  添加的位置在 **构造函数前面**.
  
- **隐式转化:** 在面向对象中, 可以从基本类型通过 构造函数 转化为对应的函数类型.
  
- `using namespace std`: 命名冲突有关，与性能是没有关系。两个库函数重名问题. 

- 位（bit）
    - 0UL 表示 无符号长整型 0 ; 1UL 表示 无符号长整型 1, 不加`UL`表示`INT`
    - 置 1（bit-set）: `number |= 1UL << n;`
    - 清零（bit-clear）: `number &= ~(1UL << n);` 
    - 取反（bit-toggle）: `number ^= 1UL << n;`
    - 检查（bit-check）: `bit = (number >> n) & 1U;`
    - 根据另一个变量来置位: `number ^= (-x ^ number) & (1UL << n);`

- sql 优化插入操作.

- 类型转换的正确用法和应用场景
    - `static_cast`: 静态转换的意思，也就是在编译期间转换，转换失败的话会抛出一个编译错误。
        - 基本数据类型之间的转换。[安全性开发人员保证]
        - void 指针转换成目标类型的指针。[安全性开发人员保证]
        - 任何类型的表达式转换成 void 类型。
        - 有转换构造函数或类型转换函数的类与其它类型之间的转换。
        - 类层次结构中基类和子类之间指针或引用的转换。进行上行转换（即子类的指针或引用转换成基类表示）是安全的，不过一般在进行这样的转化时会省略 static_cast；进行下行转换（即基类指针或引用转换成子类表示）时，由于没有动态类型检查，所以是不安全的，一般用 dynamic_cast 来替代。
    - `dynamic_cast` : 动态转换, 会在运行期借助 RTTI 进行类型转换（这就要求基类必须包含虚函数），主要用于类层次间的下行转换（即基类指针或引用转换成子类表示）。对于指针，如果转换失败将返回 NULL；对于引用，如果转换失败将抛出 std::bad_cast 异常。
    - `const_cast`: 修改类型的 const 或 volatile 属性
    - `reinterpret_cast` : 重新解释的意思，顾名思义，reinterpret_cast 这种转换仅仅是对二进制位的重新解释，不会借助已有的转换规则对数据进行调整，非常简单粗暴，所以风险很高。
    - C 语言风格类型转化`(type)value` + 函数式风格类型转换`type(value)`
        - 其实是一个意思，只是写法风格的差异而已。它涵盖了上面四种`*_cast`的所有功能，同时它的使用需要完全由程序员自己把控。
    
- 不需要对`malloc`返回的值进行转换
    - C 中，从 void* 到其它类型的指针是自动转换的，所以无需手动加上类型转换。
    - 在旧式的 C 编译器里，如果一个函数没有原型声明，那么编译器会认为这个函数返回 int。那么，如果碰巧代码里忘记包含头文件 <stdlib.h>，那么编译器看到malloc 调用时，会认为它返回一个 int。
    - 维护的耦合度高.

- `include` 的 `<>` & `""` diff
    - `<filename>`一般会去系统路径和编译器预指定的路径找。
    - `"filename"`一般会去工程目录下找

- 三法則: 简单来说, 为了日后维护方便, C++里三个成员函数缺一不可:
    - 析构函数 
    - 复制构造函数
    - 赋值运算符 (C++)
      
        - C++ 会以值语义处理用户自定义类型的对象，这就是说在不同的上下文环境中, 
        
        - 关于构造赋值函数 (copy constructor) 的编写**[手动管理资源]**, 国内的教材一般说明是 **开辟额外内存空间**, 其实一般更好的方式是 **在构造函数(constructor)中创建资源，并在析构函数释放资源。** 对于忘记写构造赋值函数 (copy constructor)的后果就是 **析构野指针, 引发 [未定义行为错误](https://stackoverflow.com/questions/2397984/undefined-unspecified-and-implementation-defined-behavior)**. 
        
        - ```cpp
            // 1. copy constructor
            person(const person& that){
                name = new char[strlen(that.name) + 1];
                strcpy(name, that.name);
                age = that.age;
            }
            
            // 2. copy assignment operator
            person& operator=(const person& that){
                if (this != &that){
                    delete[] name;
                    // This is a dangerous point in the flow of execution!
                    // We have temporarily invalidated the class invariants,
                    // and the next statement might throw an exception,
                    // leaving the object in an invalid state :(
                    name = new char[strlen(that.name) + 1];
                    strcpy(name, that.name);
                    age = that.age;
                }
                return *this;
            }
            ```
        
        - 注意，初始化构造和赋值的区别是：在对`name`赋值前需要先释放其内存。同时也需要自检查，如果没有自检查，`delete[] name`会将`that`对象的字符串也析构掉。 
        
        - 异常安全: 然而，在因为内存耗尽`new char[...]`抛出异常的时候，赋值运算符就无法保持 [强异常安全保证](https://en.wikipedia.org/wiki/Exception_safety)。可以利用一个局部变量来解决这个问题，
        
            ```c++
            // 2. copy assignment operator
            person& operator=(const person& that){
                char* local_name = new char[strlen(that.name) + 1];
                // If the above statement throws,
                // the object is still in the same state as before.
                // None of the following statements will throw an exception :)
                strcpy(local_name, that.name);
                delete[] name;
                name = local_name;
                age = that.age;
                return *this;
            }
            ```
        
            这同时也解决了自赋值的问题，不需要显示检查是否是自身赋值。其实，还有一个更好的办法可以解决这个问题：[copy-and-swap](https://github.com/EthsonLiu/stackoverflow-top-cpp/blob/master/question/016%20-%20copy-and-swap%20%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F.md)，不过不在这里作深入讨论，读者可以跟随链接具体了解。
        
            我之所以在此处提及异常，是想说：手写一个管理资源的类并不是我们想象中的那么容易。
        
        - C++11 以来特殊成员函数大家庭又新加入了两名成员：移动构造函数和移动赋值运算符。
        
            ```cpp
            class person{
                std::string name;
                int age;
            
            public:
                person(const std::string& name, int age);        // Ctor
                person(const person &) = default;                // Copy Ctor
                person(person &&) noexcept = default;            // Move Ctor
                person& operator=(const person &) = default;     // Copy Assignment
                person& operator=(person &&) noexcept = default; // Move Assignment
                ~person() noexcept = default;                    // Dtor
            };
            ```
        
        - 智能指针管理类???

- [运算符重载.](<https://stackoverflow.com/questions/4421706/what-are-the-basic-rules-and-idioms-for-operator-overloading)

- `??!??!`符号: `??!`是一个 [三字符组](https://zh.wikipedia.org/wiki/%E4%B8%89%E5%AD%97%E7%AC%A6%E7%BB%84%E4%B8%8E%E5%8F%8C%E5%AD%97%E7%AC%A6%E7%BB%84)，编译器会自动翻译成`|`, `{ | } ~ ` 都有这样的转化.[历史原因[-EBCDIC](https://zh.wikipedia.org/wiki/EBCDIC)]

    ```cpp
    !ErrorHasOccured() ??!??! HandleError();
    ```

- 内存模型

-  C++ 的标准输入流慢于 Python 

    - 默认情况下，cin 与 stdin 总是保持同步的，也就是说这两种方法可以混用，而不必担心文件指针混乱，同时 cout 和 stdout 也一样，两者混用不会输出顺序错乱。正因为这个兼容性的特性，导致 cin 有许多额外的开销，如何禁用这个特性呢`std::ios_base::sync_with_stdio(false);` 这样就可以取消 cin 于 stdin 的同步了。但是会导致`scanf`&`cin`混用缓冲区冲突的问题.

- [Linux分析C++性能?](https://stackoverflow.com/questions/375913/how-can-i-profile-c-code-running-on-linux)

- [智能指针](https://stackoverflow.com/questions/106508/what-is-a-smart-pointer-and-when-should-i-use-one)
    - 利用了 RAII（资源获取即初始化）技术对普通的指针进行封装，这使得智能指针实质是一个对象，行为表现的却像一个指针。C++ 标准一共有四种智能指针：auto_ptr、unique_ptr、shared_ptr 和 weak_ptr。其中 auto_ptr 在 C++11 已被摒弃，C++17 中被移除不可用了。
    - 作用: 
        - 防止忘记调用 delete。
        - 异常安全
    - 主要是**从 value 语义转化为 reference 语义**

- [目前使用模板的唯一方法就是在头文件中实现为内联。](https://stackoverflow.com/questions/495021/why-can-templates-only-be-implemented-in-the-header-file)

- `:-!!` 

    ```cpp
    /* Force a compilation error if condition is true, but also produce a
       result (of value 0 and type size_t), so the expression can be used
       e.g. in a structure initializer (or where-ever else comma expressions
       aren't permitted). */
    #define BUILD_BUG_ON_ZERO(e) (sizeof(struct { int:-!!(e); }))
    #define BUILD_BUG_ON_NULL(e) ((void *)sizeof(struct { int:-!!(e); }))
    ```

    - `(e)`：计算 e 表达式
    - `!!(e)`：两次逻辑否操作。也就是，如果 e == 0，就返回 0，否则返回 1
    - `-!!(e)`：对上面的第 2 步得到的值置负。也就是，0 的负数还是 0，1 的负数为 -1
    - `struct{int: -!!(0);} --> struct{int: 0;}`：根据第 3 步，如果是 0，那么就声明一个结构体，里边定义了一个位域长度为 0 的匿名位域变量，此时编译正常通过
    - `struct{int: -!!(1);} --> struct{int: -1;}`：但如果是 -1 的话，位域长度为负数，那编译器就会报错了
    - 因为`assert`是运行期判断，上面的宏是编译期。不过自 C++ 11 起，也支持静态断言了，可以参考 [static_assert](https://zh.cppreference.com/w/cpp/language/static_assert)

- 移动语义（move semantics）

    - 在函数嵌套写法中, 会造成同一个变量的数据从运算结果到匿名变量再到指定变量中 (如`string b(x + y);`, `x+y`->`匿名变量`->`b`), 这个时候如果用移动构造函数, 把匿名函数的内存空间拿给指定变量中, 时间复杂度就可以降下来.

    - **写法:** 右值引用`&&`.

        ```cpp
            string(string&& that){ // 这个叫做移动构造函数
                data = that.data;
                that.data = nullptr;
            }
        ```

- C 语言中, `a[5] == 5[a]`

    - C语言定义`[]` 为 ` a[b] == *(a + b)`

- 使用指针而不是对象本身？
    - **生命周期**
        - 对象被创建在栈上，它的特点就是脱离作用域后会自动销毁。
        - 指针在堆上动态创建一个对象，它的特点就是即使脱离作用域，该对象也会一直存在，除非你手动释放（delete）它，否则就会出现内存泄漏。
    - **什么时候使用 new**
        - **延长对象生命周期。** 
        - **你需要很多内存。** 
    - **什么时候使用指针**
        - **引用语义（reference semantics）：** 有的时候，你希望函数传递进来的参数不是一份副本（copy），因为创建副本的代价很大。这个时候，你就可以通过指针。不过 C++ 11 已经有了移动（move）语义，这个问题就不用担心了。
        - **多态（polymorphic）：** 对于多态类型，指针和引用可以避免对象被切片（slice）。切片的意思就是说：在函数传参处理多态变量时，如果一个派生类对象在向上转换（upcast），用的是传值的方式，而不是指针和引用，那么，这个派生类对象在 upcast 以后，将会被 slice 成基类对象，也就是说，派生类中独有的成员变量和方法都被 slice 掉了，只剩下和基类相同的成员变量和属性。
        - 希望表示对象是可选的（optional）：** 指针可以被赋值为 nullptr，也就是空的意思，你可以通过设置指针为 nullptr，来表达忽略该变量的含义。C++ 17 新增了 `std::optional`，那么这个问题也可以得到解决。
        - **你想通过解耦编译单元来减少编译时间：**  如果对象都是指针指向的，那么只需要这个类型的前向声明就可以。这可以分离编译过程的各个部分，会显著提高编译时间。
        - **兼容 C 库：** C 库的接口大多都是以指针返回对象，这个时候你就不得不用指针。当然你也可以使用智能指针来封装它，这样使用起来就方便了。

- extern "c" 是什么意思？

    -  `extern "C"` 用来告诉 **C++ 编译器**，这部分代码要按照 C 语言的方式去链接。

- 将 0.1f 更改为 0 性能会降低 10 倍？.md

    - **由[非规格化浮点数](https://blog.csdn.net/AaricYang/article/details/91358149)造成的。**处理器对非规格化浮点数的处理效率比规格化浮点数要慢 10-100 倍。下面是针对上面的代码所做的测试

- 数字转字符串

    - ```CPP
        #include <iostream>
        #include <string>
        #include <sstream>
        
        int main(){
            int a=10;
            std::stringstream ss;
            ss << a;
            std::string str=ss.str();
            std::cout<<str<<'\n';
        
            //char *instr=std::itoa(a);
            //std::string stri = std::string(instr);
            //std::cout<<stri<<'\n';
            //Portability This function is not defined in ANSI-C 
            // and is not part of C++, but is supported by some compilers.
        
            std::string s=std::to_string(42);
            std::cout<<s<<'\n';
        }
        ```

- 什么时候该定义虚析构函数，为什么要这么做？

    - 当你通过一个基类指针去删除（delete）派生对象的时候，虚析构函数就很用了。
    
- [C++11 中的 lambda 表达式是什么](https://stackoverflow.com/questions/7627098/what-is-a-lambda-expression-in-c11>)

-  `const int *`, `const int * const` 和 `int const *` 

    - `int * p` - p is pointer to int
    - `int const * p` - p is pointer to const int
    - `int * const p` - p is const pointer to int
    - `int const * const p` - p is const pointer to const int

    其中，下面两个是等同的，只是顺序的不同而已，

    - const int * == int const *
    - const int * const == int const * const

    当然还有更复杂的，

    - `int ** p` - p is pointer to pointer to int
    - `int ** const p` - p is const pointer to pointer to int
    - `int * const * p` - p is pointer to const pointer to int
    - `int const ** p` - p is pointer to pointer to const int
    - `int * const * const p` - p is const pointer to const pointer to int
    - [读懂 C 的类型声明（译）](https://ethsonliu.com/2020/04/reading-c-type-declarations.html)

- [虚函数的重要性](https://stackoverflow.com/questions/2391679/why-do-we-need-virtual-functions-in-c)?

- C 语言中的函数指针是怎么用的？

- POD: Plain Old Data

    - C++ 中的 Plain Old Data Structure 是一个聚合类，仅包含 POD 成员，没有自定义的析构函数，没有自定义的赋值运算符，并且没有非静态成员指针。

- extern 关键字在不同的源文件间共享变量

    - ```cpp
        extern int a; // 声明，a 的定义可能在其它的文件
        int b; // 定义，b 占有实际的内存
        ```

- 将一个大的数组的所有成员初始化为相同的值？

    - ```cpp
        //C
        // 1.
        int myArray[10] = { 1, 2 }; // initialize to 1,2,0,0,0..
        
        // 2.
        int myArray[10] = { 0 }; // all elements 0
        
        // 3.
        int myArray[10];
        memset(myArray, 0, sizeof(myArray));
        
        //c++
        //1
        int myArray[10] = {}; // all elements 0 in C++, but is not allowed with C
        //2
        int myArray[10];
        fill(myArray, myArray + 10, 3); // 数组元素都会被赋值为 3
        ```

- 确定数组的元素个数

    - ```cpp
        //1
        int a[17];
        size_t n = sizeof(a) / sizeof(int);// size_t n = sizeof(a) / sizeof(a[0]);
        //2 large size -> define
        #define NELEMS(x)  (sizeof(x) / sizeof((x)[0]))
        int a[17];
        size_t n = NELEMS(a);
        ```

- switch case 里面不可以定义变量, 需要加作用域副号.

- Struct & Class

    - 仅当成员都是 POD 类型且都是 public 的时候用 `struct`。

- 构造函数里面调用构造函数

    - 在 C++11 中可以

- std::string 转 const char * 或者 char * 类型

    - `string::c_str()` 的返回类型就是 `const char *`，末尾带结束符 `\0`

    -   ```c++
        std::string str;
        const char * c = str.c_str();
        ```

- `typedef` &  `using` 区别

    - 除了 `using` 还可以在模板中使用，其它的都是等同的

-  C++ 程序员应尽量避免使用 `new`

    - C++ 并不带自动 GC。任何的 `new` 都需要有对应的 `delete`，否则就会有内存泄漏。

    - ```cpp
        std::string *someString = new std::string(...); //1
        delete someString;
        
        std::string someString(...);//2
        ```

    - 这就是 [RAII](http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization) 技术。当离开它的作用域的时候，`someString` 便会自动析构。而且 C++11 完善了智能指针，旨在可以更方便地帮助我们实现 RAII，我们可以适当地加以利用。

- 仿函数

    - 重载了括号运算符 () 的对象, 不过它具有函数的一些性质, 可以在需要函数的地方（主要是**各种容器和算法**）使用。
    - 仿函数可以拥有（多个）状态。
    - C++11 带来了 `std::bind` 和 `std::function`，它们也可以完成仿函数的工作。

- typeof struct

    - ```cpp
        typedef struct Foo { ... } Foo; // 1 定义一个名称是 Foo 的结构体，并别名 Foo；
        typedef struct { ... } Foo;     // 2 定义一个匿名的结构体，并别名 Foo。
        //两者的区别就是后者无法被前置声明
        ```

    - C 标准（[C89 §3.1.2.3](http://port70.net/~nsz/c/c89/c89-draft.txt), [C99 §6.2.3](http://port70.net/~nsz/c/c99/n1256.html#6.2.3), [C11 §6.2.3](http://port70.net/~nsz/c/c11/n1570.html#6.2.3)）把不同类型的标识符（identifier）分到不同的命名空间（namespace）。例如标签标识符（tag identifiers）struct/union/enum 在标签命名空间，普通标识符（ordinary identifiers），typedef 修饰的别名和其它类型都在普通命名空间。C语言中`struct Foo { ... }; Foo x;`这样的用法会报错

- i++ & ++i
  
    - 在 for 语句中，建议使用 `++i`。如果 i 是一个基本类型（short/int/...）的话，`++i` 和 `i++` 其实没什么区别。但如果 i 是一个自定义类型的话，它的 `operator++` 后自加重载比前自加多了一次临时对象的构造，所以从效率上讲，前自加更快。因此，不管是从习惯，还是风格一致上来讲，前自加 `++i` 是更好的选择。


- 声明 & 定义

    - 声明不分配存储空间，定义会分配
    - 声明可以多次，但定义只能一次

- 接口

    - CPP 没有接口这个说法，但有虚函数, 可以实现类似接口的功能。

    - ```cpp
        class IDemo{ // “接口”
            public:
                virtual ~IDemo() {}
                virtual void OverrideMe() = 0;
        };
        
        class Parent{
            public:
                virtual ~Parent();
        };
        
        class Child : public Parent, public IDemo{
            public:
                virtual void OverrideMe(){
                    //do stuff
                }
        };
        ```

- 去除 `std::string` 头尾空格

    - ```cpp
        // trim from start (in place)
        static inline void ltrim(std::string &s) {
            s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) {
                return !std::isspace(ch);
            }));
        }
        
        // trim from end (in place)
        static inline void rtrim(std::string &s) {
            s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
                return !std::isspace(ch);
            }).base(), s.end());
        }
        
        // trim from both ends (in place)
        static inline void trim(std::string &s) {
            ltrim(s);
            rtrim(s);
        }
        ```

- 宏定义里加`while(1)`的意义

    - 其实是为了把这个宏模拟成一条真实的语句。但总有人会忘记加上 `{}`。所以加上 do-while 或者 if-else 就可以解决这个问题。`

- `malloc` & `calloc`

    - `calloc` 会申请内存，并全初始化为 0；而 `malloc` 只申请内存，并不作初始化。所以 `calloc` 的执行会比 `malloc` 稍微费时，因为它多了初始化的步骤。

- [不使用加、减、乘、除、取余的情况下，实现除以 3 的功能](https://stackoverflow.com/questions/11694546/divide-a-number-by-3-without-using-operators>)

- - ```cpp
        // replaces the + operator
        int add(int x, int y){
            while (x) {
                int t = (x & y) << 1;
                y ^= x;
                x = t;
            }
            return y;
        }
        
        int divideby3(int num){
            int sum = 0;
            while (num > 3) {
                sum = add(num >> 2, sum);
                num = add(num >> 2, num & 3);
            }
            if (num == 3)
                sum = add(sum, 1);
            return sum; 
        }
    ```
  
- C 语言布尔类型


  - ```cpp
    #include <stdbool.h>//1. 只在 C99 有效，如果可以，建议使用这个。
    
    typedef enum { false, true } bool;//2
    
    typedef int bool;//3
    enum { false, true };
    
    typedef int bool;//4
    #define true 1
    #define false 0
    ```

-  `std::string` 全部转为小写字母


  - ```cpp
    #include <algorithm>
    #include <cctype>
    #include <string>
    
    std::string data = "Abc";
    std::transform(data.begin(), data.end(), data.begin(),
        [](unsigned char c){ return std::tolower(c); });
    ```

- 对象切割（object slicing）


  - 切割: 把一个子类对象赋给父类，那么相比父类，子类对象多出的成员会被丢弃掉

- `push_back` 和 `emplace_back` 的区别


  - `emplace_back` 能就地通过参数构造对象，不需要拷贝或者移动内存，相比 `push_back` 能更好地避免内存的拷贝与移动，使容器插入元素的性能得到进一步提升。在大多数情况下应该优先使用 `emplace_back` 来代替 `push_back`。

- C++ 实现一个单例模式


  - ```cpp
    class S{
        public:
            static S& getInstance(){
                static S instance; // C++11 保证这是线程安全的
                return instance;
            }
        private:
            S() {}
        public:
            S(S const&) = delete; // 《Effective Modern C++》提到，用 delete 更有益于编译器的错误提示
            void operator=(S const&)  = delete;
    };
    ```

- 成员函数结尾加`const`


  - 表示该函数不允许修改成员变量（除 `mutable` 修饰的变量），且也只能调用 `const` 成员函数

-  C++ 标准规定类型 int 和 long 的长度大小


  - ```
    sizeof(char) == 1
    sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)
    
    sizeof(signed char)   == 1
    sizeof(unsigned char) == 1
    
    sizeof(short)     >= 2
    sizeof(int)       >= 2
    sizeof(long)      >= 4
    sizeof(long long) >= 8
    ```

- 结构体sizeof 不等于每个成员的 sizeof 之和


  - [失传的C结构体打包技艺 -- 内存对齐](http://www.catb.org/esr/structure-packing/)

- 拼接两个` std::vector`

    - ```cpp
        // vector2 拷贝到 vector1
        vector1.insert(vector1.end(), vector2.begin(), vector2.end());
        
        // vector2 移动到 vector1，此时 vector2 不可再用
        vector1.insert(vector1.end(), std::make_move_iterator(vector2.begin()), std::make_move_iterator(vector2.end()));
        ```

- 用 static_cast 取代 C 语言的强制转换

    - 是对的，C 式的强制转换看不出语义，也不利用编译器的错误检查，具体参考：[static_cast, dynamic_cast, const_cast 和 reinterpret_cast 怎么用？](https://github.com/EthsonLiu/stackoverflow-top-cpp/blob/master/question/010%20-%20static_cast%2C%20dynamic_cast%2C%20const_cast%20%E5%92%8C%20reinterpret_cast%20%E6%80%8E%E4%B9%88%E7%94%A8%EF%BC%9F.md)

- 拼接字符串

    - ```cpp
        std::string name = "John";
        int age = 21;
        std::string result;
        
        // 1. with C++11 
        // 安全。
        // 需要 C++11 的支持，需 `#include <string>`，标准所支持，跨平台。
        result = name + std::to_string(age);
        
        // 2. with IOStreams
        //安全、低效、代码啰嗦。
        // 需 `#include <sstream>`，标准所支持，跨平台。
        std::stringstream sstm;
        sstm << name << age;
        result = sstm.str();
        
        // 3. with itoa
        // 容易出错（你需要分配足够的内存）、快速、代码啰嗦。
        // `itoa` 不是一个标准方法，不确定可以在所有平台适用。
        char numstr[21]; // enough to hold all numbers up to 64-bits
        result = name + itoa(age, numstr, 10);
        
        // 4. with sprintf
        // 容易出错（你需要分配足够的内存）、快速、代码啰嗦。
        // 标准所支持，跨平台。
        char numstr[21]; // enough to hold all numbers up to 64-bits
        sprintf(numstr, "%d", age);
        result = name + numstr;
        ```

- 检测无符号整数溢出

    - ```cpp
        // 加法检测
        #include <limits.h>
        
        int a = <something>;
        int x = <something>;
        if ((x > 0) && (a > INT_MAX - x)) /* `a + x` would overflow */;
        if ((x < 0) && (a < INT_MIN - x)) /* `a + x` would underflow */;
        
        // 减法检测
        #include <limits.h>
        int a = <something>;
        int x = <something>;
        if ((x < 0) && (a > INT_MAX + x)) /* `a - x` would overflow */;
        if ((x > 0) && (a < INT_MIN + x)) /* `a - x` would underflow */;
        
        // 乘法检测
        #include <limits.h>
        
        int a = <something>;
        int x = <something>;
        // There may be a need to check for -1 for two's complement machines.
        // If one number is -1 and another is INT_MIN, multiplying them we get abs(INT_MIN) which is 1 higher than INT_MAX
        if ((a == -1) && (x == INT_MIN)) /* `a * x` can overflow */
        if ((x == -1) && (a == INT_MIN)) /* `a * x` (or `a / x`) can overflow */
        // general case
        if (a > INT_MAX / x) /* `a * x` would overflow */;
        if ((a < INT_MIN / x)) /* `a * x` would underflow */;
        ```

-  `size_t` 定义在头文件 `stddef.h` 中，标准规定它是一个至少 16 位的无符号整型。在我的机器上它是这样的，

    ```c
    typedef unsigned long size_t;
    ```

- 检测一个元素是否在 std::vector 中

    - ```cpp
        #include <algorithm>
        #include <vector>
        vector<int> vec; 
        
        if (std::find(vec.begin(), vec.end(), item) != vec.end())
           do_this();
        else
           do_that();
        ```

- [前置声明](https://stackoverflow.com/questions/553682/when-can-i-use-a-forward-declaration)

    - 定义一个指针或引用
    - 函数参数或返回值，但没法使用它们的成员变量或函数

- 读取文件内容

    - ```cpp
        //1. 按空格和换行符进行分割
        int a, b;
        while (infile >> a >> b){
            // process pair (a,b)
        }
        //2. 读取每行，然后按空格分割
        #include <sstream>
        #include <string>
        
        std::string line;
        while (std::getline(infile, line)){
            std::istringstream iss(line);
            int a, b;
            if (!(iss >> a >> b)) { break; }
        
            // process pair (a,b)
        }
        ```

- 优雅的初始化 std:vector

    - ```c++
        static const int arr[] = {16,2,77,29};
        vector<int> vec (arr, arr + sizeof(arr) / sizeof(arr[0]));
        ```

    -   如果你的编译器支持 C++ 11 的话，可以直接这样，

    -   ```c++
        std::vector<int> v = {1, 2, 3, 4};
        ```

- 如何使用 C 或 C++ 获取目录中的文件列表？不使用 `ls` 

    - ```cpp
        // Linux 平台
        char dirname[] = "/usr/local"
        DIR *dir_ptr;
        struct dirent *direntp;
         
        dir_ptr = opendir(dirname);
        if (dir_ptr == NULL)
            fprintf(stderr,"Ls: can not open %s",dirname);
        else
        {
            direntp = readdir(dir_ptr);
            while(direntp == NULL)
                printf("%s\n",direntp->d_name);
            
            closedir(dir_ptr);
        }
        
        //Windows 平台
        #include <windows.h>
        #include <tchar.h>
        #include <stdio.h>
        
        void _tmain(int argc, TCHAR *argv[])
        {
            WIN32_FIND_DATA FindFileData;
            HANDLE hFind;
        
            if (argc != 2)
            {
               _tprintf(TEXT("Usage: %s [target_file]\n"), argv[0]);
               return;
            }
        
            _tprintf (TEXT("Target file is %s\n"), argv[1]);
            hFind = FindFirstFile(argv[1], &FindFileData);
            if (hFind == INVALID_HANDLE_VALUE) 
            {
               printf ("FindFirstFile failed (%d)\n", GetLastError());
               return;
            } 
            else 
            {
               _tprintf (TEXT("The first file found is %s\n"), FindFileData.cFileName);
               FindClose(hFind);
            }
        }
        
        //C++17
        #include <string>
        #include <iostream>
        #include <filesystem>
        namespace fs = std::filesystem;
        
        int main()
        {
            std::string path = "/path/to/directory";
            for (const auto & entry : fs::directory_iterator(path))
                std::cout << entry.path() << std::endl;
        }
        ```

- typename & class 区别, 一些场景下是有区别不可替换的

    - ```cpp
        template<typename param_t>// C++ 允许在类内定义类型别名，
        class Foo
        {
            typedef typename param_t::baz sub_t;
        };
        
        template < template < typename, typename > class Container, typename Type >// 当定义模板的模板时，也必须用 class
            
        template class Foo<int>;//当显式实例化模板的时候，必须用 class
        ```

- [有什么好的办法可以在 C/C++ 程序段错误退出时输出堆栈信息，来方便查找错误么？](https://stackoverflow.com/questions/77005/how-to-automatically-generate-a-stacktrace-when-my-program-crashes)

    - 在 Linux 平台下可以使用 `<execinfo.h>` 里的 `backtrace_*` 函数，详见 [Backtraces](http://www.gnu.org/software/libc/manual/html_node/Backtraces.html). 

- static const VS #define VS enum
    - 如果需要传指针，那只能用 (1)
    - (1) 不能作为全局作用域下数组的维数定义，而 (2)(3) 可以
    - (1) 不能作为函数作用域下静态数组的维数定义，而 (2)(3) 可以
    - (1) 不能在 switch 语句下使用，而 (2)(3) 可以
    - (1) 不能用来初始化另一个静态常量，而 (2)(3) 可以
    - (2) 可以用预处理器判断是否已存在，而 (1)(3) 不可以
        - 大多场景下，enum 是最佳选择。 **如果是 C++ 语言，那么自始至终都应该使用 (1)。**


- **段错误**: 是由于程序访问了本不属于它的的内存而引起的错误。每当遇到段错误时，你就应该知道程序在内存访问上出错了。比如，访问了已释放的变量、写入只读内存......在大多数语言中，段错误在本质上都是相同的，在 C 和 C++ 中也是一样。要想重现段错误很简单，解引用一个空指针就会出现，


- [静态库和动态库](https://zhuanlan.zhihu.com/p/71372182)
    - **后缀名不同**: 
        - 动态库的后缀，在 Windows 上是 `.dll`，linux 上是 `.so`，在 OSX 上是 `.dylib`。
        - 静态库，在 WIndows 上是 `.lib`，linux 上是 `.a`。
    - **可执行文件大小不一样**: 静态链接的可执行文件要比动态链接的可执行文件要大得多，因为它将需要用到的代码从二进制文件中“拷贝”了一份，而动态库仅仅是复制了一些重定位和符号表信息。
    - **扩展性与兼容性不一样**: 如果静态库中某个函数的实现变了，那么可执行文件必须重新编译，而对于动态链接生成的可执行文件，只需要更新动态库本身即可，不需要重新编译可执行文件。正因如此，使用动态库的程序方便升级和部署。
    - **依赖不一样**: 静态链接的可执行文件不需要依赖其他的内容即可运行，而动态链接的可执行文件必须依赖动态库的存在。所以如果你在安装一些软件的时候，提示某个动态库不存在的时候也就不奇怪了。即便如此，系统中存在一些大量公用的库，所以使用动态库并不会有什么问题。
    - **加载速度不一样**: 由于静态库在链接时就和可执行文件在一块了，而动态库在加载或者运行时才链接，因此，对于同样的程序，静态链接的要比动态链接加载更快。所以选择静态库还是动态库是空间和时间的考量。但是通常来说，牺牲这点性能来换取程序在空间上的节省和部署的灵活性时值得的，再加上局部性原理，牺牲的性能并不多。
- 随机数
    - Linux 平台上建议使用 [random and srandom](https://linux.die.net/man/3/random)。如果你需要更安全的随机数，建议使用 [libsodium](https://github.com/jedisct1/libsodium) 的接口 `randombytes`，


- 文件所有内容到`string`

    -  <http://insanecoding.blogspot.com/2011/11/how-to-read-in-file-in-c.html>

    - ```cpp
        #include <string>
        #include <cstdio>
        
        std::string get_file_contents(const char *filename)
        {
          std::FILE *fp = std::fopen(filename, "rb");
          if (fp)
          {
            std::string contents;
            std::fseek(fp, 0, SEEK_END);
            contents.resize(std::ftell(fp));
            std::rewind(fp);
            std::fread(&contents[0], 1, contents.size(), fp);
            std::fclose(fp);
            return(contents);
          }
          throw(errno);
        }
        
        #include <fstream>
        #include <string>
        
        std::string get_file_contents(const char *filename)
        {
          std::ifstream in(filename, std::ios::in | std::ios::binary);
          if (in)
          {
            std::string contents;
            in.seekg(0, std::ios::end);
            contents.resize(in.tellg());
            in.seekg(0, std::ios::beg);
            in.read(&contents[0], contents.size());
            in.close();
            return(contents);
          }
        }
        ```

- [constexpr 和 const](https://stackoverflow.com/questions/14116003/difference-between-constexpr-and-const)

    - <https://www.zhihu.com/question/35614219>

-  nullptr: 一个常量 
  - **在 C 语言编程中，请使用 `NULL`。** 此时的 `NULL`，要么是 `((void*)0)`，要么是 0，对于 C 语言而言，都无所谓。
  - **在 C++ 语言编程中，请使用 `nullptr`。** 既为了避免以后出现 bug，也为了养成一个良好的编程习惯。`nullptr` 在实际编程中的应用实在太广泛，因此 C++ 编译器一般都会把 `nullptr` 定为关键字，避免程序员的滥用。
- 内联函数
    - 内联只是一种建议，并不要求编译器必须执行。如果内联函数本身开销较大（比如含有 for、switch、递归等），编译器可能拒绝内联展开。再者，现代编译器在函数内联的决策处理会比人类手写来的更准确。
    - 什么时候该用 inline 函数？

        如果这个函数的定义也放在头文件，那么你应该用 inline 修饰它。

    - 怎么让编译器不去 inline 函数？

        在 GCC 编译器下，可以使用 `__attribute__(( noinline ))` 修饰；而在 Visual Studio 下，则是 `__declspec(noinline)`。

- endl & `\n`
  
    - `std::endl` 可以刷新输出缓冲区，而 `\n` 不会。说白了就是下面的代码，
    
- `.hpp` & `.h`
    - 后缀命名不同的优点：

        1. 代码自动格式化。一些插件可以根据后缀来自动区分哪个是 C 代码，哪个是 C++，来进行对应的格式化。
        2. 语言区分。从后缀就可以很容易区分，这个文件下是 C 还是 C++。
        3. 文件命名。C++ 很容易引入 C 库，如果引入了一个 C 库内的头文件 `feature.h`，而 C++ 不得不对这个文件的代码进行面向对象设计，那么为了保持命名和语义上的统一，将 C++ 文件命名为 `feature.hpp` 是最佳的选择。

- 迭代器失效

    - [Containers library](https://en.cppreference.com/w/cpp/container) 下的各个容器都有详细的介绍。例如容器 array 下 https://en.cppreference.com/w/cpp/container/array#Iterator_invalidation

- [mutable](https://stackoverflow.com/questions/105014/does-the-mutable-keyword-have-any-purpose-other-than-allowing-the-variable-to) 
  
  
  -  https://liam.page/2017/05/25/the-mutable-keyword-in-Cxx/
  
- 匿名命名空间 & static 


    - ```cpp
        // 非法代码
        static class sample_class { /* class body */ };
        static struct sample_struct { /* struct body */ };
        // 合法代码
        namespace {  
            class sample_class { /* class body */ };
            struct sample_struct { /* struct body */ };
        }
        ```

- [noexcept](https://stackoverflow.com/questions/10787766/when-should-i-really-use-noexcept)
  
- https://ethsonliu.com/2020/04/cpp11-noexcept.html
  
-  [指针左右问题](https://stackoverflow.com/questions/859634/c-pointer-to-array-array-of-pointers-disambiguation)
   
- https://ethsonliu.com/2020/04/reading-c-type-declarations.html
  
- CPP 获取 Shell

    - ```cpp
        #include <cstdio>
        #include <iostream>
        #include <memory>
        #include <stdexcept>
        #include <string>
        #include <array>
        
        std::string exec(const char* cmd) {
            std::array<char, 128> buffer;
            std::string result;
            std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
            if (!pipe) {
                throw std::runtime_error("popen() failed!");
            }
            while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
                result += buffer.data();
            }
            return result;
        }
        ```

- [enum class & enum](https://stackoverflow.com/questions/18335861/why-is-enum-class-preferred-over-plain-enum)

- 宏来判断当前的系统类型

    - ```cpp
        #if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
           //define something for Windows (32-bit and 64-bit, this part is common)
           #ifdef _WIN64
              //define something for Windows (64-bit only)
           #else
              //define something for Windows (32-bit only)
           #endif
        #elif __APPLE__
            #include <TargetConditionals.h>
            #if TARGET_IPHONE_SIMULATOR
                 // iOS Simulator
            #elif TARGET_OS_IPHONE
                // iOS device
            #elif TARGET_OS_MAC
                // Other kinds of Mac OS
            #else
            #   error "Unknown Apple platform"
            #endif
        #elif __linux__
            // linux
        #elif __unix__ // all unices not caught above
            // Unix
        #elif defined(_POSIX_VERSION)
            // POSIX
        #else
        #   error "Unknown compiler"
        #endif
        ```

- 程序所在的目录

    - ```cpp
        #include <string>
        #include <windows.h>
        
        std::string getexepath()
        {
          char result[ MAX_PATH ];
          return std::string( result, GetModuleFileName( NULL, result, MAX_PATH ) );
        }// window
        
        #include <string>
        #include <limits.h>
        #include <unistd.h>
        
        std::string getexepath()
        {
          char result[ PATH_MAX ];
          ssize_t count = readlink( "/proc/self/exe", result, PATH_MAX );
          return std::string( result, (count > 0) ? count : 0 );
        }//linux
        ```

    - [指向类成员的指针](https://stackoverflow.com/questions/670734/pointer-to-class-data-member)

        -  pointer to member

- [decltypeauto](https://stackoverflow.com/questions/24109737/what-are-some-uses-of-decltypeauto)

<br>

**Over!**

## LINK 链接

- [C 语言有什么奇技淫巧？](https://www.zhihu.com/question/27417946/)

    

![](https://z3.ax1x.com/2021/06/28/RNt0kn.png)

<div id="j1"> [1]. https://github.com/ethsonliu/stackoverflow-top-cpp </div>