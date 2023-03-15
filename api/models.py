from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.timezone import localdate, localtime

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = localtime
        self.save(update_fields=['deleted_at'])

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, name, email, password, **extra_fields):
        if not id:
            raise ValueError('Users require an id field')
        if not name:
            raise ValueError('Users require a name field')
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(id=id, name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, name, email, password=None, **extra_fields):
        return self._create_user(id, name, email, password, **extra_fields)

    def create_superuser(self, id, name, email, password, **extra_fields):
        user = self.create_user(
            id=id,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'name', ]

    def __str__(self):
        return self.name


class Group(BaseModel):
    group_num = models.IntegerField()  # 같은 그룹 구분용(id와 별도)
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)


class Trip(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    departing_date = models.DateField(default=localdate)
    arriving_date = models.DateField(default=localdate)
    thumbnail = models.TextField(null=True)


class Expense(models.Model):
    CATEGORY_CHOICES = {
        ('room', '숙소'),
        ('airline', '항공'),
        ('traffic', '교통'),
        ('food', '식비'),
        ('shopping', '쇼핑'),
        ('tourism', '관광'),
        ('etc', '기타')
    }
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    expense_num = models.IntegerField()  # participant 때문에 여러 번 저장하게 되는데 어떤게 같은 결제 내역인지 구분용
    payer = models.ForeignKey(User, related_name='payer', on_delete=models.CASCADE)
    participant = models.ForeignKey(User, related_name='participant', on_delete=models.CASCADE)
    payment = models.IntegerField()
    payed_at = models.DateField(null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=True)


class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    url = models.TextField()
    category_custom = models.CharField(null=True, max_length=20)
    category_cv = models.CharField(default="0", max_length=30)
    taken_at = models.DateTimeField(null=True)

