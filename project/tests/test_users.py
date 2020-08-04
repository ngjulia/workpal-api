import json

import pytest

## CREATE ----------------------------------------------------------------------------------------->
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

def test_create_task(test_app_with_db):
  response = test_app_with_db.post(
    "/user/", data=json.dumps({"full_name": "Kevin", "email": "test@gmail.com","phone": "123-123-1234"})
  )
  user_id = response.json()["id"]
  response = test_app_with_db.post(
    f"/user/{user_id}/task/", data=json.dumps({"name": "Learn to code", "rank": 1, "completed": False, "completion_time": 0 })
  )
  assert response.status_code == 201
  assert response.json()["name"] == "Learn to code"
  assert response.json()["rank"] == 1
  assert response.json()["completed"] == False
  assert response.json()["completion_time"] == 0
  assert response.json()["user_id"] == user_id

def test_create_task_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
      "/user/", data=json.dumps({"full_name": "Kevin", "email": "test@gmail.com","phone": "123-123-1234"})
    )
    user_id = response.json()["id"]
    response = test_app_with_db.post(f"/user/{user_id}/task/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "payload", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "payload", "rank"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "payload", "completed"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "payload", "completion_time"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

## READ ----------------------------------------------------------------------------------------->
def test_read_user(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]d
    assert response_dict["created_at"]

