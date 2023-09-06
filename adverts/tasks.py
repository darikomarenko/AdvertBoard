from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Reply


@shared_task
def new_reply_notify(reply_id):
    reply = Reply.objects.get(id=reply_id)
    post = reply.post
    post_author = post.author.username
    post_title = post.title
    reply_text = reply.text
    reply_author = reply.author.username
    post_author_email = post.author.email

    mail_subj = 'New reply to your ad!'
    message = render_to_string(
        template_name='new_reply_email.html',
        context={
            'post_author': post_author,
            'post_title': post_title[:25] + '...',
            'reply_text': reply_text[:50] + '...',
            'reply_author': reply_author,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[post_author_email],
    )
    email.send()


@shared_task
def reply_status_notify(reply_id, status):
    reply = Reply.objects.get(id=reply_id)
    reply_author_name = reply.author.username
    reply_text = reply.text
    post = reply.post
    post_title = post.title
    post_author = post.author.username
    reply_author_email = reply.author.email

    mail_subj = 'Your reply status changed'
    message = render_to_string(
        template_name='reply_status_changed_email.html',
        context={
            'post_author': post_author,
            'post_title': post_title[:25] + '...',
            'reply_text': reply_text[:50] + '...',
            'reply_author': reply_author_name,
            'status': status,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[reply_author_email],
    )
    email.send()