from django.urls import reverse
from rest_framework.test import APITestCase

from adboards.models import Ad, Review
from users.models import User


class AdReviewPermissionsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com", password="test", role="user"
        )
        self.admin = User.objects.create(
            email="admin@mail.com", password="admin", role="admin"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("adboards:ad-list")

        self.ad = Ad.objects.create(
            author=self.user,
            title="Продажа мобильного телефона",
            description="Мобильный телефон Samsung Galaxy S21 Ultra 5G",
            price=15000,
        )

        self.review = Review.objects.create(
            author=self.user,
            ad=self.ad,
            text="Отличный телефон! Очень довольны качеством и ценой.",
        )

    def test_user_can_create_ad(self):
        data = {
            "author": self.user.pk,
            "title": "Продажа ноутбука",
            "description": "Ноутбук Apple MacBook Pro 16",
            "price": 120000,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ad.objects.count(), 2)
        self.assertTrue(Ad.objects.filter(title="Продажа ноутбука").exists())

    def test_user_can_view_own_ad(self):
        response = self.client.get(reverse("adboards:ad-detail", kwargs={"pk": self.ad.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.ad.title)

    def test_user_can_update_own_ad(self):
        response = self.client.put(reverse("adboards:ad-detail", kwargs={"pk": self.ad.id}), {
            "author": self.user.pk,
            "title": "Обновленная продажа мобильного телефона",
            "description": "Новая версия мобильного телефона",
            "price": 16000,
        })
        self.assertEqual(response.status_code, 200)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Обновленная продажа мобильного телефона")

    def test_user_can_delete_own_ad(self):
        response = self.client.delete(reverse("adboards:ad-detail", kwargs={"pk": self.ad.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ad.objects.count(), 0)

    def test_admin_can_delete_any_ad(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("adboards:ad-detail", kwargs={"pk": self.ad.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ad.objects.count(), 0)

    def test_user_can_create_review(self):
        response = self.client.post(reverse("adboards:review-list"), {
            "author": self.user.pk,
            "ad": self.ad.id,
            "text": "Новый отзыв о телефоне.",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 2)

    def test_user_can_delete_own_review(self):
        response = self.client.delete(reverse("adboards:review-detail", kwargs={"pk": self.review.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Review.objects.count(), 0)

    def test_admin_can_delete_any_review(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("adboards:review-detail", kwargs={"pk": self.review.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Review.objects.count(), 0)

    def test_anonymous_user_can_view_ads(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_create_ad(self):
        self.client.logout()
        response = self.client.post(self.url, {
            "title": "Недоступное объявление",
            "description": "Это не должно пройти",
            "price": 1000
        })
        self.assertEqual(response.status_code,
                         403)

    def test_anonymous_user_cannot_create_review(self):
        self.client.logout()
        response = self.client.post(reverse("adboards:review-list"), {
            "author": self.user.pk,
            "ad": self.ad.id,
            "text": "Новый отзыв о телефоне.",
        })
        self.assertEqual(response.status_code,
                         403)

    def test_anonymous_user_cannot_view_review(self):
        self.client.logout()
        response = self.client.get(reverse("adboards:review-list"))
        self.assertEqual(response.status_code, 401)
