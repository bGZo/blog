---
layout: default
title: Home
---

## Recent posts

<ul class="posts">
  {% for post in site.categories.posts limit:6 %}
    <li class="post">
      <a href="/blog{{ post.url }}">{{ post.title }}</a>
      <time class="publish-date" datetime="{{ post.date | date: '%F' }}">
        {{ post.date | date: "%B %-d, %Y" }}
      </time>
    </li>
  {% endfor %}
</ul>

[See all posts](/blog/posts)
