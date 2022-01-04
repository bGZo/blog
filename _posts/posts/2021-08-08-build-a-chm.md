---
layout: post
title: Build A CHM File
updated: 2021-08-08
category: posts
---


CHM? Yeah have a long history...

> In 2002, Microsoft announced some security risks associated with the .CHM format, as well as some security bulletins and patches. They have since announced their intentions not to develop the .CHM format further, and will be moving to a new generation of Windows Help called Microsoft Assistance Markup Language in the Windows Vista operating system.
>
> --[Wikipedia](https://en.wikipedia.org/wiki/Microsoft_Compiled_HTML_Help)

I try to  use command under ubuntu build `chm` file about python, without GUI software help, which sounds cool. But something during Microsoft and Open Source happend, which made the solution is old and complex, but fortunately its not difficult.

Then I found out the way in [StackoverFlow](https://stackoverflow.com/questions/9174140/html-to-chm-file-under-linux), and I got they seem not interested in this file supporting acrosso-platform and friendly to phone device(file manage and photo...). I found awesome [website](https://command-not-found.com/) for giving help to *nix command which not found . The `fpc` included `chmcmd` we need, but it occupied over `675 MB` ,,, I am hesitated, so I give up, ahhhhhh.....

let's do it in windows by HugeChm made by [strnghrs](https://www.cnblogs.com/stronghorse/) with size under `140kb`! Sounds increditable, and he give two share link, like [share1-4hie](https://pan.baidu.com/s/1PnpZ3Bk-lTArrajva7EVzQ) & [share2](https://www.mediafire.com/folder/f0z2hexqdnr9a/Software). Wish it helps you. Also that's not open source. So you only could get it from above two links. No mood to do... And also in building content and language showed had some bug, such as no contents, index, bookmark and can't search anything... SO like its title, which just suits for huge file needed to package.

I also see the documents in [Microsoft](https://docs.microsoft.com/zh-cn/previous-versions/windows/desktop/htmlhelp/creating-help). But it seemed not say anything, just like bullshit...

[EasyCHM](http://www.etextwizard.com/easychm.html) is a paid software, [sold](http://www.etextwizard.com/order_easychm.html) `$259` for home and `$359` for business... Expensive....but that works. Thank God...

Maybe using `PDF` insteaded `chm` is a better choose? And [`chmlib`](https://github.com/jedwing/CHMLib) will help you a lot in spliting `CHM`.

---

建一个CHM？是的，说来话长...

> 2002 年，Microsoft 公布了一些与 .CHM 格式相关的安全风险，以及一些安全公告和补丁。此后，他们宣布不打算进一步开发 .CHM 格式，并将转向 Windows Vista 操作系统中称为 Microsoft 协助标记语言的新一代 Windows 帮助。
>
> --[维基百科](https://en.wikipedia.org/wiki/Microsoft_Compiled_HTML_Help)

我尝试在没有 GUI 软件帮助下使用 ubuntu 下的命令构建关于 python 的`chm`文件，听起来很酷。但是在微软和开源期间发生了一些事情，这使得解决方案变得陈旧而复杂，但幸运的是它并不困难。

然后我在 [StackoverFlow](https://stackoverflow.com/questions/9174140/html-to-chm-file-under-linux) 中找到了方法，我发现他们似乎对这个支持跨平台并且对手机设备友好（文件管理和照片...）的文件不感兴趣。我发现了寻找不存在命令很友好的 [网站](https://command-not-found.com/)。 它提示我需要安装`fpc`, 其中有我们需要的`chmcmd`，但是内存需要占用`675MB`，，，我犹豫了，所以放弃了，啊哈哈.....

让我们回到 Windows 中去构建, 由[strnghrs](https://www.cnblogs.com/stronghorse/) 制作的 HugeCHM, 大小居然控制在`140kb` 内！难以置信，他在博客中给了两个分享链接，比如 [share1-4hie](https://pan.baidu.com/s/1PnpZ3Bk-lTArrajva7EVzQ) 和 [share2](https://www.mediafire.com/folder/f0z2hexqdnr9a/Software)。希望这能帮到你。但这也不是开源的。所以你只能从上面两个链接进入。没心情继续做下去... 而且软件在构建内容和语言方面也显示了一些 BUG，例如没有目录，索引，书签并且无法搜索任何东西...就像它的标题写的那样，它只适合需要的大文件的打包。

我也看到了[微软](https://docs.microsoft.com/zh-cn/previous-versions/windows/desktop/htmlhelp/creating-help)中的文档。但是好像什么都没说，就跟胡说八道一样……

[EasyCHM](http://www.etextwizard.com/easychm.html) 是付费软件，家用[许可协议](http://www.etextwizard.com/order_easychm.html) `$259` 商用许可协议`$359`, 好TM贵, 好在中文互联网上有破解版....

也许用`PDF`代替`chm`会是更好的选择？而 [`chmlib`](https://github.com/jedwing/CHMLib) 会在分离`CHM`文档上帮助你很多。 
