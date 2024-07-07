import streamlit as st
import pandas as pd
import altair as alt

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal
        "Waste": 0.1  # kgCO2/kg
    },
    # Add more countries here with their respective emission factors
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Streamlit app code
st.title("Carbon Calculator")

# User inputs
st.subheader("Your Country")
country = st.selectbox("Select", list(EMISSION_FACTORS.keys()))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, 10.0, key="distance_input")

    st.subheader("Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, 100.0, key="electricity_input")

with col2:
    st.subheader("Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, 10.0, key="waste_input")

    st.subheader("Number of meals per day")
    meals = st.number_input("Meals", 0, 10, 3, key="meals_input")

# Normalize inputs
distance_yearly = distance * 365
electricity_yearly = electricity * 12
meals_yearly = meals * 365
waste_yearly = waste * 52

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance_yearly
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity_yearly
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals_yearly
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste_yearly

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):
    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        st.warning("In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita. Between 1972 and 2021, CO2 emissions per capita of India grew substantially from 0.39 to 1.9 tons of CO2 per capita rising at an increasing annual rate that reached a maximum of 9.41% in 2021")

        # Suggest ways to reduce emissions
        st.subheader("Tips to Reduce Your Carbon Footprint")
        st.markdown("""
        - **Transportation**: Use public transport, carpool, or switch to electric vehicles.
        - **Electricity**: Opt for energy-efficient appliances, use renewable energy sources.
        - **Diet**: Reduce meat consumption, opt for plant-based meals.
        - **Waste**: Recycle, compost organic waste, reduce single-use plastics.
        """)

    # Visualization
    df = pd.DataFrame({
        'Category': ['Transportation', 'Electricity', 'Diet', 'Waste'],
        'Emissions (tonnes CO2/year)': [transportation_emissions, electricity_emissions, diet_emissions, waste_emissions]
    })

    chart = alt.Chart(df).mark_bar().encode(
        x='Category',
        y='Emissions (tonnes CO2/year)',
        color='Category'
    ).properties(
        title='Carbon Emissions by Category'
    )

    st.altair_chart(chart, use_container_width=True)
