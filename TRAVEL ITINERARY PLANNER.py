#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import matplotlib.pyplot as plt
from tabulate import tabulate

# Define functions to get coordinates and calculate distance
def get_coordinates(city):
    geolocator = Nominatim(user_agent="distance_calculator")
    location = geolocator.geocode(city)
    if location is None:
        raise ValueError(f"Could not find coordinates for {city}")
    return (location.latitude, location.longitude)

def calculate_distance(city1, city2):
    coords1 = get_coordinates(city1)
    coords2 = get_coordinates(city2)
    distance = geodesic(coords1, coords2).kilometers
    return distance

# Define transportation and accommodation costs
transportation_costs = {
    "plane": 5000,
    "train": 200,
    "bus": 100,
}

accommodation_costs = {
    "3": 100,
    "2": 400,
    "1": 2000
}

# Welcome message and input gathering
print("Welcome to the TRAVEL ITINERARY!")
source = input("Enter your city name from where you want to start travelling: ")
destination = input("Enter destination: ")
trans_cost = calculate_distance(source, destination)
print(f"Distance between your city and destination is {trans_cost} km")
mode_of_transport = input("Enter mode of transportation (plane/train/bus): ").lower()
while mode_of_transport not in transportation_costs:
    print("Invalid mode of transportation. Please choose from: plane, train, bus.")
    mode_of_transport = input("Enter mode of transportation (plane/train/bus): ").lower()
accommodation_type = input("Enter accommodation type (class: 1/2/3): ").lower()
while accommodation_type not in accommodation_costs:
    print("Invalid accommodation type. Please choose from: 1, 2, 3")
    accommodation_type = input("Enter accommodation type (class: 1/2/3): ").lower()
daily_food_budget = float(input("Enter daily food budget (in ₹): "))
start_date_str = input("Enter travel start date (DD-MM-YYYY): ")
start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
end_date_str = input("Enter travel end date (DD-MM-YYYY): ")
end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
total_days = (end_date - start_date).days
additional_expenses = float(input("Enter estimated additional expenses (in ₹): "))
num_persons = int(input("Enter the number of persons: "))

# Read CSV file
df=pd.read_excel(r"C:\Users\ptlpr\OneDrive\Documents\project.xlsx")

# Display the first few rows
condition = df['city'] == destination
filtered_data = df[condition]
print(filtered_data)

# Calculate total costs
transportation_cost = transportation_costs[mode_of_transport]
accommodation_cost_per_day = accommodation_costs[accommodation_type]
total_accommodation_cost = accommodation_cost_per_day * total_days * num_persons
total_food_cost = daily_food_budget * total_days * num_persons
total_transportation_cost = transportation_cost * trans_cost * num_persons
total_cost = total_accommodation_cost + total_food_cost + total_transportation_cost + additional_expenses

# Check if expenses are reasonable relative to distance
expenses_distance_ratio = total_cost / trans_cost

# Create and save the Folium map
city1_coords = get_coordinates(source)
city2_coords = get_coordinates(destination)
m = folium.Map(location=[city1_coords[0], city1_coords[1]], zoom_start=6)
folium.Marker([city1_coords[0], city1_coords[1]], popup=source).add_to(m)
folium.Marker([city2_coords[0], city2_coords[1]], popup=destination).add_to(m)
m.save('map.html')
display(m)

# Plot expenses and distance over time
dates = pd.date_range(start=start_date, end=end_date)
daily_distances = [trans_cost] * len(dates)
daily_expenses = [(total_accommodation_cost + total_food_cost + additional_expenses)] * len(dates)

plt.figure(figsize=(10, 6))
plt.plot(dates, daily_distances, label='Distance (km)')
plt.plot(dates, daily_expenses, label='Expenses (₹)')
plt.title('Expenses and Distance Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot as an image
plt.savefig('expenses_distance_plot.png', dpi=50)

# Display the plot
plt.show()

# Calculate daily expenses for the chosen accommodation class
daily_expenses_class = (accommodation_cost_per_day + daily_food_budget + additional_expenses) * num_persons / total_days

# Check if expenses are reasonable relative to chosen accommodation class
if total_cost <= (daily_expenses_class * total_days):
    print("Your expenditure is reasonable given the chosen accommodation class.")
else:
    print("Your expenditure is high relative to the chosen accommodation class. You may need to reconsider your budget.")

# Add total expenses and distance of source and destination to the output
summary_df = pd.DataFrame({
    'City': [source, destination],
    'Total Distance (km)': [trans_cost, trans_cost],
    'Total Expenses (₹)': [total_cost, total_cost]
})

print("\nSummary of Travel Itinerary:")
print("\n----- Travel Cost Summary -----")
summary_table = [
    ["Transportation Cost", f"₹{total_transportation_cost}"],
    [f"Accommodation Cost ({accommodation_type})", f"₹{total_accommodation_cost}"],
    [f"Food Cost ({daily_food_budget} per day per person)", f"₹{total_food_cost}"],
    ["Additional Expenses", f"₹{additional_expenses}"],
    ["Total Estimated Cost", f"₹{total_cost}"]
]

# Add color to the summary table
def color_text(text, color):
    return f"\033[{color}m{text}\033[0m"

summary_table_colored = []
for row in summary_table:
    summary_table_colored.append([color_text(row[0], '1;36'), color_text(row[1], '1;35')])

print(tabulate(summary_table_colored, tablefmt='plain'))

