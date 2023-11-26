from app.main import app
from fastapi.testclient import TestClient
from app.Config import settings

client = TestClient(app)

REG_NO = settings.REG_NO
PASSWORD = settings.PASSWORD

AUTH_COOKIE = ""
PLACEMENT_AUTH_COOKIE = ""



# HEALTH ROUTE
def test_health_route():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert isinstance(resp.json()["app"], str)


#################################################
#
#                   USER ROUTES
#
#################################################


def test_login_user():
    response = client.post(
        "/api/v1/user/login", json={"reg_no": REG_NO, "password": PASSWORD}
    )
    assert response.status_code == 200
    assert isinstance(response.json()["cookie"], str)
    global AUTH_COOKIE
    AUTH_COOKIE = response.json()["cookie"]


def test_get_user_me():
    resp = client.post(
        "/api/v1/user/me",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["name"], str)


def test_get_user_messages():
    resp = client.post(
        "/api/v1/user/messages",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["messages"], list)


def test_get_user_syllabus():
    resp = client.post(
        "/api/v1/user/syllabus",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["course"], dict)


def test_get_user_announcements():
    resp = client.post(
        "/api/v1/annoucements",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["annoucements"], list)


def test_get_user_authorities():
    resp = client.post(
        "/api/v1/user/authorities",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["authorities"], list)


def test_get_user_attendance():
    resp = client.post(
        "/api/v1/user/attendance",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["summary"], list)


def test_get_user_assignments_marks():
    resp = client.post(
        "/api/v1/user/assignments",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["theory"], list)
    assert isinstance(resp.json()["practical"], list)


def test_get_user_pending_assignments():
    resp = client.post(
        "/api/v1/user/pending_assignments",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["assignments"], list)


def test_get_user_exams():
    resp = client.post(
        "/api/v1/user/exams",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["exams"], list)


def test_get_user_cgpa():
    resp = client.post(
        "/api/v1/user/cgpa",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["cgpa"], dict)


def test_get_user_marks():
    resp = client.post(
        "/api/v1/user/marks",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["cookie"], str)


#################################################
#
#                 TIMETABLE ROUTES
#
#################################################


def test_makeup_class():
    resp = client.post(
        "/api/v1/timetable/makeup",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["makeup"], list)


def test_timetable():
    resp = client.post(
        "/api/v1/timetable/classes",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["time_table"], dict)


def test_timetable_today():
    resp = client.post(
        "/api/v1/timetable/today",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["today_time_table"], list)


#################################################
#
#                   MISC ROUTES
#
#################################################


def test_todays_drives():
    resp = client.post(
        "/api/v1/misc/drives",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["drives"], list)


def test_search_user_on_lpu():
    resp = client.get(
        "api/v1/misc/search_user?id=Ranit Naha",  # api/v1/misc/search_user?id=reg_no
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["users"], list)


#################################################
#
#                   HOSTEL ROUTES
#
#################################################


def test_hostel_details_with_electricity():
    resp = client.post(
        "/api/v1/hostel/",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json()["user_details"], dict)


def test_hostel_leave_slip():
    resp = client.post(
        "/api/v1/hostel/leave_slip",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": AUTH_COOKIE},
    )
    assert isinstance(resp.json()["cookie"], str)


#################################################
#
#                   PLACEMENT ROUTES
#
#################################################


def test_placement_login():
    resp = client.post(
        "/api/v1/placement/login",
        json={"reg_no": REG_NO, "password": PASSWORD},
    )
    assert isinstance(resp.json()["cookie"], str)
    global PLACEMENT_AUTH_COOKIE
    PLACEMENT_AUTH_COOKIE = resp.json()["cookie"]


def test_user_details():
    resp = client.post(
        "/api/v1/placement/",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": PLACEMENT_AUTH_COOKIE},
    )
    assert isinstance(resp.json()["registration_number"], str)


def test_drives_details():
    resp = client.post(
        "/api/v1/placement/drives",
        json={"reg_no": REG_NO, "password": PASSWORD, "cookie": PLACEMENT_AUTH_COOKIE},
    )
    assert isinstance(resp.json()["drive_details"], list)
