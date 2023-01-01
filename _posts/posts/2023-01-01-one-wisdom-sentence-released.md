---
layout: post
title: One wisdom sentence released
updated: 2023-01-01
category: posts
comment_link: https://github.com/bGZo/blog/issues/11
---

2023 新年伊始, 整理 2022 的陈年笔记时发现有很多不知名, 但是又舍不得丢弃的句子, 想着干脆把他们做成引用得了. 连着建仓库, 设计页面, 写脚本一套下来也没花太多时间, 一个简单的静态自动部署的网站就建好了. Deploy Address: https://one.bgzo.cc

![](https://unpkg.com/bgzo@23.1.1/img/one-preview.png)

## One tech stack

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
- [ ] When the quotes increasing huge, how to generate page smartly? Is possible to make a API service?

[^1]: Page design parody for [Words of Wisdom](https://wordsofwisdom.app/);