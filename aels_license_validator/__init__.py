import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError
from typing import Optional


async def case_id_lookup(
    case_id: str,
    approved_codes: list,
    timeout=30000
) -> Optional[dict]:
    """
    Takes a Case ID and a list of codes to search for a candidate.
    
    Returns a dictionary with:
    -first_name
    -last_name
    -code_checks

    Will return None if a TimeoutError occurs.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(timeout)

        await page.goto("https://aels.ade.arkansas.gov/AELS/Search.aspx")

        try:
            await page.locator("[id=MainContent_SearchCaseId]").fill(case_id)
            await page.locator("[id=MainContent_SearchButton]").click()
            await page.get_by_text("Select").last.click()
            first_name = await page.locator("[id=ctl00_MainContent_txtFirstName]").input_value()
            last_name = await page.locator("[id=ctl00_MainContent_txtLastName]").input_value()
            content = await page.locator(
                "[id=ctl00_MainContent_grdPublicLicenseAreas_ctl00]"
            ).inner_html()
        except TimeoutError:
            return None


    soup = BeautifulSoup(content, "html.parser")
    table_content = soup.find_all("tr")

    # Get the first column of content from the license table.
    # This is where the license codes will be found.
    possible_codes = [
        [text for text in row.stripped_strings][0] for row in table_content
    ]

    # Check to see if they have the code.
    code_checks = {}

    for code in approved_codes:
        if code in possible_codes:
            code_checks[code] = True
        else:
            code_checks[code] = False
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "code_checks": code_checks
    }


if __name__ == "__main__":
    # Zack Check: 528 and 317
    print(asyncio.run(case_id_lookup("8397011", ["528"])))
    print(asyncio.run(case_id_lookup("8397011", ["317"])))
