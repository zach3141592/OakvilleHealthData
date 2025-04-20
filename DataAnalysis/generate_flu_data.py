import csv
from datetime import datetime, timedelta
import random
import os

# List of pharmacy addresses in Oakville
pharmacies = [
    "Shoppers Drug Mart, 123 Lakeshore Rd W, Oakville",
    "Rexall, 245 Trafalgar Rd, Oakville",
    "Pharmasave, 156 Kerr St, Oakville",
    "Guardian Pharmacy, 89 Cornwall Rd, Oakville",
    "Walmart Pharmacy, 240 Leighland Ave, Oakville",
    "Costco Pharmacy, 1200 South Service Rd, Oakville",
    "Loblaw Pharmacy, 301 Cornwall Rd, Oakville",
    "Sobeys Pharmacy, 240 Leighland Ave, Oakville",
    "Medicine Shoppe, 345 Kerr St, Oakville",
    "IDA Pharmacy, 178 Lakeshore Rd E, Oakville"
]

# List of common Oakville street names
streets = [
    "Lakeshore Rd", "Trafalgar Rd", "Kerr St", "Cornwall Rd", "Leighland Ave",
    "Dundas St", "Speers Rd", "Rebecca St", "Dorval Dr", "Third Line",
    "Sixth Line", "Neyagawa Blvd", "Upper Middle Rd", "Glen Abbey Gate",
    "Maple Grove Dr", "River Oaks Blvd", "Winston Park Blvd", "Bronte Rd",
    "QEW", "Ford Dr", "Wyecroft Rd", "Chartwell Rd", "Nottinghill Gate",
    "Glenashton Dr", "Westoak Trails Blvd"
]

# List of street types
street_types = ["Rd", "St", "Ave", "Blvd", "Dr", "Gate", "Line", "Cres", "Way"]

# List of directions
directions = ["N", "S", "E", "W", ""]

def generate_random_address():
    # Generate street number (1-9999)
    street_number = random.randint(1, 9999)
    
    # Choose a random street
    street = random.choice(streets)
    
    # Generate unit number (optional)
    unit = ""
    if random.random() < 0.3:  # 30% chance of having a unit number
        unit = f"{random.randint(1, 999)}-"
    
    # Generate postal code
    postal_code = f"L{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)} {random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
    
    return f"{unit}{street_number} {street}, Oakville, ON {postal_code}"

# Generate random dates between September 1, 2023 and March 31, 2024
def random_date():
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2024, 3, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

print("Starting to generate data...")
print(f"Current working directory: {os.getcwd()}")

# Generate 1000 records
try:
    output_file = 'flu_data_new.csv'  # Removed DataAnalysis/ prefix since we're already in that directory
    print(f"Writing to file: {output_file}")
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Pharmacy Address', 'Customer Address'])  # Header row
        print("Header written successfully")
        
        for i in range(1000):
            date = random_date()
            pharmacy = random.choice(pharmacies)
            customer_address = generate_random_address()
            writer.writerow([date, pharmacy, customer_address])
            if i % 100 == 0:  # Print progress every 100 records
                print(f"Generated {i} records")
    
    print(f"Data generation completed successfully. File size: {os.path.getsize(output_file)} bytes")
except Exception as e:
    print(f"An error occurred: {str(e)}") 