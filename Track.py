import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode
from streamlit_folium import st_folium

st.title("📍 Phone Number Location Tracker")
# st.write("Enter a phone number (with country code) to track its location.")

number = st.text_input("Enter a number with country code (e.g., +14155552671):")

key = "ca360cb4e53d4cf6a8c39febffd80afd"
geo_coder = OpenCageGeocode(key)

if "map_data" not in st.session_state:
    st.session_state.map_data = None

if st.button("Track Location"):
    if number:
        try:
            check_number = phonenumbers.parse(number)
            num_loc = geocoder.description_for_number(check_number, "en")
            num_carrier = carrier.name_for_number(check_number, "en")

            st.success(f"📍 Location: {num_loc}")
            st.info(f"📞 Carrier: {num_carrier}")

            results = geo_coder.geocode(num_loc)

            if results:
                full_location = results[0]['formatted']
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']

                st.write(f"🌍 Full Location: {full_location}")
                st.write(f"🗺 Latitude: {lat}, Longitude: {lng}")

                map_loc = folium.Map(location=[lat, lng], zoom_start=9)
                folium.Marker([lat, lng], popup=num_loc).add_to(map_loc)
                st.session_state.map_data = map_loc
            
            else:
                st.error("Could not retrieve location coordinates.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid phone number!")

if st.session_state.map_data:
    st_folium(st.session_state.map_data, width=700, height=500)
