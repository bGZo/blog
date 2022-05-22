---
layout: default
title: Thoughts
---

## Thoughts

> [Clichés](https://www.detailedpedia.com/wiki-Clich%C3%A9) pointless, therefore only the following are reserved: 

<ul class="posts">
  {% for thought in site.categories.thoughts %}
    <li class="post">
      <a href="{{ thought.url }}">{{ thought.title }}</a>
      <time class="publish-date" datetime="{{ thought.date | date: '%F' }}">
        {{ thought.date | date: "%B %-d, %Y" }}
      </time>
    </li>
  {% endfor %}
</ul>
