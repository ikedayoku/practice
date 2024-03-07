from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings    # あとで使います。

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'    # デフォルトは名前入力、今回はメールアドレスにカスタム

class Post(models.Model):
    """Post object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """Comment object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

# import hashlib
from datetime import timedelta
from django.utils import timezone

def in_30_days():
    return timezone.now() + timedelta(days=30)

# class AccessToken(models.Model):
#     # ひもづくユーザー
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # アクセストークン(max_lengthが40に設定されている理由は、トークンはsha1でハッシュ化した文字列を設定するため)
#     token = models.CharField(max_length=40)
#     # アクセス日時
#     access_datetime = models.DateTimeField(default=in_30_days)

#     def str(self):
#         # メールアドレスとアクセス日時、トークンが見えるように設定
#         dt = timezone.localtime(self.access_datetime).strftime("%Y/%m/%d %H:%M:%S")
#         return self.user.user_id + '(' + dt + ') - ' + self.token

#     @staticmethod
#     def create(user: User):
#         # ユーザの既存のトークンを取得
#         if AccessToken.objects.filter(user=user).exists():
#             # トークンがすでに存在している場合は削除
#             AccessToken.objects.get(user=user).delete()

#         # トークン作成（UserID + Password + システム日付のハッシュ値とする）
#         dt = timezone.now()
#         str = user.user_id + user.password + dt.strftime('%Y%m%d%H%M%S%f')
#         hash = hashlib.sha1(str.encode('utf-8')).hexdigest()

#         # トークンをDBに追加
#         token = AccessToken.objects.create(
#             user=user,
#             token=hash,
#             access_datetime=dt)

#         return token