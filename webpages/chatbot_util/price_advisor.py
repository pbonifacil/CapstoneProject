import warnings
import umap.umap_ as umap  # pip install umap-learn
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from webpages.chatbot_util.util import DATASET_PATH

# Ignore warnings
warnings.filterwarnings("ignore")


def predict_price(brand: str,
                  model: str,
                  year: int,
                  displacement_cm3: int,
                  power_hp: int,
                  gear_type: str,
                  kilometers: int,
                  fuel: str,
                  condition: str = "used",
                  ):
    df = pd.read_csv(DATASET_PATH, index_col=0)

    # Fixed values - Forces the model to look for cars with an average price
    compared_price = "The price is within the average."

    # Convert all str variables to lowercase
    brand = brand.lower()
    model = model.lower()
    gear_type = gear_type.lower()
    condition = condition.lower()
    fuel = fuel.lower()

    # Convert the brand and model to lowercase
    df["Brand"] = df["Brand"].str.lower()
    df["Model"] = df["Model"].str.lower()

    # Filter the df by brand and model
    filtered_df = df[(df["Brand"] == brand) & (df["Model"] == model)]

    # Select the useful columns to predict the similar price of the car
    predict_columns = ["Year", "Kilometers", "Displacement_cm3", "Power_hp", "Gear_Type", "Condition", "Fuel",
                       "Compared_Price"]

    # Use the columns to create a umap of the cars
    df_umap = filtered_df[predict_columns]

    df_umap['Displacement_cm3'] = df_umap['Displacement_cm3'].fillna(0)

    # Add the new car to the df
    df_umap.loc[1000000] = [year, kilometers, displacement_cm3, power_hp, gear_type, condition, fuel, compared_price]

    # Convert the gear type and condition to lowercase
    df_umap["Gear_Type"] = df_umap["Gear_Type"].str.lower()
    df_umap["Condition"] = df_umap["Condition"].str.lower()
    df_umap["Fuel"] = df_umap["Fuel"].str.lower()

    # Convert the categorical columns to numerical
    df_umap = pd.get_dummies(df_umap, columns=["Gear_Type", "Fuel", "Condition", "Compared_Price"],
                             drop_first=True)

    # Create the umap
    reducer = umap.UMAP(n_jobs=-1)
    embedding = reducer.fit_transform(df_umap)

    # Get the umap embedding of the new car
    new_car_embedding = embedding[-1]

    try:
        # Fit the NearestNeighbors model
        model_knn = NearestNeighbors(n_neighbors=6,
                                     algorithm='ball_tree')  # n_neighbors is 6 because the car itself is included
        model_knn.fit(embedding)

        # Find the nearest neighbors
        distances, indices = model_knn.kneighbors([new_car_embedding])

        # The first index will be the new car itself, so we exclude it
        closest_neighbors_indices = indices[0][1:]

        # Get the indices in the original df
        closest_neighbors_indeces_original_df = df_umap.iloc[closest_neighbors_indices].index

        # Extract the prices of the closest neighbors
        avg_price = sum(df.iloc[closest_neighbors_indeces_original_df]["Price_EUR"].values) / 5

        # keep only the first 2 significant digits
        avg_price = int(round(avg_price, -3))
        return f'A car with those specifications is worth around {avg_price}€. Let me know if you need anything else. 😉'

    except TypeError:
        return "We don't have enough data to make a prediction. Sorry for any inconvenience."


class PredictorInput(BaseModel):
    brand: str = Field(description="brand of the car")
    model: str = Field(description="model of the car")
    year: int = Field(description="year of the car")
    displacement_cm3: int = Field(description="displacement of the car")
    power_hp: int = Field(description="horsepower of the car")
    gear_type: str = Field(description="gear type of the car")
    kilometers: int = Field(description="kilometers of the car")
    fuel: str = Field(description="type of fuel of the car")
    condition: str = Field(description="used or new car")


class CustomPredictorTool(BaseTool):
    name = "price_predictor"
    description = "useful for when you need to predict the price of a car"
    args_schema: Type[BaseModel] = PredictorInput
    return_direct: bool = True

    def _run(
            self, brand: str, model: str, year: int, displacement_cm3: int, power_hp: int,
            gear_type: str, kilometers: int, fuel: str, condition: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return str(predict_price(brand=brand,
                                 model=model,
                                 year=year,
                                 displacement_cm3=displacement_cm3,
                                 power_hp=power_hp,
                                 gear_type=gear_type,
                                 kilometers=kilometers,
                                 fuel=fuel,
                                 condition=condition,
                                 ))

    async def _arun(
            self, brand: str, model: str, year: int, displacement_cm3: int, power_hp: int,
            gear_type: str, kilometers: int, fuel: str, condition: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Predictor does not support async")
