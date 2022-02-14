---
layout: default
title: Thoughts
---

## Thoughts

> 'Man Thinks, God Laughs.' --by _Milan Kundera_

<ul class="posts">
  {% for thought in site.categories.thoughts %}
    <li class="post">
      <a href="/blog{{ thought.url }}">{{ thought.title }}</a>
      <time class="publish-date" datetime="{{ thought.date | date: '%F' }}">
        {{ thought.date | date: "%B %-d, %Y" }}
      </time>
    </li>
  {% endfor %}
</ul>