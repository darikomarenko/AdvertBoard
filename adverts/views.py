from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .filters import *


class PostListView(ListView):
    template_name = 'posts_list.html'
    context_object_name = 'posts_list'
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print(context)
        return context

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date_of_creation').select_related('author')
        print(queryset)
        return queryset


class PostSearchView(ListView):
    model = Post
    template_name = 'posts_search.html'
    ordering = '-date_of_creation'
    context_object_name = 'posts_search'
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        print(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetailView(DetailView, CreateView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_post = context.get('post')
        context['replies_to_this_post'] = current_post.replies_to_post.all()

        if self.request.user.id is None:
            context['current_user_left_reply'] = False
        else:
            context['current_user_left_reply'] =\
                context['replies_to_this_post'].filter(author=self.request.user).exists()

        print(context)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('adverts/post_detail', kwargs={'pk': f'{self.object.post.pk}'})

    def form_valid(self, form, **kwargs):
        repl = form.save(commit=False)
        repl.author = self.request.user
        repl.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


@login_required(login_url='account_login')
def post_delete_ask(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post,
        'question': 'Are you sure you want to delete this post?',
    }
    return render(
        request,
        'post_delete.html',
        context=context,
    )


@login_required(login_url='account_login')
def post_delete_confirm(request, pk):
    Post.objects.get(id=pk).delete()
    return redirect(
        to='posts_list'
    )


@login_required(login_url='account_login')
def reply_delete_ask(request, pk, reply_pk):
    post = Post.objects.get(id=pk)
    current_reply = post.replies_to_post.get(id=reply_pk)
    context = {
        'reply': current_reply,
        'question': 'Are you sure you want to delete this reply?',
    }
    return render(
        request,
        'post_delete.html',
        context=context,
    )


@login_required(login_url='account_login')
def reply_delete_confirm(request, pk, reply_pk):
    post = Post.objects.get(id=pk)
    post.replies_to_post.get(id=reply_pk).delete()
    return redirect(
        to='posts_list',
    )


@login_required(login_url='account_login')
def reply_approve_and_disapprove(request, pk, reply_pk):
    post = Post.objects.get(id=pk)
    current_reply = post.replies_to_post.get(id=reply_pk)

    if not current_reply.is_approved and not current_reply.is_rejected:
        current_reply.approve()
    elif current_reply.is_approved and not current_reply.is_rejected:
        current_reply.disapprove()
    elif not current_reply.is_approved and current_reply.is_rejected:
        current_reply.unreject()
        current_reply.approve()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='account_login')
def reply_reject_and_unreject(request, pk, repl_pk):
    post = Post.objects.get(id=pk)
    current_reply = post.replies_to_post.get(id=repl_pk)

    if not current_reply.is_rejected and not current_reply.is_approved:
        current_reply.reject()
    elif current_reply.is_rejected and not current_reply.is_approved:
        current_reply.unreject()
    elif not current_reply.is_rejected and current_reply.is_approved:
        current_reply.disapprove()
        current_reply.reject()

    return redirect(request.META.get('HTTP_REFERER'))


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'account_login'
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print(context)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


class ProfilePostsView(ListView):
    template_name = 'profile_posts.html'
    ordering = '-date_of_creation'
    context_object_name = 'profile_posts'
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        print(context)
        return context

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        self.filterset = ProfilePostFilter(self.request.GET, queryset)
        return self.filterset.qs


class ProfileRepliesView(ListView):
    template_name = 'profile_replies.html'
    ordering = '-date_of_creation'
    context_object_name = 'profile_replies'
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        print(context)
        return context

    def get_queryset(self):
        queryset = Reply.objects.filter(author=self.request.user)
        self.filterset = ProfileReplyFilter(self.request.GET, queryset)
        return self.filterset.qs