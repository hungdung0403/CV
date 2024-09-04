from database.connections_db import connect_db
from module.crawling.crawl_cv_timviec365 import crawl_list_cv, crawl_url_cv, download_images, crawl_url_cv_info
from constant.config import WEB_URL_TV365, IMAGE_FOLDER, WEB_URL_ITVIEC
from module.crawling.crawl_job_itviec import crawl_url_job, crawl_list_job
import concurrent.futures


def main():
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the crawl_timviec365 function to the executor
        future_timviec365 = executor.submit(crawl_timviec365)

        # Submit the crawl_itviec function to the executor
        future_itviec = executor.submit(crawl_itviec)

        # Wait for both functions to complete
        future_timviec365.result()
        future_itviec.result()

    print("Crawling and downloading completed successfully.")


def crawl_timviec365():
    # Run the crawling logic for timviec365
    links = crawl_list_cv(WEB_URL_TV365)
    all_matches = set()

    for link in links:
        crawl_url_cv_info(link)
        matches = crawl_url_cv(link)
        all_matches.update(matches)

    download_images(all_matches, IMAGE_FOLDER)
    print(connect_db().server_info())


def crawl_itviec():
    # Run the crawling logic for ITViec
    links = crawl_list_job(WEB_URL_ITVIEC)
    for link in links:
        crawl_url_job(link)


if __name__ == "__main__":
    main()
