import requests
from utils.default_variables import DEFAULT_API_URL

# Test to check if the application is running
def test_is_application_running():
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200, "Application is not currently running. Please start the application before running the tests."

# Test to check if the application is shutdown
def test_is_application_shutdown():
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200, "Application has already been shutdown."
    try:
        response = requests.get(f'{DEFAULT_API_URL}/shutdown"')
    except requests.exceptions.ConnectionError:
        assert True
