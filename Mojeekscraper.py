import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

def scrape_mojeek_search_results(search_term, num_results=10):
    encoded_search_term = quote(search_term)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    start_index = 0
    results_count = 0

    while results_count < num_results:
        url = f"https://www.mojeek.com/search?q={encoded_search_term}&s={start_index}"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                results = soup.find_all("li")

                if results:
                    print(f"\nSearch results for '{search_term}':\n")
                    for result in results:
                        title_element = result.find("h2")
                        if title_element:
                            link = result.find("a")["href"]
                            print(link)
                            results_count += 1
                            if results_count == num_results:
                                return
                    time.sleep(1)
                else:
                    print(f"No more results found for '{search_term}'.")
                    return
            elif response.status_code == 429:
                print("Too many requests. Consider reducing frequency or rotating user agents.")
                return
            else:
                print("Failed to retrieve search results. Check the URL and network connection.")
                return
        except Exception as e:
            print("An error occurred:", e)
            return

        start_index += 10

def main():
    search_term = input("Enter search term: ")
    num_results = int(input("Enter the number of results you want: "))
    scrape_mojeek_search_results(search_term, num_results)

if __name__ == "__main__":
    main()
