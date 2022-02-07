from django import template

OBSCENE_WORDS = ['задача', 'развитие', 'путин']

register = template.Library()


@register.filter()
def censor(value):
    array_words = value.split()
    for idx in range(0, len(array_words)):
        if array_words[idx].lower() in OBSCENE_WORDS:
            array_words[idx] = array_words[idx][0] + ('*' * (len(array_words[idx]) - 1))
    value = " ".join(array_words)
    return f'{value}'
