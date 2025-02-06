from playwright.sync_api import sync_playwright
import json

# Define the login page URL and file paths
login_url = "https://3rd-eye-ed-mate-qa.mpower-social.com/login"
auth_file = "auth_state.json"

def save_auth_state(context, token):
    # Save session storage token to the JSON file
    storage = context.storage_state()
    auth_data = {
        "storage": storage,
        "session_token": token
    }
    with open(auth_file, "w") as f:
        json.dump(auth_data, f)
    print(f"Authentication state and token saved to {auth_file}.")

def login(browser, username, password):
    # Launch the browser
    # browser = playwright.chromium.launch(headless=False)

    # Create a browser context
    context = browser.new_context()

    # Open a new page
    page = context.new_page()

    # Navigate to the login page
    page.goto(login_url)

    # Enter username
    page.fill("//input[@id='outlined-adornment-email-login']", username)

    # Enter password
    page.fill("//input[@id='outlined-adornment-password-login']", password)

    # Click the submit button
    page.click("//button[@type='submit']")

    # Wait for the user to be logged in
    page.wait_for_url("**/batches?batchName=")

    # Extract the token from session storage
    token = page.evaluate("() => sessionStorage.getItem('token')")
    print("Session Token:", token)

    # Save the authentication state and session token
    save_auth_state(context, token)

    # Keep the browser open
    # input("Press Enter once you're ready to proceed...")
    page.wait_for_timeout(3000)
    browser.close()

def logout(login_with_saved_state):
        # Login and create a page instance
        page = login_with_saved_state

        # wait for appear all batch list
        page.wait_for_timeout(3000)
        page.wait_for_load_state("domcontentloaded")

        page.wait_for_timeout(10000)

        page.wait_for_selector("//div[@role='button' and @aria-label='user-account']", timeout=10000)

        # Code to logout

        ##Click on profile
        page.locator("//div[@role='button' and @aria-label='user-account']").click()

        ##Click on logout button
        page.locator("//div[@role='button']//p[text()='Logout']").click()

        # Assert that the button is available
        assert page.locator("button:has-text('Sign In')").is_visible(), "Sign In button is not visible"

        print("Logout is succesfull")

