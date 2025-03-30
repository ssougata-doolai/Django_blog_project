from django.shortcuts import render, get_object_or_404, redirect
from . models import (
    Post,
    Comment,
    PostPreference,
    CommentPreference,
    PostReport )
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

def blank(text):
    count = 0
    for i in text:
        if i != ' ':
            count += 1
    if count <= 5:
        return 0
    else:
        return count

class PostListView(ListView):
    model = Post
    template_name = 'blogs/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')


class PostDetailView(DetailView):
#    model = Post
    context_object_name = 'object'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs.get('pk'),published_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id = self.kwargs.get('pk')).order_by('-created_date')
        if self.request.user.is_authenticated:
            context['post_pref'] = PostPreference.objects.filter(user = self.request.user,post_id = self.kwargs.get('pk')).first()
            context['com_pref'] = CommentPreference.objects.filter(user = self.request.user,comment_id = self.kwargs.get('comment_id')).first()

        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['comments'],2)
        try:
            context['comments'] = paginator.page(page)
        except PageNotAnInteger:
            context['comments'] = paginator.page(1)
        except EmptyPage:
            context['comments'] = paginator.page(num_pages)

        return context

class Search(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blogs/search.html'

    def get_context_data(self, **kwargs):
        context = super(Search,self).get_context_data(**kwargs)
        s = self.request.GET.get('search')
        if s:
            context['search'] = s
            context['results'] = Post.objects.filter(title__icontains=s)
            print(context['results'])
            return context

class Topic(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blogs/topic.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Post.objects.filter(topic=self.kwargs.get('topic'),published_date__lte=timezone.now()).order_by('-created_date')

    """def get_context_data(self, **kwargs):
        context = super(Search,self).get_context_data(**kwargs)
        s = get_object_or_404(Post, topic=self.kwargs.get('name'))
        if s:
#            context['search'] = s
            context['results'] = Post.objects.filter(topic__icontains=s)
#            print(context['results'])
            return context
    """


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','topic','text','thumbnail']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.POST.get('publish'):
            super().form_valid(form)
            post = form.instance
            post.save()
            return render(self.request,'blogs/confirm_publish.html',{'post':post})
        else:
            messages.success(self.request,f'Blog "{form.instance.title}" is Saved to Draft')
        return super().form_valid(form)

@login_required
def confirm_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user == post.author:
        post.published_date = timezone.now()
        post.save()
        messages.success(request,f'Blog "{post.title}" is published')
        return redirect("blogs:blogs-index")
    else:
        raise PermissionDenied


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','topic','text','thumbnail']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = self.get_object()
        if self.request.POST.get('publish'):
            super().form_valid(form)
            post = form.instance
            post.save()
            return render(self.request,'blogs/confirm_publish.html',{'post':post})
        else:
            if post.published_date != None:
#                print("post",post.edited)
                post.edited = True
                post.save()
            messages.success(self.request,f'Blog "{form.instance.title}" is Updated')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'blogs/comment_update_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        comment = self.get_object()
        super().form_valid(form)
        comment = form.instance
        comment.save()
        messages.success(self.request,f'Comment "{form.instance.comment}" is Updated')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('blogs:post-details',kwargs={'pk':post.pk},)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class MyDraftListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = 'blogs/draft_list.html' #<app>/<model>_<viewtype>/html
    context_object_name = 'posts'

    def test_func(self):
        if self.request.user.username == self.kwargs.get('username'):
            return True
        return False

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user,published_date=None).order_by('-created_date')

class MyPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = 'blogs/post_list.html' #<app>/<model>_<viewtype>/html
    context_object_name = 'posts'

    def test_func(self):
        print("user:  ",self.request.user.username)
        print("useras:  ",self.kwargs.get('username'))
        if self.request.user.username == self.kwargs.get('username'):
            return True
        return False

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user,published_date__isnull=False).order_by('-created_date')


class UserPostListView(ListView):
    model = Post
    template_name = 'blogs/user_post_list.html' #<app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user,published_date__lte=timezone.now()).order_by('-created_date')

@login_required
def AddComment(request,pk):
    if request.method == "POST":
        c = request.POST.get('the_comment')
        print("value of comment= '",c,"'")
        if blank(c) == 0:
            return JsonResponse({})
        post = get_object_or_404(Post,pk = pk)
        comment = Comment()
        comment.post_id = pk
        comment.comment = c
        comment.author = request.user
        comment.created_date = timezone.now()
        comment.save()

        comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
        context = {}
        context['result'] = 'Created succesfully'
        context['commenttpk'] = comment.pk
        context['comment'] = comment.comment
        context['created'] = comment.created_date

        return JsonResponse(context)
    else:
        return JsonResponse(context)


@login_required
def post_preference(request,pk,user_preference):
    if request.method == "GET":
        post = get_object_or_404(Post,pk = pk)
        obj = ''
        valueobj = ''
        context = {}
        try:
            obj = PostPreference.objects.get(user=request.user,post=post)
            valueobj = obj.value
            valueobj = int(valueobj)
            user_preference = int(user_preference)
            if valueobj != user_preference:
                obj.delete()

                upref = PostPreference()
                upref.user = request.user
                upref.post = post
                upref.value = user_preference

                if user_preference == 1 and valueobj != 1:
                    post.likes += 1
                    post.dislikes -= 1
                elif user_preference == 2 and valueobj != 2:
                    post.likes -= 1
                    post.dislikes += 1
                upref.save()
                post.save()
                if request.user.is_authenticated:
                    context['value'] = upref.value
                    context['json_post_like'] = post.likes
                    context['json_post_dislike'] = post.dislikes
                    return JsonResponse(context)
                else:
                    return reverse('blogs:post-details', kwargs={'pk':pk})
#                return HttpResponseRedirect(reverse('blogs:post-details',args=(post.pk,)))
            elif valueobj == user_preference:
                obj.delete()

                if user_preference == 1:
                    post.likes -= 1
                elif user_preference == 2:
                    post.dislikes -= 1
                post.save()
                if request.user.is_authenticated:
                    context['value'] = None
                    context['json_post_like'] = post.likes
                    context['json_post_dislike'] = post.dislikes
                    return JsonResponse(context)
                else:
                    return reverse('blogs:post-details', kwargs={'pk':pk})
#                return HttpResponseRedirect(reverse('blogs:post-details',args=(post.pk,)))
        except PostPreference.DoesNotExist:
            upref = PostPreference()
            upref.user = request.user
            upref.post = post
            upref.value = user_preference
            user_preference = int(user_preference)
            if user_preference == 1:
                post.likes += 1
            elif user_preference == 2:
                post.dislikes += 1
            upref.save()
            post.save()
            if request.user.is_authenticated:
                context['value'] = upref.value
                context['json_post_like'] = post.likes
                context['json_post_dislike'] = post.dislikes
                return JsonResponse(context)
            else:
                return reverse('blogs:post-details', kwargs={'pk':pk})
#            return HttpResponseRedirect(reverse('blogs:post-details',args=(post.pk,)))
        else:
            post = get_object_or_404(Post,pk=pk)
            if request.user.is_authenticated:
                context['value'] = None
                context['json_post_like'] = post.likes
                context['json_post_dislike'] = post.dislikes
                return JsonResponse(context)
            else:
                return reverse('blogs:post-details', kwargs={'pk':pk})

#            return HttpResponseRedirect(reverse('blogs:post-details',args=(post.pk,)))

@login_required
def comment_preference(request, blog_id,comment_id,user_preference):
    if request.method == "GET":
        context = {}
        post = get_object_or_404(Post,pk = blog_id)
        comment = get_object_or_404(Comment,pk = comment_id)
        obj = ''
        valueobj = ''
        try:
            obj = CommentPreference.objects.get(user=request.user,comment=comment)
            valueobj = obj.value
            valueobj = int(valueobj)
            user_preference = int(user_preference)
            if valueobj != user_preference:
                obj.delete()

                upref = CommentPreference()
                upref.user = request.user
                upref.post = post
                upref.comment = comment
                upref.value = user_preference

                if user_preference == 1 and valueobj != 1:
                    comment.likes += 1
                    comment.dislikes -= 1
                elif user_preference == 2 and valueobj != 2:
                    comment.likes -= 1
                    comment.dislikes += 1
                upref.save()
                comment.save()
                context['com_value'] = upref.value
                context['json_com_like'] = comment.likes
                context['json_com_dislike'] = comment.dislikes
                return JsonResponse(context)
#                return HttpResponseRedirect(reverse('blogs:post-details',args=(blog_id,)))
            elif valueobj == user_preference:
                obj.delete()

                if user_preference == 1:
                    comment.likes -= 1
                elif user_preference == 2:
                    comment.dislikes -= 1
                comment.save()
                context['com_value'] = None
                context['json_com_like'] = comment.likes
                context['json_com_dislike'] = comment.dislikes
                return JsonResponse(context)
#                return HttpResponseRedirect(reverse('blogs:post-details',args=(blog_id,)))
        except CommentPreference.DoesNotExist:
            upref = CommentPreference()
            upref.user = request.user
            upref.post = post
            upref.comment = comment
            upref.value = user_preference
            user_preference = int(user_preference)
            if user_preference == 1:
                comment.likes += 1
            elif user_preference == 2:
                comment.dislikes += 1
            upref.save()
            comment.save()
            context['com_value'] = upref.value
            context['json_com_like'] = comment.likes
            context['json_com_dislike'] = comment.dislikes
            return JsonResponse(context)
#            return HttpResponseRedirect(reverse('blogs:post-details',args=(blog_id,)))
        else:
            post = get_object_or_404(Post,pk=blog_id)
            context['com_value'] = None
            context['json_com_like'] = post.likes
            context['json_com_dislike'] = post.dislikes
            return JsonResponse(context)
#            return HttpResponseRedirect(reverse('blogs:post-details',args=(blog_id,)))

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = PostReport
    fields = ['feedback','feedback_text']
    template_name = 'blogs/feedback.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
#        print("kasflj",self.post)
        form.instance.post = Post.objects.filter(pk=self.kwargs.get('blog_id')).first()
        return super().form_valid(form)
