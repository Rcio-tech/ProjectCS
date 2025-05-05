import streamlit as st
import pandas as pd
import pydeck as pdk
from Feature_API import autocomplete_address, get_coordinates, get_route_info

st.set_page_config(page_title="🗺️ Address Route Mapper", layout="centered")
st.title("📍 Route Finder with Autocomplete")

# --- START ADDRESS ---
start_query = st.text_input("Start Address")
start_suggestions = []
selected_start = None

if len(start_query) >= 3:
    try:
        start_suggestions = autocomplete_address(start_query)
        selected_start = st.selectbox("Choose Start Location", start_suggestions)
    except Exception as e:
        st.error(f"Start autocomplete failed: {e}")

# --- END ADDRESS ---
end_query = st.text_input("Destination Address")
end_suggestions = []
selected_end = None

if len(end_query) >= 3:
    try:
        end_suggestions = autocomplete_address(end_query)
        selected_end = st.selectbox("Choose Destination", end_suggestions)
    except Exception as e:
        st.error(f"Destination autocomplete failed: {e}")

# --- CALCULATE ROUTE ---
if selected_start and selected_end and st.button("Calculate Route"):
    try:
        # Get coordinates for both locations
        start_coords = get_coordinates(selected_start)
        end_coords = get_coordinates(selected_end)

        # Get route information from API
        route = get_route_info(start_coords, end_coords)

        st.success("Your route has been calculated")
        st.info(f"Distance: **{route['distance_km']:.2f} km**")

        # --- FORMAT DURATION ---
        duration_min = route['duration_min']
        if duration_min >= 60:
            hours = int(duration_min // 60)
            minutes = int(duration_min % 60)
            st.info(f"Duration: **{hours}h {minutes} min**")
        else:
            st.info(f"Duration: **{duration_min:.1f} minutes**")

        # --- PREPARE ROUTE FOR MAP ---
        route_coords = [[lat, lon] for lon, lat in route['geometry']]
        df_route = pd.DataFrame(route_coords, columns=["lat", "lon"])

        # Create consecutive pairs for line segments
        df_route["lon_next"] = df_route["lon"].shift(-1)
        df_route["lat_next"] = df_route["lat"].shift(-1)
        df_route = df_route.dropna()

        midpoint = df_route.iloc[len(df_route) // 2]

        # Create line layer connecting each pair of points
        layer = pdk.Layer(
            "LineLayer",
            data=df_route,
            get_source_position=["lon", "lat"],
            get_target_position=["lon_next", "lat_next"],
            get_color=[0, 0, 255],
            get_width=5
        )

        # Set the view to the route midpoint
        view_state = pdk.ViewState(
            latitude=midpoint["lat"],
            longitude=midpoint["lon"],
            zoom=10
        )

        # Show the map
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    except Exception as e:
        st.error(f"Error computing route: {e}")


