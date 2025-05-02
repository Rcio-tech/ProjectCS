import streamlit as st

st.title("Car Journey CO₂ Emission Calculator")

st.write("Welcome! This app will help you calculate and compare the carbon emissions of your trips.")

# Sample input
start = st.text_input("Enter start address")
end = st.text_input("Enter destination address")
vehicle = st.selectbox("Select vehicle type", ["Petrol", "Diesel", "Electric", "Hybrid"])

if st.button("Calculate Emissions"):
    st.write(f"Calculating emissions from {start} to {end} using a {vehicle} vehicle...")

