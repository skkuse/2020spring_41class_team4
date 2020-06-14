from django.core import mail
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string


class NoTemplatesException(Exception):
    """
    Exception indicating no templates could be loaded.
    """
    def __init__(self, template_base):
        """
        Args:
            template_base:
                The base name used to look up plain text and HTML
                templates.
        """
        self.base = template_base

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            A string indicating the templates that could not be found.
        """
        return "Could not find the template '{html}' or '{text}'.".format(
            html='{}.html'.format(self.base),
            text='{}.txt'.format(self.base),
        )


def send_email(template_name, context=None, *args, **kwargs):
    """
    Send a templated email.

    To generate the message used for the email, the method first
    searches for an HTML template with the given name
    (eg: <template>.html), and renders it with the provided context. The
    process is repeated for the plain text message except a 'txt'
    extension is used. All other options are forwarded to Django's
    ``send_mail`` function.

    Args:
        template_name:
            The name of the template to use without an extension. The
            extensions ``html`` and ``txt`` are appended to the template
            name and then rendered to provide the email content.
        context:
            A dictionary containing the context to render the message
            with. Defaults to an empty dictionary.

    Returns:
        ``1`` if the email is succesfully sent and ``0`` otherwise. The
        return values come from Django's ``send_mail`` function.

    Throws:
        NoTemplatesException:
            If neither the HTML nor plain text template can be loaded.
    """
    context = context or {}

    try:
        html = render_to_string(
            context=context,
            template_name='{}.html'.format(template_name),
        )
    except TemplateDoesNotExist:
        html = ''

    try:
        text = render_to_string(
            context=context,
            template_name='{}.txt'.format(template_name),
        )
    except TemplateDoesNotExist:
        text = ''

    if not html and not text:
        raise NoTemplatesException(template_name)

    return mail.send_mail(
        *args,
        html_message=html,
        message=text,
        **kwargs
    )
