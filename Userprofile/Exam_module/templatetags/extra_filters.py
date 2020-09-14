from django import template

register = template.Library()


@register.filter
def index(_list, _index):
    return _list[_index]


@register.simple_tag
def define(val):
    return val


@register.filter
def get_question(queryset, field):
    return queryset.filter(type=field)


@register.filter
def get_response(queryset, res, ):
    try:
        obj = queryset.response_set.get(user=res.student, question_paper=res.question_paper,
                                        question=queryset).answer
    except Exception as e:
        obj = ''
    return obj


@register.filter
def semester(queryset, sem):
    return queryset.filter(sem=sem)


@register.filter
def applied_science_subject(queryset, dept):
    return queryset.filter(dept=dept)
