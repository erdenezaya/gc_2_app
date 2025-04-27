def test_login_success_sets_session(client, make_user):
    make_user()  # create Alice once
    resp = client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        follow_redirects=True,
    )
    assert b"Logged in successfully" in resp.data
    # Flask-Login sets _user_id cookie -> ensure we’re considered authenticated
    with client.session_transaction() as sess:
        assert "_user_id" in sess


def test_login_wrong_password(client, make_user):
    make_user()
    resp = client.post(
        "/login",
        data={"username": "alice", "password": "badpass"},
        follow_redirects=True,
    )
    assert b"Invalid" in resp.data
    with client.session_transaction() as sess:
        assert "_user_id" not in sess


def test_logout_clears_session(client, make_user):
    make_user()
    # first log in
    client.post("/login", data={"username": "alice", "password": "secret"})
    # then log out
    client.get("/logout", follow_redirects=True)
    with client.session_transaction() as sess:
        assert "_user_id" not in sess
