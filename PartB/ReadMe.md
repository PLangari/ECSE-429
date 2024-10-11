## 1) To run all tests with actual behaviour passing:
    `pytest -vk "not expected_behaviour_failing" --random-order`

## 2) To run only the tests where the expected behaviour fails:
    `pytest -vk "expected_behaviour_failing" --random-order`

### If you find bugs (actual behaviour != expected behaviour) mark the scenario step defintion with `@pytest.mark.expected_behaviour_failing`. This will not run the test when calling command 1) above. 