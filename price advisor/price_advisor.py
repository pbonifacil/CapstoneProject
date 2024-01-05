import warnings
import umap.umap_ as umap
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# Ignore warnings
warnings.filterwarnings("ignore")

def predict_price(df: pd.DataFrame, 
                  brand: str, 
                  model: str, 
                  year: int, 
                  displacement_cm3: int, 
                  power_hp: int, 
                  gear_type: str,
                  stand_warranty_months: int = 12,
                  condition: str = "used",
                  number_of_doors: int = 5,
                  kilometers: int = 15000
                  ):
    
    # Fixed values - Forces the model to look for cars with an average price
    compared_price = "The price is within the average."

    # Convert all str variables to lowercase
    brand = brand.lower()
    model = model.lower()
    gear_type = gear_type.lower()
    condition = condition.lower()

    # Convert the brand and model to lowercase
    df["Brand"] = df["Brand"].str.lower()
    df["Model"] = df["Model"].str.lower()

    # Filter the df by brand and model
    filtered_df = df[(df["Brand"] == brand) & (df["Model"] == model)]

    # Select the useful columns to predict the similar price of the car
    predict_columns = ["Year", "Kilometers", "Displacement_cm3", "Power_hp", "Gear_Type", "Number_of_Doors", "Stand_Warranty_months", "Condition", "Compared_Price"]

    # Use the columns to create a umap of the cars
    df_umap = filtered_df[predict_columns]

    # Add the new car to the df
    df_umap.loc[1000000] = [year, kilometers, displacement_cm3, power_hp, gear_type, number_of_doors, stand_warranty_months, condition, compared_price]

    # Substitute the NaN values with the mean of the column or 0 depending on the column
    df_umap["Stand_Warranty_months"].fillna(0, inplace=True)

    # Convert the gear type and condition to lowercase
    df_umap["Gear_Type"] = df_umap["Gear_Type"].str.lower()
    df_umap["Condition"] = df_umap["Condition"].str.lower()

    # Convert the categorical columns to numerical
    df_umap = pd.get_dummies(df_umap, columns=["Gear_Type", "Number_of_Doors", "Condition", "Compared_Price"], drop_first=True)

    # Create the umap
    reducer = umap.UMAP(n_jobs=-1)
    embedding = reducer.fit_transform(df_umap)

    # Get the umap embedding of the new car
    new_car_embedding = embedding[-1]

    # Fit the NearestNeighbors model
    model_knn = NearestNeighbors(n_neighbors=6, algorithm='ball_tree')  # n_neighbors is 6 because the car itself is included
    model_knn.fit(embedding)

    # Find the nearest neighbors
    distances, indices = model_knn.kneighbors([new_car_embedding])

    # The first index will be the new car itself, so we exclude it
    closest_neighbors_indices = indices[0][1:]

    # Get the indices in the original df
    closest_neighbors_indeces_original_df = df_umap.iloc[closest_neighbors_indices].index

    # Extract the prices of the closest neighbors
    avg_price = sum(df.iloc[closest_neighbors_indeces_original_df]["Price_EUR"].values)/5

    # keep only the first 2 significant digits
    avg_price = int(round(avg_price, -3))
    
    return avg_price



## Working example:
# df = pd.read_csv("C:/Users/migue/OneDrive/Desktop/car_dataset.csv", index_col=0)
# avg_price = predict_price(df = df, 
#                           brand = "bmw", 
#                           model = "520", 
#                           year = 2019, 
#                           displacement_cm3 = 2000, 
#                           power_hp = 190, 
#                           gear_type = "automatic",
#                           stand_warranty_months = 12,
#                           condition = "used",
#                           number_of_doors = 5,
#                           kilometers = 15000
#                           )

# print(f"The predicted price is: {avg_price}€")