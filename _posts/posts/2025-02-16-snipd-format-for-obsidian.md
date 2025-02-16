---
layout: post
title: Snipd format for Obsidian
updated: 2025-02-16
category: posts
source: https://github.com/bGZo/blog/issues/32
number: 32
---

<!--title:""-->

> [!NOTE]
> This is a very early version, if something help, I would maintain it.

## Repo Meta

![](https://img.shields.io/github/stars/bGZo/snipd-podcast-format-for-obsidian?style=for-the-badge&label=stars) ![](https://img.shields.io/github/repo-size/bGZo/snipd-podcast-format-for-obsidian?style=for-the-badge&label=size) ![](https://img.shields.io/github/created-at/bGZo/snipd-podcast-format-for-obsidian?style=for-the-badge&label=since)

<iframe src="https://www.youtube.com/embed/bB-VWtidB5E" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen/>

## Why

Snipd export all snips to a singal file by default. And they cannot be queried by obsidian. That's okey when you just only have severals snips. But after two years usage, I have more than 3,000 snips on platform.

Export 3000 snips, format it manually, then delete them one by one?

Okey, sounds like a hell.

My solution is, using this script to separate them to them files, then you could copy them to obsidian.

So how the data on Snipd deal with? I choose to delete account, even though the origin data is still on server, cause Snipd only support export all snips one time. The design is weird so I have no idea what to do.

Is there any free alternatives? I wondered.

Anyway, this workflow works for me, and I really wish Snipd could consider the Obsidian use case.

That's would be awesome.

At least not now : (

## Quick Start

```shell
git clone git@github.com:bGZo/snipd-podcast-format-for-obsidian.git
cd snipd-podcast-format-for-obsidian

# install pipx
sudo apt install pipx

# install poetry
pipx install poetry

# install dependency
poetry install 

# run
poetry run snipd snipd-export.md -o /path/you/want/export
```
