from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, password):
        if not email:
            raise ValueError('enter email')
        if not first_name:
            raise ValueError('enter first_name')
        if not last_name:
            raise ValueError('enter last_name')
        if not phone:
            raise ValueError('enter phone')
        user = self.model(email=self.normalize_email(email), phone=phone,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone, password):
        user = self.create_user(first_name, last_name, email, phone, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    # def normalize_phone_number(self, phone_number):
    #     return phone_number
