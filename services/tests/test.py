import pytest
from django.urls import reverse
from services.models import Service

pytestmark = pytest.mark.django_db


class TestServiceEndpoints:
    def test_list_services_returns_only_active_services(self, api_client):
        s1 = Service.objects.create(title="Cleaning", service_type=Service.Type.CLEANING, is_active=True, base_duration_minutes=60)
        Service.objects.create(title="Old Service", service_type=Service.Type.OTHER, is_active=False, base_duration_minutes=60)

        res = api_client.get(reverse("service-list"))
        assert res.status_code == 200
        data = res.json()
        items = data["results"] if isinstance(data, dict) and "results" in data else data

        assert len(items) == 1
        assert items[0]["id"] == s1.id

    def test_retrieve_single_service(self, api_client):
        s1 = Service.objects.create(title="Moving", service_type=Service.Type.MOVING, is_active=True, base_duration_minutes=90)

        res = api_client.get(reverse("service-detail", kwargs={"pk": s1.id}))
        assert res.status_code == 200
        body = res.json()
        assert body["id"] == s1.id
        assert "service_type_display" in body

    def test_create_service_not_allowed(self, api_client):
        res = api_client.post(reverse("service-list"), data={"title": "X"}, format="json")
        assert res.status_code in (401, 403, 405)
