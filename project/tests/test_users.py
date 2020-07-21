import json

import pytest

def test_create_user(test_app_with_db):
  response = test_app_with_db.post(
    "/user/", data=json.dumps({"full_name": "Kevin", "email": "test@gmail.com","phone": "123-123-1234"})
  )
  assert response.status_code == 201
  assert response.json()["full_name"] == "Kevin"
  assert response.json()["email"] == "test@gmail.com"
  assert response.json()["phone"] == "123-123-1234"
  assert response.json()["tasks"] == []

def test_create_user_invalid_json(test_app):
    response = test_app.post("/user/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "payload", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "payload", "phone"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
