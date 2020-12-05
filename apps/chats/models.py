from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max, Q
from django_extensions.db.models import TimeStampedModel

from apps.users.models import User


class DialogQuerySet(models.QuerySet):
    def last_sent(self, user: User, order: str = '-last_sent'):
        return (self
                .prefetch_related('messages')
                .annotate(last_sent=Max('messages__created', filter=Q(messages__sender=user)))
                .order_by(order)
                )

    def last_received(self, user: User, order: str = '-last_received'):
        return (self
                .prefetch_related('messages')
                .annotate(last_received=Max('messages__created', filter=~Q(messages__sender=user)))
                .order_by(order)
                )


class DialogManager(models.Manager):
    def get_queryset(self):
        return DialogQuerySet(self.model, using=self._db)

    def last_sent(self, user: User):
        return self.get_queryset().last_sent(user)

    def last_received(self, user: User):
        return self.get_queryset().last_received(user)


class Dialog(TimeStampedModel):
    users = ArrayField(models.IntegerField(), size=2, unique=True)

    objects = DialogManager()

    def __str__(self):
        return f"Dialog of {self.users}"

    def save(self, *args, **kwargs):
        self.users = sorted(self.users)
        return super().save(*args, **kwargs)

    @property
    def participants(self):
        return User.objects.filter(pk__in=self.users)

    @property
    def is_favorite(self):
        return self.favoritedialog_set.exists()

    def add_to_favorite(self, user: User):
        obj, c = FavoriteDialog.objects.get_or_create(dialog=self, user=user)
        return c

    def send_message(self, sender: User, text: str):
        return self.messages.create(sender=sender, dialog=self, text=text)


class FavoriteDialog(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorite_dialogs')
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)


class Message(TimeStampedModel):
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='sent_messages')
    is_read = models.BooleanField(default=False)  # must be moved to an additional model for using with group chats
    text = models.TextField()
    dialog = models.ForeignKey(Dialog, models.PROTECT, related_name='messages')

    def __str__(self):
        return f"{self.sender}'s message to {self.dialog}"

    def mark_as_read(self) -> None:
        (self.dialog.messages
         .filter(created__lte=self.created)
         .update(is_read=True)
         )
