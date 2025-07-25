import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://midway-auth.amazon.com/login?next=%2FSSO%2Fredirect%3Fclient_id%3Dhttps%253A%252F%252Fidp-us-west-2.federate.amazon.com%26redirect_uri%3Dhttps%253A%252F%252Fidp-us-west-2.federate.amazon.com%252Fapi%252Fv1%252Fintermediate%26response_type%3Did_token%26scope%3Dopenid%26nonce%3DP250724131508647PDXHQD8M9WY3LJF%26state%3Dus-west-2_P250724131508647PDXHQD8M9WY3LJF_AgR4e6q2HENI5bYmNjjK-ZiEmFlCQqv41KRYGf9I5ZCANhIAKAABAAN0eG4AH1AyNTA3MjQxMzE1MDg2NDdQRFhIUUQ4TTlXWTNMSkYAAQAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjY0MjM5NzE3MDM1MDprZXkvbXJrLTZlZDM4YTQ3YjY3NDQ1YjA5MTA4ZmVhOTY5Y2M3NDVkALgBAgEAeOYmjA3sUyj2zMF5PB1ua6ihksVKub2WCzL4wiv8kAFCAXFbcGEe41P7JXVdEIT5cgIAAAB-MHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxxd8qquYwbUk3iyQUCARCAO6aCRt6JJX3SaAU5EZfyjgslBNyzvyfaSvhY2W4tGARUlGt_l4MJPNaao6kSmPgX7UuHmmjLUA1MuVeLAgAAEAA1VPlbKv_nX2UBQNCEGv1rtJT9Bwhta6UpxvdpCg0TJ6Vojc0HLVcJTxl0lK89Jl3_____AAAAAQAAAAAAAAAAAAAAAQAAAE9H1i0rlhQjH7Cxw0HnW-LG-xcdnKychdwy6uDgE6xfPZ5hVKSXt8VgJi3AiNAg0Au9SXEA0ml6MxTGlr9TadZis75XFbjH9KAErAHuxShNrH33-FiCR13Yf5XruCq1tA&require_digital_identity=false")
    page.get_by_role("textbox", name="Amazon username").click()
    page.get_by_role("textbox", name="Amazon username").fill("kambroem")
    page.get_by_role("textbox", name="PIN").click()
    page.get_by_role("textbox", name="PIN").fill("3473991073")
    page.get_by_role("button", name="Sign in").click()
    page.goto("https://midway-auth.amazon.com/SSO/redirect?client_id=https%3A%2F%2Fidp-us-west-2.federate.amazon.com&redirect_uri=https%3A%2F%2Fidp-us-west-2.federate.amazon.com%2Fapi%2Fv1%2Fintermediate&response_type=id_token&scope=openid&nonce=P250724131508647PDXHQD8M9WY3LJF&state=us-west-2_P250724131508647PDXHQD8M9WY3LJF_AgR4e6q2HENI5bYmNjjK-ZiEmFlCQqv41KRYGf9I5ZCANhIAKAABAAN0eG4AH1AyNTA3MjQxMzE1MDg2NDdQRFhIUUQ4TTlXWTNMSkYAAQAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjY0MjM5NzE3MDM1MDprZXkvbXJrLTZlZDM4YTQ3YjY3NDQ1YjA5MTA4ZmVhOTY5Y2M3NDVkALgBAgEAeOYmjA3sUyj2zMF5PB1ua6ihksVKub2WCzL4wiv8kAFCAXFbcGEe41P7JXVdEIT5cgIAAAB-MHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxxd8qquYwbUk3iyQUCARCAO6aCRt6JJX3SaAU5EZfyjgslBNyzvyfaSvhY2W4tGARUlGt_l4MJPNaao6kSmPgX7UuHmmjLUA1MuVeLAgAAEAA1VPlbKv_nX2UBQNCEGv1rtJT9Bwhta6UpxvdpCg0TJ6Vojc0HLVcJTxl0lK89Jl3_____AAAAAQAAAAAAAAAAAAAAAQAAAE9H1i0rlhQjH7Cxw0HnW-LG-xcdnKychdwy6uDgE6xfPZ5hVKSXt8VgJi3AiNAg0Au9SXEA0ml6MxTGlr9TadZis75XFbjH9KAErAHuxShNrH33-FiCR13Yf5XruCq1tA")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
