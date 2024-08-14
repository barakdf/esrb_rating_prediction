import pandas as pd
from bs4 import BeautifulSoup


def clean_html(text):
    """Cleans HTML content by removing all link tags and their content,
    while stripping other tags but retaining their content."""
    soup = BeautifulSoup(text, "html.parser")

    # Remove all <a> tags and their content
    for a in soup.findAll('a'):
        a.decompose()

    # Remove all other tags but keep the content
    cleaned_text = soup.get_text(separator=" ").strip()

    return cleaned_text


def clean_dataset(input_file, output_file, text_column):
    """Cleans the specified text column in a dataset and saves the cleaned data."""
    # Load the dataset
    df = pd.read_csv(input_file)

    # Apply the cleaning function to the specified column
    df[f'cleaned_{text_column}'] = df[text_column].apply(clean_html)

    # Save the cleaned dataset to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == "__main__":
    # Example usage
    input_file = "steam_app_details.csv"
    output_file = "cleaned_steam_app_details.csv"
    text_column = "detailed_description"

    clean_dataset(input_file, output_file, text_column)
