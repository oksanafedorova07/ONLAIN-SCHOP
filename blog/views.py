import django.views.generic
from django.urls import reverse_lazy, reverse
from .models import Post


class PostListView(django.views.generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailView(django.views.generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj


class PostCreateView(django.views.generic.CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(django.views.generic.UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(django.views.generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')