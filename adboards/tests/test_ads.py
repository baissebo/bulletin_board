import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from adboards.models import Ad, Review
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    return User.objects.create(
        email="test@mail.com",
        password="testpassword",
        role="user"
    )


@pytest.fixture
def create_admin(db):
    return User.objects.create(
        email="admin@mail.com",
        password="adminpassword",
        role="admin"
    )


@pytest.fixture
def create_ad(db, create_user):
    return Ad.objects.create(
        author=create_user,
        title="Объявление",
        description="Описание",
        price=100,
    )


@pytest.fixture
def admin_create_ad(db, create_admin):
    return Ad.objects.create(
        author=create_admin,
        title="Объявление админа",
        description="Описание админа",
        price=150,
    )


def test_user_create_ad(api_client, create_user):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:ad-list")
    data = {
        "author": create_user.id,
        "title": "Новое объявление",
        "description": "Новое описание для объявления",
        "price": 150
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Ad.objects.count() == 1
    assert Ad.objects.get().title == "Новое объявление"


def test_user_can_view_own_ad(api_client, create_user, create_ad):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:ad-detail", args=[create_ad.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == create_ad.title


def test_user_can_update_own_ad(api_client, create_user, create_ad):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:ad-detail", args=[create_ad.id])
    data = {
        "author": create_user.id,
        "title": "Обновленное объявление",
        "description": "Обновленное описание для объявления",
        "price": 200
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Ad.objects.get().title == "Обновленное объявление"


def test_user_can_delete_own_ad(api_client, create_user, create_ad):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:ad-detail", args=[create_ad.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


def test_user_cannot_delete_any_ad(api_client, create_user, admin_create_ad):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:ad-detail", args=[admin_create_ad.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.count() == 1


def test_admin_can_delete_any_ad(api_client, create_admin, create_ad):
    api_client.force_authenticate(user=create_admin)

    url = reverse("adboards:ad-detail", args=[create_ad.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


def test_user_can_create_review(api_client, create_user, create_ad):
    api_client.force_authenticate(user=create_user)

    url = reverse("adboards:review-list")
    data = {
        "author": create_user.id,
        "ad": create_ad.id,
        "text": "Новый отзыв",
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert Review.objects.get().text == "Новый отзыв"


def test_user_can_delete_review(api_client, create_user, create_ad):
    api_client.force_authenticate(user=create_user)
    review = Review.objects.create(author=create_user, ad=create_ad, text="Отзыв")

    response = api_client.delete(reverse("adboards:review-detail", kwargs={"pk": review.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


def test_admin_can_delete_any_review(api_client, create_admin, create_user, create_ad):
    api_client.force_authenticate(user=create_admin)
    review = Review.objects.create(author=create_user, ad=create_ad, text="Отзыв")

    response = api_client.delete(reverse("adboards:review-detail", kwargs={"pk": review.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_anonymous_user_can_view_ads(api_client):
    response = api_client.get(reverse("adboards:ad-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_user_cannot_create_ad(api_client):
    response = api_client.post(reverse("adboards:ad-list"), {
        "title": "Недоступное объявление",
        "description": "Это не должно пройти",
        "price": 1000
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_create_review(api_client, create_ad):
    response = api_client.post(reverse("adboards:review-list"), {
        "author": 1,
        "ad": create_ad.id,
        "text": "Новый отзыв о телефоне.",
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_view_review(api_client):
    response = api_client.get(reverse("adboards:review-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
