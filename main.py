from scraper import run_scraper

with open("channel_list.txt", "r") as file:
    for line in file:
        try:
            run_scraper(line)
        except Exception as ex:
            print(ex)