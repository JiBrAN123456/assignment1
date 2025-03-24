from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    
    def create_user(self, email , password=None, **extra_fields):
        if not email:
            raise ValueError("Email not Valid")
        
        email = self.normalize_email(email)
        user = self.model(email= email , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email , password = None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        return self.create_user(email , password , **extra_fields)
    

class User(AbstractUser):
     
    ROLE_CHOICES = [ 
        ('manager', "Manager"),
        ('user','User')
                     ]

    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length= 20 , unique=True , null=True , blank = True )
    role = models.CharField(max_length=20, choices= ROLE_CHOICES , default= 'user')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return f"{self.username} ({self.role}) "
    


class Task(models.Model):
    
    STATUS_CHOICES = [
        ("pending","Pending"),
        ("in_progress","In_Progress"),
        ("completed","Completed"),
    ]    



    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateField(null= True , blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default="pending")

    assigned_users = models.ManyToManyField(User, related_name="tasks")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name= "created_task")

    def __str__(self):
        return self.name