from django.urls.conf import path
from .views import (
    CancelOrViewPlanView,
    DeactivatePlanView,
    CallbackView,
    PlanView,
    SubView,
    UserView,
    MyObtainTokenPairView,
    ActivatePlanView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("login", MyObtainTokenPairView.as_view(), name="token_obtain_view"),
    path("signup", UserView.as_view()),
    path("nplan", PlanView.as_view()),
    path("plan", SubView.as_view()),
    path("activate", ActivatePlanView.as_view()),
    path("callback", CallbackView.as_view()),
    path("cancelOrResumePlan", CancelOrViewPlanView.as_view()),
    path("deactivate", DeactivatePlanView.as_view()),
    path("verifytoken", TokenVerifyView.as_view()),
]
