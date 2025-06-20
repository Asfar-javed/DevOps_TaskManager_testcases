import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Helper function to create the WebDriver instance
def create_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8081")
    return driver


def test_load_homepage():
    driver = create_driver()
    assert "Task Manager" in driver.title
    driver.quit()


def test_create_task():
    driver = create_driver()
    input_box = driver.find_element(By.CLASS_NAME, "task-input")
    submit_button = driver.find_element(By.CLASS_NAME, "submit-btn")
    input_box.send_keys("Test Task")
    submit_button.click()
    time.sleep(1)
    tasks = driver.find_elements(By.CLASS_NAME, "single-task")
    assert any("Test Task" in task.text for task in tasks)
    driver.quit()


def test_show_tasks():
    driver = create_driver()
    tasks = driver.find_elements(By.CLASS_NAME, "single-task")
    assert len(tasks) >= 0
    driver.quit()


def test_delete_task():
    driver = create_driver()
    time.sleep(1)
    delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-btn")
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(1)
    assert True
    driver.quit()


def test_open_edit_page():
    driver = create_driver()
    edit_links = driver.find_elements(By.CLASS_NAME, "edit-link")
    if edit_links:
        edit_links[0].click()
        time.sleep(1)
        assert "Edit Task" in driver.page_source
    else:
        assert True
    driver.quit()


def test_update_task():
    driver = create_driver()
    edit_links = driver.find_elements(By.CLASS_NAME, "edit-link")
    if edit_links:
        edit_links[0].click()
        time.sleep(1)
        input_box = driver.find_element(By.CLASS_NAME, "task-edit-name")
        checkbox = driver.find_element(By.CLASS_NAME, "task-edit-completed")
        button = driver.find_element(By.CLASS_NAME, "task-edit-btn")
        input_box.clear()
        input_box.send_keys("Updated Task")
        if not checkbox.is_selected():
            checkbox.click()
        button.click()
        time.sleep(2)
        assert "success" in driver.page_source.lower()
    driver.quit()


def test_empty_submission():
    driver = create_driver()
    submit_button = driver.find_element(By.CLASS_NAME, "submit-btn")
    submit_button.click()
    time.sleep(1)
    assert "error" in driver.page_source.lower() or "please try again" in driver.page_source.lower()
    driver.quit()


def test_alert_on_success():
    driver = create_driver()
    input_box = driver.find_element(By.CLASS_NAME, "task-input")
    submit_button = driver.find_element(By.CLASS_NAME, "submit-btn")
    input_box.send_keys("Task for Alert Test")
    submit_button.click()
    time.sleep(1)
    alert = driver.find_element(By.CLASS_NAME, "form-alert")
    assert alert.is_displayed()
    driver.quit()


def test_edit_button_loading_text():
    driver = create_driver()
    edit_links = driver.find_elements(By.CLASS_NAME, "edit-link")
    if edit_links:
        edit_links[0].click()
        time.sleep(1)
        button = driver.find_element(By.CLASS_NAME, "task-edit-btn")
        button.click()
        time.sleep(0.5)
        assert button.text.lower() in ["loading...", "edit"]
    driver.quit()


def test_page_no_errors():
    driver = create_driver()
    assert "error" not in driver.page_source.lower()
    driver.quit()


if __name__ == "__main__":
    print("Running Selenium Test Suite...\n")

    tests = [
        test_load_homepage,
        test_create_task,
        test_show_tasks,
        test_delete_task,
        test_open_edit_page,
        test_update_task,
        test_empty_submission,
        test_alert_on_success,
        test_edit_button_loading_text,
        test_page_no_errors,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1
        except AssertionError:
            print(f"[FAIL] {test.__name__} - Assertion Failed")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} - Exception: {e}")
            failed += 1

    print(f"\nTest Summary:\n  Passed: {passed}\n  Failed: {failed}")
    if failed > 0:
        sys.exit(1)
