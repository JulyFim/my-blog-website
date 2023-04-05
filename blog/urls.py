from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    # base system logic
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogOutUser.as_view(), name='logout'),
    path('update_profile/', views.UpdateUserProfile.as_view(), name='update_profile'),
    path('user_profile/<str:username>/', views.UserProfile.as_view(), name='user_profile'),
    path('delete_profile/', views.DeleteUser.as_view(), name='delete_profile'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    # nav bar
    path('new_post/', views.NewPostView.as_view(), name='new_post'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact'),
    # filtering
    path('search', views.Search.as_view(), name='search'),
    path('post/<slug:slug>/', views.BlogDetail.as_view(), name='details'),
    path('category/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category_detail'),
]

if settings.DEBUG:
    """
    With that Django's development server is capable of serving media files.
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
