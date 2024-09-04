import os
from dotenv import load_dotenv

load_dotenv()

CHROMEDRIVER_PATH = str(os.getenv("CHROMEDRIVER_PATH"))
IMAGE_FOLDER = "cv_collection"
MONGO_URI = str(os.getenv("MONGO_URI"))
USERNAME_DB = str(os.getenv("USERNAME_DB"))
PASSWORD_DB = str(os.getenv("PASSWORD_DB"))
DOMAIN_SELENIUM = str(os.getenv("DOMAIN_SELENIUM"))
TESSERACT = str(os.getenv("TESSERACT"))
DATABASE_NM = os.getenv("DATABASE_NM")

# Information needed to retrieve data (TIMVIEC365)
WEB_URL_TV365 = str(os.getenv("WEB_URL_TV365"))
LIST_INFO_TV365 = os.getenv("CONTENT_INFO_TV365")
COLLECTION_NM_TV365 = os.getenv("COLLECTION_NM_TV365")

# Information needed to retrieve data (ITVIEC)
WEB_URL_ITVIEC = str(os.getenv("WEB_URL_ITVIEC"))
COLLECTION_NM_ITVIEC = os.getenv("COLLECTION_NM_ITVIEC")
