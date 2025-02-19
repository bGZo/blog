---
layout: post
title: Hentai Reader
updated: 2025-02-19
category: posts
source: https://github.com/bGZo/blog/issues/31
number: 31
---


> [!warning]
> ⚠️ NSFW 警告：本篇文章可能包含暴力，性描寫等僅供 18 歲以上閱覽的內容。

## Why

我很喜歡色情內容，但如果把它和其他訂閱源放在一起，我一定不會再花時間琢磨別人的博客了，加上本人自制力差，容易被性暗示喚起性慾，所以對我來說，色情內容需要做隔離。

那爲什麼不用 RSSHub，還要自己用 Python 寫規則呢？

1. 定製化：我需要對拉去下來的源做附加的邏輯，比如過濾器，預覽圖替換，防盜鏈 (todo)
2. 版權：RSShub 已經算是一個知名的項目了，且對一些版權性 PR 持保守態度，樹大招風，我覺得你一定懂。
3. 週期：開發週期會被 RSShub 上游卡着，或者我本地需要部署一個 RSShub 實例，比較麻煩，加上本身菜，就當練手了。

當然，這個項目不可能盈利，僅僅是繼 [個人博客](https://blog.bgzo.cc/) 後，出於興趣探索的再一款 jekyll 博客。

有非常多侷限，如內容排版，目錄導航，視覺設計等等，還有非常多待改進的地方

![](https://raw.githack.com/bGZo/assets/dev/2025/202502150013399.png)

## How

### Vercel host via <https://hentai.bgzo.cc>

### Source via: <https://github.com/bGZo/hentai>

## What

### Features

1. Fetch RSS feeds and keep the latest resource daily
2. Persist feeds in repo and support API with following (`http://rss.bgzo.cc`) with json

| Name | Route | Description | Method | Note |
|-------|------|------|------|------|
| Feed  | `/feeds/${tag_name_with_hyphen_and_lower}` | RSS feed, return xml | `GET` | `${tag_name_with_slash_and_lower}` is the url string handle by `lower()` and hyphen(`-`). <br/>For example, we have a `DLsite Game Ranking.xml` file in server, then the correct full url address will be `http://rss.bgzo.cc/feeds/alsite-game-ranking.xml`; |
| Contents | `/archives/${year}/${month}/${day}.json` | Contents, return JSON response | `GET` | **NOTE**: The timezone of response is GMT, format it whatever you want |

### Todos

- [ ] #doing Support more sources
    - [x] https://www.dlsite.com
    - [x] https://www.4gamers.com.tw
    - [x] https://mingqiceping.com (Feed 地址失效)
    - [ ] telegram channel limit
- [ ] #todo More usable
    - [x] Separate from RSS sources configuration from codes

### Wontfix

#### 防盜鏈

一些網站本身開啓了防盜鏈，如: [靈夢御所](https://blog.reimu.net/feed)。除非單獨構建應用，或是添加請求頭 `Referer: https://blog.reimu.net`，否則在一般的瀏覽器，是無法繞過的。

比如以下圖片，你無法把它嵌入到你的博客，卻能正常通過鼠標右鍵新建標籤頁打開瀏覽。

```
https://img.reimu.net/uploads/2023/06/6499957d1a902.png
```

#### How to deal with the content only show for the user login?

So the way RSS is bankruptcy, how does you request content using common method? How do you recognize the different websites? There are too much details.

#### How to deal with the copyright?

Considered the risk of copyright, I should not build any mirror site for business content.

### Alternatives

- https://nodetics.com/feedbro
- Telegram pron channel
