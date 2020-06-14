try:
    from unittest import mock
except ImportError:
    import mock

from django.template import TemplateDoesNotExist

import email_utils

import pytest


html_message = '<p>An <strong>HTML</strong> message.</p>'
text_message = 'A plain text message.'


def render_both(template_name, *args, **kwargs):
    """
    Fake render function that returns both HTML and plain text.
    """
    if template_name.endswith('html'):
        return html_message

    return text_message


def render_html(template_name, *args, **kwargs):
    """
    Fake render function that returns only HTML.
    """
    if template_name.endswith('html'):
        return html_message

    raise TemplateDoesNotExist('{} does not exist'.format(template_name))


@mock.patch('email_utils.render_to_string')
@mock.patch('email_utils.mail.send_mail')
def test_send_email(mock_send, mock_render_to_string):
    """
    The send email function should load the plain text and HTML versions
    of the template, and send an email with them.
    """
    mock_render_to_string.side_effect = render_both

    context = {'foo': 'bar'}
    from_email = 'no-reply@example.com'
    recipient_list = ['test@example.com']
    subject = 'Test Email'
    template_name = 'foo'

    email_utils.send_email(
        context=context,
        from_email=from_email,
        recipient_list=recipient_list,
        subject=subject,
        template_name=template_name,
    )

    assert mock_render_to_string.call_count == 2
    assert mock_render_to_string.call_args_list[0][1] == {
        'context': context,
        'template_name': '{}.html'.format(template_name),
    }
    assert mock_render_to_string.call_args_list[1][1] == {
        'context': context,
        'template_name': '{}.txt'.format(template_name),
    }

    assert mock_send.call_count == 1
    assert mock_send.call_args[1] == {
        'from_email': from_email,
        'html_message': html_message,
        'message': text_message,
        'recipient_list': recipient_list,
        'subject': subject,
    }


@mock.patch('email_utils.render_to_string')
@mock.patch('email_utils.mail.send_mail')
def test_send_email_html(mock_send, mock_render_to_string):
    """
    If only the HTML version of the template is available, the plain
    text message should be empty.
    """
    mock_render_to_string.side_effect = render_html

    context = {'foo': 'bar'}
    template_name = 'foo'

    email_utils.send_email(context=context, template_name=template_name)

    assert mock_render_to_string.call_count == 2
    assert mock_render_to_string.call_args_list[0][1] == {
        'context': context,
        'template_name': '{}.html'.format(template_name),
    }
    assert mock_render_to_string.call_args_list[1][1] == {
        'context': context,
        'template_name': '{}.txt'.format(template_name),
    }

    assert mock_send.call_count == 1
    assert mock_send.call_args[1] == {
        'html_message': html_message,
        'message': '',
    }


@mock.patch('email_utils.render_to_string')
@mock.patch('email_utils.mail.send_mail')
def test_send_email_neither(mock_send, mock_render_to_string):
    """
    If neither template can be loaded, an exception should be thrown and
    no email should be sent.
    """
    mock_render_to_string.side_effect = TemplateDoesNotExist('foo')

    with pytest.raises(email_utils.NoTemplatesException):
        email_utils.send_email('foo')

    assert mock_send.call_count == 0
