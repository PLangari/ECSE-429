## To run all tests with actual behaviour passing:
    `pytest -vk "not expected_behaviour_failing" --random-order`

## To run only the tests where the expected behaviour fails:
    `pytest -vk "expected_behaviour_failing" --random-order`

## To run only the tests where the actual behaviour is not what is expected:
    `pytest -vk "actual_behaviour_passing" --random-order`

- The three commands above will run the test to see if the server is running first and the last test will be the shutdown endpoint to kll the server. The tests ran in between are in random order. After every test, run make sure to restart the server

## To test only if the application is running:
    `pytest -vk "check_application_running"`

## To test only if the application is shutdown:
    `pytest -vk "check_application_shutdown"`