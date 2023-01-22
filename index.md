---
layout: default
title: Home
---

## Recent Posts

<ul class="posts">
  {% for post in site.posts limit:5 %}
    <li class="post">
      <a href="{{ post.url }}">{{ post.title }}</a>
      <time class="publish-date" datetime="{{ post.date | date: '%F' }}">
        {{ post.date | date: "%Y/%m/%d" }}
      </time>
    </li>
  {% endfor %}
</ul>

[See all posts](/posts.html)
