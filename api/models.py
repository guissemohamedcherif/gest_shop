from django.db import models
import uuid
from backend import settings
from django.db.models import CheckConstraint, Q
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here.

ADMIN = 'admin'
SUPERADMIN = 'superadmin'
CLIENT = 'client'
VENDEUR = 'vendeur'

USER_TYPES = (
    (CLIENT, CLIENT),
    (VENDEUR, VENDEUR),
    (ADMIN, ADMIN),
    (SUPERADMIN, SUPERADMIN),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', SUPERADMIN)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    prenom = models.CharField(max_length=500, blank=True, null=True)
    nom = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20 ,null=True, blank=True)
    adress = models.TextField(null=True,blank=True)
    date_de_naissance = models.DateField(null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default=CLIENT)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # these field are required on registering
    REQUIRED_FIELDS = ['prenom', 'nom']
    
    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        app_label = "api"

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'<User: {self.pk}, email: {self.email}, user_type: {self.user_type}>'


class Categorie(models.Model):
    slug = models.SlugField(default=uuid.uuid1, max_length=1000, unique=True)
    nom = models.CharField("Nom Categorie", max_length=255)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="categories",
                               null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'<Categorie: {self.pk}, nom: {self.nom}>'
    
    def create(self, validated_data):
        parent_id = validated_data.get('parent', None)
        instance = Categorie(**validated_data)

        if parent_id is not None and parent_id == instance.id:
            instance.parent = None

        instance.save()
        return instance
    
    def update(self, validated_data):
        parent_id = validated_data.get('parent', None)
        instance = Categorie(**validated_data)

        instance.save()
        return instance


class Article(models.Model):
    slug = models.SlugField(default=uuid.uuid1, max_length=1000, unique=True)
    nom = models.CharField("Nom Article", max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    quantite = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'<Article: {self.pk}, nom: {self.nom}, prix: {self.prix}>'


class DetailVente(models.Model):
    slug = models.SlugField(default=uuid.uuid1, unique=True)
    quantite = models.PositiveIntegerField(default=0)
    prix = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="details")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DetailVente {self.id} - Article {self.article.nom} - Quantite: {self.quantite}"


class Vente(models.Model):
    slug = models.SlugField(default=uuid.uuid1, unique=True)
    reference = models.CharField(max_length=250)
    quantite = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    details = models.ManyToManyField(DetailVente, related_name="ventes", default=[])
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)