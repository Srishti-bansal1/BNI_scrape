from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict
import pandas as pd
import os

@dataclass
class Details:
    name: str = None
    company :str = None
    Profession : str = None

@dataclass
class DetailsList:
    details_list=[]
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize((asdict(details) for details in self.details_list), sep="_")
    
    def save_to_excel(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)


def main():
     with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://bni-hyderabadwest.in/hyderabad-west-aastha/en-IN/memberlist?chapterName=33661&regionIds=10745$isChapterwebsite",timeout = 90000)     
        page.wait_for_timeout(20000)

        listings = page.locator('//div[contains(@class,"page")]/div[2]/div/section/div/div[2]/div/table/tbody/tr').all() 
        print(listings)
        print(len(listings))

        details_list = DetailsList()
        n = 1
        for listing in listings[:5]:
            listing.click()
            page.wait_for_timeout(10000)

            name_xpath = f'//*[@id="chapterListTable"]/tbody/tr[{n}]/td[1]'
            company_xpath = f'//*[@id="chapterListTable"]/tbody/tr[{n}]/td[2]'
            Profession_xpath = f'//*[@id="chapterListTable"]/tbody/tr[{n}]/td[3]'
            print(n)

            detail = Details()
        
            detail.name = page.locator(name_xpath).inner_text()
            print(detail.name)
            detail.company = page.locator( company_xpath).inner_text()
            print(detail.company)
            detail.Profession = page.locator( Profession_xpath).inner_text()
            print(detail.Profession)
            n = n+1
            print(n)

            details_list.details_list.append(detail)

        details_list.save_to_excel("data")


        browser.close()


if __name__ == "__main__":
    main()