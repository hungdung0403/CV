# Import the necessary libraries
import google.generativeai as genai
import json
from PIL import Image
import pytesseract
import os
import pandas as pd
import numpy as np

from constant.config import TESSERACT, IMAGE_FOLDER

# Store your API key
GOOGLE_API_KEY = 'AIzaSyAz9dXRzMom_fa2XiueN2jkQHvm4mNSluo'

# Configure the SDK with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# Create a GenerativeModel instance using the 'gemini-pro' model
model = genai.GenerativeModel('gemini-pro')

# Set the path to the pytesseract executable
pytesseract.pytesseract.tesseract_cmd = TESSERACT  # Replace with the actual path

def recognize_text_in_image(image_path):
    # Open the image using PIL
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert('L')

    # Convert the image to black and white
    image = Image.eval(image, lambda x: 255 if x > 128 else 0)

    # Recognize text in the image using pytesseract
    text = pytesseract.image_to_string(image, lang='vie')
    return text

# Example usage
image_directory = IMAGE_FOLDER
output_json_file = 'CV.json'

# Initialize an empty dictionary to store the extracted data
data = {}
personal_info_df = pd.DataFrame()
work_experience_df = pd.DataFrame()
education_df = pd.DataFrame()
references_df = pd.DataFrame()
additional_info_df = pd.DataFrame()
n_personal_info_df = pd.DataFrame()
n_work_experience_df = pd.DataFrame()
n_education_df = pd.DataFrame()
n_references_df = pd.DataFrame()
n_additional_info_df = pd.DataFrame()


# Iterate through all the image files in the directory
for filename in os.listdir(image_directory):
    first_value = filename.split('_')[0]
    if filename == first_value:
        break
for filename in os.listdir(image_directory):
    if filename.endswith('.png'):
        image_path = os.path.join(image_directory, filename)
        text = recognize_text_in_image(image_path)

        # Generate content by transforming the image content
        # The prompt should include the image path and specify the desired output format (JSON object)
        response = model.generate_content(f'The CV data of the candidates is structured as follows: {text}, divided into filename and text sections. The text section is separated by the delimiter \n. '
                                          f'We need to extract entities from text section, transform them into JSON objects '
                                          f'(Personal Info (Include: Name, Gender, Date of Birth, Phone Number, Email, Addess), Work Experience (Include: Company, Postion, Job Title, Start Date, End Date, Description), Education (Include: School Name, Degree, Start Date, End Date, GPA, Rank, Major), Skills, Objective, References, Additional Info, Interests, Award)'
                                          f', and perform spell checking. The rusult must be in JSON format')
        content = response.text
        data = content.replace("```json", "")
        data = data.replace("```", "")
        data = data.replace("null", '["nan"]')
        data = data.replace("[]", '["nan"]')
        data = data.replace("JSON", '')
        try:
            data = json.loads(data)
            data = {key: ['nan'] if value == [] else value for key, value in data.items()}
            # Add the extracted text to the data dictionary
            # Your code to process the extracted data goes here
        except json.JSONDecodeError:
            print(f"Error decoding JSON for file: {filename}")
            continue
        # Add the extracted text to the data dictionary
        import re

        if first_value == filename:
            # Create dataframes
            additional_info = data.get("Additional Info", [])
            if not additional_info:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                additional_info_df["Additional Info"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                additional_info_df["Additional Info"] = pd.Series(additional_info)
            Objective = data.get("Objective", [])
            if not Objective:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                additional_info_df["Objective"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                additional_info_df["Objective"] = pd.Series(Objective)
            References = data.get("References", [])
            if not References:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                additional_info_df["References"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                additional_info_df["References"] = pd.Series(References)
            Interests = data.get("Interests", [])
            if not Interests:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                additional_info_df["Interests"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                additional_info_df["Interests"] = pd.Series(Interests)
            Award = data.get("Award", [])
            if not Award:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                additional_info_df["Award"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                additional_info_df["Award"] = pd.Series(Award)
            additional_info_df = additional_info_df.assign(id=filename)
            print(data.get("Personal Info", []))
            personal_info_df = pd.DataFrame(data.get("Personal Info", []), index = [0], dtype=object)
            personal_info_df = personal_info_df.assign(id=filename)

            work_experience_df = pd.DataFrame(data.get("Work Experience", []))
            work_experience_df = work_experience_df.assign(id=filename)

            education_df = pd.DataFrame(data.get("Education", []))
            education_df = education_df.assign(id=filename)
            references_df = pd.DataFrame(data.get("References", []))
            references_df = references_df.assign(id=filename)

        else:
            # New DataFrames from data2
            n_additional_info = data.get("Additional Info", [])
            if not n_additional_info:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                n_additional_info_df["Additional Info"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                n_additional_info_df["Additional Info"] = pd.Series(n_additional_info)
            n_Objective = data.get("Objective", [])
            if not n_Objective:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                n_additional_info_df["Objective"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                n_additional_info_df["Objective"] = pd.Series(n_Objective)
            n_References = data.get("References", [])
            if not n_References:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                n_additional_info_df["References"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                n_additional_info_df["References"] = pd.Series(n_References)
            n_Interests = data.get("Interests", [])
            if not n_Interests:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                n_additional_info_df["Interests"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                n_additional_info_df["Interests"] = pd.Series(n_Interests)
            n_Award = data.get("Award", [])
            if not n_Award:
                # Nếu danh sách rỗng, gán NaN cho toàn bộ cột
                n_additional_info_df["Award"] = np.nan
            else:
                # Nếu có dữ liệu, gán danh sách thành một Series
                n_additional_info_df["Award"] = pd.Series(n_Award)
            n_additional_info_df = n_additional_info_df.assign(id=filename)
            print(data.get("Personal Info", []))
            n_personal_info_df = pd.DataFrame(data.get("Personal Info", []), index=[0], dtype=object)
            n_personal_info_df = n_personal_info_df.assign(id=filename)
            print('----------------------')
            print(n_personal_info_df)
            print('----------------------')
            n_work_experience_df = pd.DataFrame(data.get("Work Experience", []))
            n_work_experience_df = n_work_experience_df.assign(id=filename)

            n_education_df = pd.DataFrame(data.get("Education", []))
            n_education_df = n_education_df.assign(id=filename)

            n_references_df = pd.DataFrame(data.get("References", []))
            n_references_df = n_references_df.assign(id=filename)

            # Append the new DataFrames to the existing DataFrames
            personal_info_df = pd.concat([personal_info_df, n_additional_info_df], ignore_index=True)
            work_experience_df = pd.concat([work_experience_df, n_work_experience_df], ignore_index=True)
            education_df = pd.concat([education_df, n_education_df], ignore_index=True)
            references_df = pd.concat([references_df, n_references_df], ignore_index=True)
            additional_info_df = pd.concat([additional_info_df, n_additional_info_df])


# Print the updated DataFrames
print("Personal Info DataFrame:")
print(personal_info_df)
print()

print("Work Experience DataFrame:")
print(work_experience_df)
print()

print("Education DataFrame:")
print(education_df)
print()

print("References DataFrame:")
print(references_df)
print()

print("Additional Info DataFrame:")
print(additional_info_df)
print()
# Export the dataframes to CSV files
personal_info_df.to_csv('personal_info.csv', index=False)
work_experience_df.to_csv('work_experience.csv', index=False)
education_df.to_csv('education.csv', index=False)
references_df.to_csv('references.csv', index=False)
additional_info_df.to_csv('additional_info.csv', index=False)
