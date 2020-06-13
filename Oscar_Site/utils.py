from django.utils.encoding import force_text


def ajax_response_form(form):
    form_spec = {
        'fields': {},
        'field_order': [],
        'errors': form.non_field_errors()
    }
    for field in form:
        field_spec = {
            'label': force_text(field.label),
            'value': field.value(),
            'help_text': force_text(field.help_text),
            'errors': [
                force_text(e) for e in field.errors
            ],
            'widget': {
                'attrs': {
                    k: force_text(v)
                    for k, v in field.field.widget.attrs.items()
                }
            }
        }
        form_spec['fields'][field.html_name] = field_spec
        form_spec['field_order'].append(field.html_name)
    return form_spec
