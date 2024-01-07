from data_generators.webscrapers.util import get_completion
from fpdf import FPDF


def get_car_brand_curiosity(brand_name):
    prompt = f"Tell me interesting facts about the {brand_name}. Write around 500 words."
    return get_completion(prompt)


def create_pdf(dict):
    pdf = FPDF()
    pdf.set_font("Arial", size=8)
    for key in dict:
        pdf.add_page()
        pdf.cell(0, 4, txt=key, ln=1, align="C")
        pdf.multi_cell(0, 4, txt=dict[key], align="L")

    pdf.output("car_brands_curiosities.pdf")


# Iterate through each brand and get curiosity
if __name__ == "__main__":
    # Dictionary to store brand curiosities
    brand_curiosities = {}
    # List of car brands
    car_brands = ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Nissan", "Tesla"]

    for brand in car_brands:
        curiosity = get_car_brand_curiosity(brand)
        brand_curiosities[brand] = curiosity

    create_pdf(brand_curiosities)