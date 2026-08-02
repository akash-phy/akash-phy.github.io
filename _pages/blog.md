---
layout: page
title: Blog
permalink: /blog/
nav: true
nav_order: 4
---

<div class="post-list">
  {% for post in site.posts %}
    <article class="post-item">
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <p class="post-meta">
        {{ post.date | date: '%B %d, %Y' }}
        {% if post.tags.size > 0 %}
          &nbsp;·&nbsp;
          {% for tag in post.tags %}
            <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}">{{ tag }}</a>{% unless forloop.last %}, {% endunless %}
          {% endfor %}
        {% endif %}
      </p>
      {% if post.description %}
        <p>{{ post.description }}</p>
      {% endif %}
    </article>
    {% unless forloop.last %}<hr>{% endunless %}
  {% endfor %}
</div>
