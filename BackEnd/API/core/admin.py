from django.contrib import admin
from .models import Manager, Plan, SubscribedPlan, Transaction

admin.site.register(Manager)
admin.site.register(Plan)
admin.site.register(SubscribedPlan)
admin.site.register(Transaction)
