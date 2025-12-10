from fastapi import status

VALID_PHONE = "+78005553535"
ANOTHER_PHONE = "+78007005050"
VALID_ADDRESS = "Москва, ул. Ленина 1"
NEW_ADDRESS = "Москва, ул. Ленина 20"
INVALID_ADDRESS = "Надым, ул"
INVALID_PHONE = "112"


class TestContactAPI:

    def test_create_contact_success(self, client, fake_repo):
        payload = {"phone": VALID_PHONE, "address": VALID_ADDRESS}
        response = client.post("/api/v1/contacts/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["phone"] == VALID_PHONE
        assert data["address"] == VALID_ADDRESS

        assert fake_repo.store[VALID_PHONE] == VALID_ADDRESS

    def test_create_contact_duplicate(self, client):
        payload = {"phone": VALID_PHONE, "address": VALID_ADDRESS}
        client.post("/api/v1/contacts/", json=payload)

        response = client.post("/api/v1/contacts/", json=payload)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Контакт уже существует"

    def test_create_validation_error(self, client):
        payload = {"phone": VALID_PHONE, "address": INVALID_ADDRESS}
        response = client.post("/api/v1/contacts/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        payload = {"phone": INVALID_PHONE, "address": VALID_ADDRESS}
        response = client.post("/api/v1/contacts/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_get_contact_success(self, client):
        client.post(
            "/api/v1/contacts/", json={"phone": VALID_PHONE, "address": VALID_ADDRESS}
        )

        response = client.get(f"/api/v1/contacts/{VALID_PHONE}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["address"] == VALID_ADDRESS

    def test_get_contact_not_found(self, client):
        response = client.get(f"/api/v1/contacts/{ANOTHER_PHONE}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Контакт не найден"

    def test_update_contact_success(self, client, fake_repo):
        client.post(
            "/api/v1/contacts/", json={"phone": VALID_PHONE, "address": VALID_ADDRESS}
        )

        update_payload = {"address": NEW_ADDRESS}
        response = client.put(f"/api/v1/contacts/{VALID_PHONE}", json=update_payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["address"] == NEW_ADDRESS

        assert fake_repo.store[VALID_PHONE] == NEW_ADDRESS

    def test_update_contact_not_found(self, client):
        update_payload = {"address": NEW_ADDRESS}
        response = client.put(f"/api/v1/contacts/{ANOTHER_PHONE}", json=update_payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_contact_success(self, client, fake_repo):

        client.post(
            "/api/v1/contacts/", json={"phone": VALID_PHONE, "address": VALID_ADDRESS}
        )

        response = client.delete(f"/api/v1/contacts/{VALID_PHONE}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert VALID_PHONE not in fake_repo.store

        get_resp = client.get(f"/api/v1/contacts/{VALID_PHONE}")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_contact_not_found(self, client):
        response = client.delete(f"/api/v1/contacts/{ANOTHER_PHONE}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
