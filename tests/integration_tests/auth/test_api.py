import pytest


@pytest.mark.parametrize(
    "email, password, status_code", [("kot0_@pes.com", "1234", 200), ("kot1_@pes.com", "1234", 200)]
)
async def test_auth(ac, email, password, status_code):
    # email = 'kot_@pes.com'
    # password = '1234'
    resp_reg = await ac.post("/auth/register", json={"email": email, "password": password})
    assert resp_reg.status_code == status_code
    if status_code != 200:
        return

    resp_login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # me
    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == status_code
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # logout
    await ac.post("/auth/logout")
    assert "access_token" not in ac.cookies
