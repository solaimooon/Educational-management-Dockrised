from django import template
register = template.Library()

@register.filter
def change_the_result_field_of_link_table(var):
    if var == "studing":
        return 'در حال تحصیل'
    elif var == "pass":
        return 'قبول'
    else:
        return "مردود"


