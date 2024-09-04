# ETL Pipeline for TimViec365 Job Listings

This project is an ETL (Extract, Transform, Load) pipeline for extracting data from the TimViec365 job listing website and processing it. The main purpose is to automate the process of collecting and processing job listings data.

## Getting Started

To run this project, follow these steps:

1. Set up the configuration file:
   - Open the `python-etl-cv/constant/config.py` file.
   - Fill in the `WEB_URL` variable with the URL of the TimViec365 website you want to crawl.

2. Install the required dependencies:
   - Open a terminal or command prompt.
   - Navigate to the project directory (`python-etl-cv`).
   - Run the following command to install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

3. Run the crawling script:
   - Open a terminal or command prompt.
   - Navigate to the `helper` directory (`python-etl-cv/helper`).
   - Run the following command to execute the crawling script:
     ```
     python crawl_cv_timviec365.py
     ```

4. Run the main script:
   - Open a terminal or command prompt.
   - Navigate to the project directory (`python-etl-cv`).
   - Run the following command to execute the main ETL pipeline:
     ```
     python main.py
     ```

## Project Structure

The project's directory structure is as follows:

```
python-etl-cv/
├── constant/
│   └── config.py
├── helper/
│   └── crawl_cv_timviec365.py
├── interface/
│   └── __init__.py
├── main.py
├── model/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Key Files and Directories

- `constant/config.py`: Contains constant values or configurations for the project.
- `helper/crawl_cv_timviec365.py`: A helper script for crawling CVs from the TimViec365 website.
- `interface/`: This directory is likely where the project's user interface or interaction logic resides.
- `model/`: Contains the project's primary data models or algorithms.
- `main.py`: The main ETL pipeline script.
- `requirements.txt`: Specifies the project's dependencies.
- `README.md`: This file, which provides an introduction to the project and instructions on how to run it.

## Notable Aspects

- The project follows the Python package layout convention, which is a common practice for organizing Python codebases.
- Each directory has an `__init__.py` file, allowing them to be treated as packages.
- The project structure makes it easy to maintain and extend the project as it grows in complexity.

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. I'm always open to suggestions and improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Acknowledgments

This project was inspired by the need for an automated ETL pipeline for job listings data. The code for crawling CVs from TimViec365 was adapted from existing open-source projects.