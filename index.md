---
layout: page
title: 博文
tagline: Supporting tagline
---
{% include JB/setup %}

<ul class="posts" style="list-style-type: square;color: gainsboro;">
  {% for post in site.posts %}
    <li>
        <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
        <span style="color:gray;font-size:0.7em">{{ post.date | date_to_string }}</span> 
    </li>
  {% endfor %}
</ul>
