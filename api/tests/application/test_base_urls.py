from http import HTTPStatus


def test_root(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK


def test_status(client):
    response = client.get("/status")

    assert response.status_code == HTTPStatus.OK
