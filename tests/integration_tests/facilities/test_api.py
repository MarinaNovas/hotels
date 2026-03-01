async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    isinstance(response.json(), list)


async def test_post_facilities(ac):
    facility_title = "тайский массаж"
    response = await ac.post("/facilities", json={"title": facility_title})
    assert response.status_code == 200
    res = response.json()
    print(f"{res=}")
    assert isinstance(res, dict)
    assert res["result"]["title"] == facility_title
    assert "result" in res
