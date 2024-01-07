from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import pickle
from StringProgressBar import progressBar


def listing_link_scraper(n_listings, load_data=False):
    """
    Scrapes Standvirtual website for car listing links.

    Parameters:
    - n_listings (int): The number of car listing links to be scraped.
    - load_data (bool): True if you want to fill an existing links list.

    Returns:
    - list: A list of scraped car listing links from Standvirtual.

    This function initiates a web scraper using Selenium and Beautiful Soup to retrieve car listing links from Standvirtual.
    It navigates through multiple pages of the website, starting from page 2 to collect the specified number of car listing links.
    The progress is indicated by a progress bar printed in the console.

    Note: Ensure you have the geckodriver downloaded and provide the correct path to the executable_path.
    """
    geckodriver_path = r'selenium/geckodriver.exe'
    dr = webdriver.Firefox(service=FirefoxService(executable_path=geckodriver_path))  # initialize firefox web driver
    url = "https://www.standvirtual.com/carros?page="  # base url for scraping, just attach the number of the page at the end of the string
    listing_links = []
    page = 2  # start at page 2 because page 1 sometimes is a bit different

    if load_data:
        with open("listing_links.pkl", "rb") as fa:
            listing_links = pickle.load(fa)

    while len(listing_links) < n_listings:
        # PROGRESS BAR
        progress_bar = progressBar.filledBar(n_listings, len(listing_links))
        print(progress_bar[0] + " - " + str(round(progress_bar[1], 2)) + f"%  -  {len(listing_links)} links scraped...", end="\r")

        dr.get(url + str(page))  # fetch webpage data
        soup = BeautifulSoup(dr.page_source, "html.parser")  # use BeautifulSoup to extract html code
        page_links = soup.find_all('a', href=True)  # find all fields with <a> tag and 'href' attribute, these include listing and non-listing links
        page_listing_links = [link['href'] for link in page_links if
                              link['href'].startswith('https://www.standvirtual.com/carros/anuncio/')]  # filter only for listing links

        listing_links.extend(page_listing_links)  # attach page links to final list
        listing_links = list(set(listing_links))  # remove duplicate links
        page += 1  # turn the page

        time.sleep(2)  # sleep for 2 seconds so we don't get flagged by Standvirtual

    dr.close()  # close the webdriver
    return listing_links


if __name__ == "__main__":
    links = listing_link_scraper(10000)
    links = list(set(links))
    f = open("listing_links.pkl", "wb")
    pickle.dump(links, f)
    f.close()
    print("Links scraped and saved to disk...")

# to read the data:
# with open("listing_links.pkl", "rb") as fa:
#     data = pickle.load(fa)
