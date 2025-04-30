import pytest
from flask import session

def test_login_success_sets_session(client, make_user):
    make_user(username="alice", password="secret")
    client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        follow_redirects=True,
    )
    # Don’t check the flash text—just ensure the user is logged in
    with client.session_transaction() as sess:
        assert "_user_id" in sess

def test_login_wrong_password(client, make_user):
    make_user(username="alice", password="secret")
    resp = client.post(
        "/login",
        data={"username": "alice", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert b"Invalid" in resp.data or b"not registered" in resp.data
    with client.session_transaction() as sess:
        assert "_user_id" not in sess

def test_login_unregistered_user(client):
    resp = client.post(
        "/login",
        data={"username": "ghost", "password": "whatever"},
        follow_redirects=True,
    )
    assert b"not registered" in resp.data or b"Invalid" in resp.data
    with client.session_transaction() as sess:
        assert "_user_id" not in sess

def test_logout_clears_session(client, make_user):
    make_user(username="alice", password="secret")
    client.post("/login", data={"username": "alice", "password": "secret"})
    client.get("/logout", follow_redirects=True)
    with client.session_transaction() as sess:
        assert "_user_id" not in sess
