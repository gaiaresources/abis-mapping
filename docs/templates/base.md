{% block metadata %}---
title: {{ metadata.label }}
summary: {{ metadata.description }}
---{% endblock %}
{% block versions %}<small>
**abis-mapping** v{{ project_version }} &emsp; **{{metadata.name}}** v{{ metadata.version }}
</small>{% endblock %}

{% block body %}{% endblock %}
