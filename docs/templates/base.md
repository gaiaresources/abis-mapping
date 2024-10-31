{% block metadata %}---
title: {{ metadata.label }} - v{{ metadata.version }}
{% if metadata.template_lifecycle_status == "deprecated" %} - Deprecated{% endif %}
{% if metadata.template_lifecycle_status == "beta" %} - Beta{% endif %}
summary: {{ metadata.description }}
---{% endblock %}
{% block versions %}<small>
**abis-mapping** v{{ project_version }} &emsp; **{{metadata.name}}** v{{ metadata.version }}
</small>{% endblock %}

{% if metadata.template_lifecycle_status == "deprecated" %}
!!! warning "Template Deprecated"

    This Template is deprecated, and will be archived in the future.
    Please consider migrating to the current version of this Template.

{% endif %}
{% if metadata.template_lifecycle_status == "beta" %}
!!! warning "Template In Beta"

    This Template is in Beta, and may not be ready for use.
    Changes to the Template may be made before it is ready for use.

{% endif %}

{% block body %}{% endblock %}
