import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def check(case_id: str, approved_codes: list) -> bool:
    """
    Takes a Case ID and a list of codes to search for in candidate.
    Returns True if they have at least one of the codes.
    Returns False if they have none of the codes.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://aels.ade.arkansas.gov/AELS/Search.aspx")

        await page.locator("[id=MainContent_SearchCaseId]").fill(case_id)
        await page.locator("[id=MainContent_SearchButton]").click()
        await page.get_by_text("Select").last.click()
        content = await page.locator(
            "[id=ctl00_MainContent_grdPublicLicenseAreas_ctl00]"
        ).inner_html()

    soup = BeautifulSoup(content, "html.parser")
    table_content = soup.find_all("tr")

    # Get the first column of content from the license table.
    # This is where the license codes will be found.
    possible_codes = [
        [text for text in row.stripped_strings][0] for row in table_content
    ]

    # Check to see if they have the code.
    for code in possible_codes:
        if code in approved_codes:
            return True
    return False


if __name__ == "__main__":
    # Zack Check: 528 and 317
    print(asyncio.run(check("8397011", ["528"])))
    print(asyncio.run(check("8397011", ["317"])))