---
layout: default
title: Home
---

## TL;DR

<ul class="posts">
  {% assign all_posts = site.categories.posts | concat: site.categories.thoughts %}
  {% for post in all_posts %}
    <li class="post">
      <a href="{{ post.url }}">{{ post.title }}</a>
      <time class="publish-date" datetime="{{ post.date | date: '%F' }}">
        {{ post.date | date: "%Y/%m/%d" }}
      </time>
    </li>
  {% endfor %}
</ul>
