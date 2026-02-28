from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import signup, my_profile, update_profile, LoginView, CheckEmailAPIView,ResetPasswordAPIView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', my_profile, name='my-profile'),
    path('me/update/', update_profile, name='update-profile'),
    path("check-email/", CheckEmailAPIView.as_view(), name="check-email"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
] 

