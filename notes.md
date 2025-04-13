---
layout: default
title: Notes
permalink: /notes/
---

# Notes

<div class="simple-note-listing">
  <ul>
    {% assign notes = site.notes | sort: 'date' | reverse %}
    {% for note in notes %}
      {% assign note_path = note.url | remove: '/notes/' | remove: '.html' %}
      {% assign display_path = note_path | replace: '-', ' ' %}
      <li>
        <a href="{{ note.url }}">{{ display_path }}</a>
      </li>
    {% endfor %}
  </ul>
</div>
