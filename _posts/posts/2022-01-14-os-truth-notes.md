---
layout: post
title: OS Truth Notes
updated: 2022-01-13
category: posts
---


- [Bochs](https://sourceforge.net/projects/bochs/files/bochs)
  - Install
    - From Source Code
      - [gtk/gtk.h not found on Ubuntu c++](https://stackoverflow.com/questions/24955686/gtk-gtk-h-not-found-on-ubuntu-c#answer-43835758).
        - ```bash
          #~/.bashrc
          export CPATH=$CPATH:/usr/include/gtk-2.0
          export CPATH=$CPATH:/usr/include/glib-2.0/
          export CPATH=$CPATH:/usr/lib/glib-2.0/include/
          export CPATH=$CPATH:/usr/include/pango-1.0/
          export CPATH=$CPATH:/usr/lib/gtk-2.0/include/
          export CPATH=$CPATH:/usr/include/atk-1.0/
          ```
      - [glibconfig.h: No such file or directory](https://github.com/dusty-nv/jetson-inference/issues/6#issuecomment-280827061). 
        - ```bash
          sudo cp /usr/lib/x86_64-linux-gnu/glib-2.0/include/glibconfig.h /usr/include/glib-2.0/glibconfig.h
          ```
      - [cairo.h: No such file or directory](https://stackoverflow.com/questions/11918274/how-to-run-and-compile-a-cairo-file-in-ubuntu) => Not solved...
      - Giving up.
      - Seem like not use `sudo` to run `make`, so I try but still throw error `ndefined reference to symbol 'pthread_create@@GLIBC_2.2.5'` and [`error adding symbols: DSO missing from command line`](https://stackoverflow.com/questions/19901934/libpthread-so-0-error-adding-symbols-dso-missing-from-command-line). Next I cancel the `--enable-debugger` in `./configure` command. Then it works for me. I still not know why....
        ```shell
        ./configure --prefix=/home/happy/Documents/bochs --enable-disasm --enable-iodebug --enable-x86-debugger --with-x --with-x11
        ```
    - From RPM
      - ```bash
        sudo alien -i package_name.rpm
        ```
      - [libSDL2-2.0.so.0: cannot open shared object file: No such file or directory](https://stackoverflow.com/questions/29711336/libsdl2-2-0-so-0-cannot-open-shared-object-file)
        ```bash
        sudo apt install libsdl2-dev
        ```
      - Can't find auto-install path, then give up...
  - Usage
    - `mbr.S` 文件长这样. 
      ```assembly
      ; +--------------------------+
      ; |/home/xxx/test/bochs/mbr.S|
      ; +--------------------------+
      SECTION MBR vstart=0x7c00
          mov ax,cs
          mov ds,ax
          mov es,ax
          mov ss,ax
          mov fs,ax
          mov sp,0x7c00
      
          mov ax, 0x600
          mov bx, 0x700
          mov cx, 0
          mov dx, 0x184f
      
          int  0x10
      
          mov ah, 3
          mov bh, 0
          int 0x10
      
          mov ax, message
          mov bp, ax
          
          mov cx, 5
          mov ax, 0x1301
          
          mov bx, 0x2
          int 0x10
      
          jmp $
      
          message db "1 MBR"
          times 510-($-$$) db 0
          db 0x55,0xaa
      ```
      之后通过
      ```bash
      nasm -o mbr.bin mbr.S
      ```
      变成 `mbr.bin` 文件, 之后做一个 `img` 引导
      ```bash
      dd if=/home/xxx/test/bochs/mbr.bin of=/home/xxx/test/bochs/hd60M.img bs=512 count=1 conv=notrunc
      ```
    - ```bash
      # +---------------------------------+
      # |/home/xxx/test/bochs/bochsrc.disk|
      # +---------------------------------+
      megs: 32 #Memory 32M
      romimage: file=/home/xxx/test/bochs/share/bochs/BIOS-bochs-latest #Machine's BIOS
      vgaromimage: file=/home/xxx/test/bochs/share/bochs/VGABIOS-lgpl-latest #Machine's VGA BIOS
      
      boot: disk
      log: bochs.out #log out
      
      mouse: enabled=0 #close mouse
      keyboard_mapping: enabled=1, map=/home/lfh-0191121339/test/bochs/share/bochs/keymaps/x11-pc-us.map #open keyboard
      
      ata0: enabled=1, ioaddr1=0x1f0, ioaddr2=0x3f0, irq=14 #hard disk setting -> ata0
      ata0-master: type=disk, path="hd60M.img", mode=flat, cylinders=121, heads=16, spt=63 #hard disk setting -> master, importent!
      
      #gdbstub: enabled=1, port=1234, text_base=0, data_base=0, bss_base=0 #gdb support
      ```
