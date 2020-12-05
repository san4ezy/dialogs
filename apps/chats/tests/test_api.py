from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.chats.models import Dialog
from apps.users.tests.factories import UserFactory


class TestChats(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_dialog(self):
        friend = UserFactory()
        response = self.client.post(
            reverse('dialogs-list'),
            data={
                'user_id': friend.pk,
            },
            format='json',
        )
        assert response.status_code == 201
        dialog_id = response.data['id']
        dialog = Dialog.objects.get(pk=dialog_id)
        assert self.user.pk in dialog.users
        assert friend.pk in dialog.users

    def test_get_last_sent_dialogs(self):
        friends = UserFactory.create_batch(10)
        dialogs = []
        for friend in friends:
            dialog = Dialog.objects.create(users=[self.user.pk, friend.pk])
            dialog.send_message(sender=self.user, text=f"{self.user}'s message")
            dialog.send_message(sender=friend, text=f"{friend}'s message")
            dialogs.append(dialog)
        dialog = dialogs[5]  # 5 is like random dialog
        dialog.send_message(sender=self.user, text=f"One more {self.user}'s message")  # must be on the top
        dialogs[3].send_message(sender=friends[3], text=f"One more {friends[3]}'s message")  # mustn't be on the top
        response = self.client.get(f"{reverse('dialogs-list')}?last_sent=true")
        data = response.data['results']
        assert 200
        assert data[0]['id'] == dialog.pk

    def test_get_last_received_dialogs(self):
        friends = UserFactory.create_batch(10)
        dialogs = []
        for friend in friends:
            dialog = Dialog.objects.create(users=[self.user.pk, friend.pk])
            dialog.send_message(sender=friend, text=f"{friend}'s message")
            dialog.send_message(sender=self.user, text=f"{self.user}'s message")
            dialogs.append(dialog)
        dialog = dialogs[5]  # 5 is like random dialog
        dialog.send_message(sender=friends[3], text=f"One more {friends[3]}'s message")  # must be on the top
        dialogs[3].send_message(sender=self.user, text=f"One more {self.user}'s message")  # mustn't be on the top
        response = self.client.get(f"{reverse('dialogs-list')}?last_received=true")
        data = response.data['results']
        assert 200
        assert data[0]['id'] == dialog.pk
