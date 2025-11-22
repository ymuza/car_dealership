import pytest
from unittest.mock import AsyncMock
from types import SimpleNamespace

# A valid vehicle response matching VehicleBase / Vehicle
VALID_VEHICLE = {
    "vehicle_id": 1,
    "vin": "1HGBH41JXMN109186",
    "make_id": 10,
    "model": "Corolla",
    "type_id": 3,
    "year": 2020,
    "color": "Blue",
    "mileage": 20000,
    "is_new": False,
    "price": 15000.0,
    "status": "available",
    "image_url": "/images/car.png",
    "created_at": None,
    "updated_at": None
}

VALID_VEHICLE_BASE = {
    k: v for k, v in VALID_VEHICLE.items()
    if k != "vehicle_id"
}


# ------------------------
#  GET /Vehicles/vehicles
# ------------------------
@pytest.mark.asyncio
async def test_get_vehicles(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_service.return_value.get_vehicles = AsyncMock(
        return_value=[VALID_VEHICLE]
    )

    response = await test_client.get("/Vehicles/vehicles")

    assert response.status_code == 200

    data = response.json()[0]

    # Field-by-field comparison
    for key, value in VALID_VEHICLE_BASE.items():
        if key in ("created_at", "updated_at"):  # FastAPI alters timestamp formatting
            continue
        assert data[key] == value



# ------------------------
#  GET /Vehicles/search
# ------------------------
@pytest.mark.asyncio
async def test_search_vehicles(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_service.return_value.search_vehicles.return_value = [VALID_VEHICLE]

    response = await test_client.get("/Vehicles/search?model=Corolla")

    assert response.status_code == 200
    data = response.json()[0]
    for key, value in VALID_VEHICLE.items():
        if key not in ("created_at", "updated_at"):
            assert data[key] == value


# ------------------------
# POST /Vehicles/vehicles
# ------------------------

@pytest.mark.asyncio
async def test_add_vehicle(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_vehicle_obj = SimpleNamespace(**VALID_VEHICLE)
    mock_service.return_value.add_vehicle.return_value = mock_vehicle_obj

    payload = {
        "vin": "1HGBH41JXMN109186",
        "make_id": 10,
        "model": "Corolla",
        "type_id": 3,
        "year": 2020,
        "color": "Blue",
        "mileage": 20000,
        "is_new": False,
        "price": 15000.0,
        "status": "available",
    }

    response = await test_client.post("/Vehicles/vehicles", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["vehicle_id"] == VALID_VEHICLE["vehicle_id"]

# ------------------------
# PATCH /Vehicles/vehicles/{id}
# ------------------------
@pytest.mark.asyncio
async def test_update_vehicle_image(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    updated = VALID_VEHICLE.copy()
    updated["image_url"] = "/images/updated.png"

    mock_service.return_value.update_vehicle = AsyncMock(return_value=updated)

    payload = {"image_url": "/images/updated.png"}

    response = await test_client.patch("/Vehicles/vehicles/1", json=payload)

    assert response.status_code == 200
    assert response.json()["image_url"] == "/images/updated.png"


@pytest.mark.asyncio
async def test_update_vehicle_not_found(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_service.return_value.update_vehicle = AsyncMock(return_value=None)

    response = await test_client.patch("/Vehicles/vehicles/999", json={"image_url": "x"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


# ------------------------
# DELETE /Vehicles/vehicles/{id}
# ------------------------
@pytest.mark.asyncio
async def test_delete_vehicle(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_service.return_value.remove_vehicle = AsyncMock(return_value=True)

    response = await test_client.delete("/Vehicles/vehicles/1")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_vehicle_not_found(test_client, mocker):
    mock_service = mocker.patch("app.routers.vehicle_router.VehicleService")

    mock_service.return_value.remove_vehicle = AsyncMock(return_value=False)

    response = await test_client.delete("/Vehicles/vehicles/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
