from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


class Category(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post'
    )
    main_text = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='post'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='post'
    )

    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()

    comment_text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return "Comment {} by {}".format(self.comment_text, self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userprofile'
    )
    avatar = models.ImageField(
        upload_to='users/avatars/', null=True, blank=True
    )
    bio = models.TextField(null=True, blank=True)
    address = models.TextField(default="Address isn't given.", blank=True)

    created_on = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"@{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# @receiver(pre_delete, sender=User)
# def remove_profile(sender, instance, **kwargs):
#     if instance:
#         profile = UserProfile.objects.get(user=instance)
#         user = profile.user
#         user.delete()
