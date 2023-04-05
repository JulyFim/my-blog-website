from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from django.template.defaultfilters import slugify
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
from . import forms
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class BlogListView(ListView):
    paginate_by = 4
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-id']


class Search(ListView):
    template_name = 'blog/index.html'
    paginate_by = 4
    context_object_name = 'posts'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return models.Post.objects.filter(
            Q(title__icontains=search) | Q(main_text__icontains=search)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class NewPostView(View):
    @staticmethod
    def get(request):
        post_form = forms.PostForm()

        return render(request, 'blog/new_post.html', {'post_form': post_form})

    @staticmethod
    def post(request):
        title = request.POST.get('title')

        author = get_object_or_404(models.User, username=request.user.username)

        main_text = request.POST.get('main_text')

        category = get_object_or_404(models.Category, id=request.POST.get('category'))
        request.POST.get('tag')

        image = request.FILES.get('image')
        models.Post.objects.create(
            title=title,
            slug=slugify(title),
            author=author,
            main_text=main_text,
            category=category,
            image=image,
        )
        messages.success(request, 'Post successfully added.')
        return redirect('home')


class AboutUsView(View):
    @staticmethod
    def get(request):
        template_name = 'blog/about.html'
        return render(request, template_name=template_name, )


class ContactUsView(View):
    @staticmethod
    def get(request):
        return render(request, 'blog/contact.html')


class BlogDetail(View):
    @staticmethod
    def get(request, slug):
        post = get_object_or_404(models.Post, slug=slug)

        post_category = get_object_or_404(models.Category, slug=post.category.slug)
        related_posts = models.Post.objects.filter(category=post_category).order_by('-id')[:3]

        comments = models.Comment.objects.filter(post=post).order_by('-id')[:6]
        categories = models.Category.objects.all()

        comment_form = forms.CommentForm()
        return render(request, 'blog/post.html', {'post': post,
                                                  'comments': comments,
                                                  'categories': categories,
                                                  'related_posts': related_posts,
                                                  'comment_form': comment_form
                                                  })

    @staticmethod
    def post(request, slug):
        post = get_object_or_404(models.Post, slug=slug)

        user_name = str(request.user)
        if user_name == 'AnonymousUser':
            messages.error(request, 'You have to be authorized to leave a comment.')
            return redirect('details', slug)

        user = get_object_or_404(User, username=request.user.username)
        name = user.username
        email = user.email
        comment_text = request.POST.get('comment_text')

        if email:
            models.Comment.objects.create(name=name, email=email, comment_text=comment_text, post=post)
            return redirect('details', slug)
        models.Comment.objects.create(name=name, email='None', comment_text=comment_text, post=post)
        return redirect('details', slug)


class CategoryDetail(View):
    @staticmethod
    def get(request, category_slug):
        category = get_object_or_404(models.Category, slug=category_slug)
        posts = models.Post.objects.filter(category=category)
        categories = models.Category.objects.all()
        return render(request, 'blog/index.html', {'posts': posts,
                                                   'categories': categories,
                                                   })


class RegisterUser(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            messages.error(request, 'You are already in the system')
            return redirect('home')
        form = forms.NewUserForm()
        return render(request, 'blog/register.html', {'form': form})

    @staticmethod
    def post(request):
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        messages.error(request, 'Unsuccessful registration.')
        return redirect('register')


class LogOutUser(View):
    @staticmethod
    def get(request):
        logout(request)
        messages.info(request, 'Logged out successful.')
        return redirect('home')


class LoginUser(View):
    @staticmethod
    def get(request):
        form = AuthenticationForm
        return render(request, 'blog/login.html', {'form': form})

    @staticmethod
    def post(request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, f'You are logged in as {user}.')
                return redirect('home')
            messages.error(request, "Authentication fault.")
        messages.error(request, "Invalid data. Please, make sure data you give matches all form needs.")
        return redirect('login', )


class UpdateUserProfile(View):
    @staticmethod
    def get(request):
        profile = get_object_or_404(models.UserProfile, user=request.user)
        form = forms.UserProfileForm(instance=profile)
        return render(request, 'blog/update_profile.html', {'form': form})

    @staticmethod
    def post(request):
        form = forms.UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = get_object_or_404(models.UserProfile, user=request.user)
            new_avatar = form.cleaned_data.get('avatar')
            new_bio = form.cleaned_data.get('bio')
            new_address = form.cleaned_data.get('address')

            # setting data
            if new_avatar:
                profile.avatar = new_avatar
            profile.bio = new_bio
            profile.address = new_address

            # saving changes
            profile.save()
            messages.success(request, 'Changes successfully saved!')
            return redirect('user_profile', username=request.user.username)
        messages.error(request, "Given data isn't valid")
        return redirect('update_profile')


class UserProfile(View):
    @staticmethod
    def get(request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(models.UserProfile, user=user)
        return render(request, 'blog/user_profile.html', {'profile': profile})


class DeleteUser(View):
    @staticmethod
    def get(request):
        user = request.user
        profile = models.UserProfile.objects.get(user=user)

        profile.delete()
        user.delete()

        messages.success(request, 'User has been deleted successfully!')
        return redirect('home')


class UserList(ListView):
    paginate_by = 10
    model = User
    template_name = 'blog/users.html'
    context_object_name = 'users'
    ordering = ['id']

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.User.objects.all()
        messages.error(self.request, 'You are not a staff user!')
        return User.objects.all()[:0]


class PasswordReset(View):
    @staticmethod
    def get(request):
        form = PasswordResetForm()
        return render(request=request, template_name='password/password_reset.html', context={'form': form})

    @staticmethod
    def post(request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = get_object_or_404(User, email=email)

            if user:
                subject = 'Password reset requested'
                email_temlpate_name = 'password/password_reset_email.txt'
                data = {
                    'email': user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Xtra Blog',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                message = render_to_string(email_temlpate_name, data)
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header')
                else:
                    return redirect('password_reset_done')
        messages.error(request, 'Invalid data')
        return redirect('password_reset')
