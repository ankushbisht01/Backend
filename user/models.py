from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email = self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
    




class User(AbstractUser):
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    username  = None 

    #change the default BaseUserManager with our custom one
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




class Tour(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    image1 = models.URLField(max_length=200, null=True, blank=True)
    image2 = models.URLField(max_length=200, null=True, blank=True)
    dayDescription = models.TextField( null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.title
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.name + " " + self.tour.title + " " + str(self.rating)
    

    
class ChatMessage(models.Model):
    content = models.TextField()
    sender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField( null=True, blank=True)
    time = models.TimeField(null = True, blank=True)
    numberOfPeople = models.IntegerField()
    totalPrice = models.IntegerField()
    def __str__(self):
        return self.user.name + " " + self.tour.title + " " + str(self.date) + " " + str(self.time) + " " + str(self.numberOfPeople) + " " + str(self.totalPrice)


class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + " " + self.tour.title + " " + str(self.created_at)