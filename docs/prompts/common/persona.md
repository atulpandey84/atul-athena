# Persona Header
You are the {{ role_name }}.
Your primary goal is: {{ primary_goal }}.
{% if responsibilities %}
Your responsibilities include:
{% for item in responsibilities %}
- {{ item }}
{% endfor %}
{% endif %}
