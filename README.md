# NOVA IMS 3rd Year - Capstone Project

## AutoMentor - Steering you toward your dream car

This repository contains a Streamlit chat bot application that offers three distinct features related to car information retrieval and analysis. The three main functionalities include:

1. **Car Listing Search**: Allows users to search for car listings within Standvirtual's database based on specified car details.

2. **Vehicle Appraisal**: Assists users in appraising the value of a vehicle they intend to sell. This feature employs umap and NearestNeighbors algorithms to determine the average price of the five closest neighbors, providing valuable pricing insights.

3. **Vectorstore Database Similarity Search**: Enables users to conduct a similarity search within the database for information on various car brands.

## Instructions for Usage

### Streamlit App:
To run the Streamlit app, follow these steps:
1. Install the necessary dependencies from `requirements.txt`.
```
pip install -r requirements.txt
```
2. Run the main application file.
```
streamlit run main.py
```
3. Access the Streamlit app via the provided URL in your browser.

### Data Generators:
The data_generators folder contains scripts for generating specific data used within the application. To utilize these generators:

1. Navigate to the `data_generators` directory.
2. Install the required dependencies specified in `generators_requirements.txt`.
```
pip install -r data_generators/generators_requirements.txt
```
3. Run each script individually as needed.

## License
This project is licensed under the [MIT License](LICENSE).

Please feel free to explore, contribute, and provide feedback to enhance the functionality of AutoMentor!
