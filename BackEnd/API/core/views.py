from django.http import HttpResponseRedirect
from django.db.models import Q, FilteredRelation
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

# project
from .models import Manager, Plan, SubscribedPlan, Transaction
from .serializers import PlanSerilizer, SubscribedPlanSerializer, UserSerilizer
from .paytm import generate_checksum, verify_checksum
from .serializers import MyTokenObtainPairSerializer

# authentications & permissions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from datetime import date as datep

# def load_data(apps, schema_editor):
#     Plan = apps.get_model("core", "Plan")

#     Plan(
#         plan_price=300,
#         name="Short Term Plan",
#         monthly_plan_duration=3,
#     ).save()
#     Plan(
#         plan_price=600,
#         name="Mid Term Plan",
#         monthly_plan_duration=6,
#     ).save()
#     Plan(
#         plan_price=900,
#         name="Long Term Plan",
#         monthly_plan_duration=9,
#     ).save()


class UserView(generics.CreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = UserSerilizer


class PlanView(generics.CreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerilizer
    # permission_classes = (IsAdminUser,)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class SubView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        user_id = request.data["user_id"]
        # outer join for fetching all plans (including subscribed plan)
        queryset = Plan.objects.annotate(
            sub=FilteredRelation(
                "subscribedplan", condition=Q(subscribedplan__subscribeduser=user_id)
            )
        ).values("name", "plan_price", "sub__is_active", "id", "sub__is_subscribed")
        for i in queryset:
            if i["sub__is_active"] == None:
                i["sub__is_active"] = False

            if i["sub__is_subscribed"] == None:
                i["sub__is_subscribed"] = False

        return Response({"data": queryset})


class ActivatePlanView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        amount = request.data["amount"]
        userid = request.data["user_id"]
        user = Manager.objects.get(pk=userid)
        # saving client ip for redirecting purpose
        ip = request.META.get("HTTP_ORIGIN")

        transaction = Transaction.objects.create(made_by=user, amount=amount, ip=ip)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
            ("MID", settings.PAYTM_MERCHANT_ID),
            ("ORDER_ID", str(transaction.order_id)),
            ("CUST_ID", str(transaction.made_by.email)),
            ("TXN_AMOUNT", str(transaction.amount)),
            ("CHANNEL_ID", settings.PAYTM_CHANNEL_ID),
            ("WEBSITE", settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ("INDUSTRY_TYPE_ID", settings.PAYTM_INDUSTRY_TYPE_ID),
            ("CALLBACK_URL", "http://127.0.0.1:8000/api/callback"),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params["CHECKSUMHASH"] = checksum
        print("SENT: ", checksum)

        return render(request, "payments/redirect.html", context=paytm_params)


class CancelOrViewPlanView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.data["user_id"]
        user = Manager.objects.get(id=user_id)
        subplan = SubscribedPlan.objects.get(subscribeduser=user)
        subplan.is_active = not (subplan.is_active)
        try:
            subplan.save()
            return Response({"data": "subplan"})
        except Exception:
            return Response(Exception)


class CallbackView(APIView):
    def post(self, request):
        paytm_checksum = ""
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data["CHECKSUMHASH"][0]
        for key, value in received_data.items():
            if key == "CHECKSUMHASH":
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(
            paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum)
        )

        # fetching transation info
        orderId = received_data["ORDERID"][0]
        tranx = Transaction.objects.get(order_id=orderId)
        amount = str(tranx.amount)
        redirect_url = tranx.ip + "/"
        try:
            if is_valid_checksum:
                print("Checksum Matched")
                received_data["message"] = "Checksum Matched"
                if received_data["STATUS"][0] == "TXN_SUCCESS":
                    plan = Plan.objects.get(plan_price=amount)
                    # on success creating new subplan
                    subPlan = SubscribedPlan.objects.create(
                        subscribeduser=tranx.made_by,
                        is_active=True,
                        is_subscribed=True,
                        plan=plan,
                        # subscribed_date="2010-11-30",
                        subscribed_date=datep.today().strftime("%Y-%m-%d"),
                    )
                    return HttpResponseRedirect(
                        redirect_to=redirect_url + "success/" + orderId + "/" + amount
                    )
                else:
                    # on failed redirecting to fail page of frontend
                    return HttpResponseRedirect(
                        redirect_to=redirect_url + "fail/" + orderId + "/" + amount
                    )
            else:
                print("Checksum Mismatched")
                received_data["message"] = "Checksum Mismatched"
                return HttpResponseRedirect(
                    redirect_to=redirect_url + "fail/" + orderId + "/" + amount
                )
        except Exception:
            print(Exception)
            return HttpResponseRedirect(
                redirect_to=redirect_url + "fail/" + orderId + "/" + amount
            )


class DeactivatePlanView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.data["user_id"]
        user = Manager.objects.get(id=user_id)
        subplan = SubscribedPlan.objects.get(subscribeduser=user)
        subplan.delete()
        return Response(status=204)
