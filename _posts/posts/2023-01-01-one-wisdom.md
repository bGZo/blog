---
layout: post
title: One wisdom
updated: 2025-02-13
category: posts
source: https://github.com/bGZo/blog/issues/11
number: 11
---

2023 新年伊始，整理 2022 的陳年筆記時發現有很多不知名，但是又捨不得丟棄的句子，想着乾脆把他們做成引用得了。連着建倉庫，設計頁面，寫腳本一套下來也沒花太多時間，一個簡單的靜態自動部署的網站就建好了: [One](https://one.bgzo.cc/)[^2].

![](https://unpkg.com/bgzo@23.1.1/img/one-preview.png)

## Tech stack

- Jekyll
- Github Action

## Highlights

- [x] Every single page for quote; Detail[^1] is following:

<p class="codepen" data-height="300" data-default-tab="html,result" data-slug-hash="wvxWKZb" data-user="bgzo" style="height: 300px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
  <span>See the Pen <a href="https://codepen.io/bgzo/pen/wvxWKZb">
  quotes</a> by bGZo (<a href="https://codepen.io/bgzo">@bgzo</a>)
  on <a href="https://codepen.io">CodePen</a>.</span>
</p>
<script async src="https://cpwebassets.codepen.io/assets/embed/ei.js"></script>

- [x] Generate quote by syncing Github issues with metadata;
- [x] Deploy with [Vercel](https://vercel.com)
- [x] SEO supported by plugin.
- [ ] More functions, like mobile views, share links, quote tags.
- [ ] When the quotes increasing huge, how to generate page smartly? Is possible to make a API service?[^3]

[^1]: Page design parody for [Words of Wisdom](https://wordsofwisdom.app/);
[^2]: Name inspired by [「ONE · 一個」](https://wufazhuce.com/);
[^3]: Jekyll is just a static website generation. Seem like impossible to deliver value from jekyll to js. More discuss via: [Jekyll - display a random chosen post in index - Stack Overflow](https://stackoverflow.com/questions/31490789);  