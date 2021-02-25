from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin

# create user
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create(
        self, email, first_name, last_name, company, address, DOB, password=None
    ):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        print("create user called")
        user.first_name = first_name
        user.last_name = last_name
        user.company = company
        user.address = address
        user.DOB = DOB
        user.set_password(password)  # change password to hash
        user.is_superuser = False
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Manager(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=30)
    last_name = models.CharField("last name", max_length=30)
    DOB = models.DateField(null=True)
    address = models.CharField(max_length=300, null=True)
    company = models.CharField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.email)


class Plan(models.Model):
    name = models.CharField(max_length=100)
    monthly_plan_duration = models.IntegerField()
    plan_price = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class SubscribedPlan(models.Model):
    subscribeduser = models.OneToOneField(Manager, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    subscribed_date = models.DateField(null=True)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.subscribeduser} has {self.plan}"


class Transaction(models.Model):
    made_by = models.ForeignKey(
        get_user_model(), related_name="transactions", on_delete=models.CASCADE
    )
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    ip = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime("PAY2ME%Y%m%dODR") + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.order_id} with {self.amount} from {self.ip}"
