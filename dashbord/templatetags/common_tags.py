from django import template
register = template.Library()

@register.filter
def change_null_value(var):
    if var =="NULL":
        return ""
    else:
        return var

@register.filter
def change_title_of_type_field(var):
    if var =='Guest':
        return 'مهمان'
    elif var == 'student':
        return 'دانش آموز'
    elif var == 'teacher':
        return 'معلم'
    elif var == 'operator':
        return 'اپراتور'
    else:
        return " "