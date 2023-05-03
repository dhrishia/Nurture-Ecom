from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','Karnataka'),
    ('AndraPradesh','AndraPradesh')
)
DIST_CHOICES = {
    ('Kannur','Kannur'),
    ('Kozhikkode','Kozhikkode'),
    ('Ernakulam','Ernakulam'),
    ('Thiruvananthapuram','Thiruvananthapuram'),
    ('Banglore','Banglore'),
    ('Hubli','Hubli'),
    ('Hydrabad','Hydrabad'),
    ('Coimbator','Coimbator'),
    ('Madurai','Madurai'),
}

    

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pic', default='profile_pic/default.jpg')
    is_email_verified = models.BooleanField(default=False)
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contains didgits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, null=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)
    district = models.CharField(choices=DIST_CHOICES,max_length=20, null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=20, null=True)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    

class Address(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    full_name = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.CharField(max_length=50)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.CharField(max_length=50)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    house_name = models.CharField(max_length=150)
    address_line_1 = models.CharField(max_length=255,  default=0)
    address_line_2 = models.CharField(max_length=255, blank=True,  default=0)
    delivery_instruction = models.CharField(max_length=150)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)

 
 
    class Meta:
        verbose_name='Address'
        verbose_name_plural='Addresses'

    def __str__(self):
        return self.house_name