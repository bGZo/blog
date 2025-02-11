---
layout: default
title: Home
---

<ul class="posts">
  {% assign all_posts = site.categories.posts | concat: site.categories.thoughts %}
  {% assign all_posts = all_posts | sort: "date" | reverse %}
  {% for post in all_posts %}
    <li class="post">
      <a href="{{ post.url }}">{{ post.title }}</a>
      <time class="publish-date" datetime="{{ post.date | date: '%F' }}">
        {{ post.date | date: "%Y/%m/%d" }}
      </time>
    </li>
  {% endfor %}
</ul>
