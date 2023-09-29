---
layout: post
title: 你的下一臺電腦，不可能會是 iPad Pro
updated: 2023-09-29
category: thoughts
source: https://github.com/bGZo/blog/issues/24
number: 24
---





今天下午，EMS 取走了武漢寄過來的快遞，寄去了北京。Apple 退貨算是告一段落，這讓我不禁開始重新想一個問題：**我真正的需求到底是什麼**？

## 真正需求

即使後來也一遍一遍地在內心勸過自己，想要用 Pencil 去畫畫，去塗鴉，去記筆記，但至少，身爲一個寫代碼、看漫畫的人來說，但是還是覺得這是一個謊言。在這個廣告宣傳蓋過實際產品的環境，廣告是一點都不能信的。那些從產品發佈會主持人嘴中吹出來的牛逼，跑出來的火車，也許就是一種詐騙。

$$性能 > 便攜 > 續航$$

但是，我忽略了最重要的一件事情：生態。

## 放棄心路

其實越寫越想放棄，這是一種反覆幻滅的過程：

首先，是 Everything Paid 的味道。尤其是我最主要的內容消費平臺，Safari 瀏覽器，Safari 相比於 [kiwibrowser/src](https://github.com/kiwibrowser/src) 只能說是一個殘廢。我必須短時間內改變自己多年來使用 Chromium 養成的大量操作習慣。這相當不適應，或者我就只能買 App Store 第三方開發出來的插件，當然這些事情都還好。最重要的是 Tampermonkey 的缺失（即使有[quoid/userscripts](https://github.com/quoid/userscripts)），因爲 Safari 不提供 Chrome API，油猴的大多數腳本也無法無感遷移，這讓我有了第一個想退掉它的衝動。

其次，是 Apple 的閉源傲慢側載政策。基於第一點不適，我只能開始尋求開源的替代品，但就 AltStore 這樣臨時的解決方案來說相當失望。因爲 Apple 還有這樣的限制（只支持同時 Sideload 三個應用，每週 10 個 App IDs）：

> You can sideload as many apps as you want with AltStore, but due to Apple's restrictions **only 3 sideloaded apps can be active at a time**. If you try to activate more than 3 apps, you will be prompted to "deactivate" a sideloaded app first. Deactivating an app will make AltStore back up all its data before removing it from your iPhone or iPad, freeing up a slot for you to then sideload another app. Alternatively, you can manually deactivate an app at any time by long-pressing it in the My Apps tab and pressing "Deactivate".  
— [Activating Apps - AltStore](https://faq.altstore.io/how-to-use-altstore/activating-apps)  

> Every app you sideload with AltStore requires a certain number of "App IDs" to be registered with your Apple ID, which depends on the number of app extensions each app contains. **You can only register up to 10 App IDs at a time**, but each App ID expires after one week. If you want to sideload an app that requires more App IDs than you have available, you'll have to wait for enough App IDs to expire.  
— [App IDs - AltStore](https://faq.altstore.io/how-to-use-altstore/app-ids)  

所以你只能拿到 2 個側載 App 的資格（AltStore 自己要佔一個）。總的來說，就算我已經花了 $799（￥6399）買它，但我還是需要爲它的軟件政策每年付 $99 給 Apple? 真的有人願意堅守這樣的平臺嗎？[無法分配內存、也無法創建子進程，即使是本人，也無法獨立 Build 應用程序 (必須花錢去簽名)的平臺？](https://developer.apple.com/forums/thread/128859)

What A Fucking Joke?

然後，是續航，官方標稱的 10 個小時簡直讓人控訴詐騙。因爲我的體感最多也就是 5 個小時，已經掉到了 20% 以下，這還沒有接鍵盤，也沒有上蜂窩（帶筆）。就如同這個[視頻](https://www.youtube.com/watch?v=VtYL0Ye1vP8)結尾測試數據一樣，高強度 Safari 一個小時掉電 20% 是稀鬆平常的事情。和 Mac 上十多個小時的續航相形見絀。

最後一點是，當我想到自己手中這臺雞肋的設備其實等於 2 個 Steam Deck(Arch Linux) 的時候，我徹底的放棄了。

Okey, It's not worth any more.

> 我不在信任蘋果製造產品的出發點是爲了更好的用戶體驗，赤裸裸的用所謂商業策略來對消費者行使心理操縱以保證他們的利潤。2022 年了跨不過的還是 64g ，60hz ，這倆坎。 
—  [iPad Pro M2 版本已經發布 - V2EX](https://www.v2ex.com/t/887936)[^1]

Apple, you fool your customer.

[^1]: 關於此類話題的更多討論，可見：[iPad Pro 算是好產品麼？ - V2EX](https://v2ex.com/t/954360)、[放棄 iPad Pro 的原因、AI 繼續驅動應用創新、Android 14 新特性](https://iois.me/archives/15061.html) ；