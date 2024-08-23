import streamlit as st
import requests
from bs4 import BeautifulSoup

url_list = {
    "University of Michigan": "https://iisma.kemdikbud.go.id/info/s80-university-of-michigan/",
    "NYU": "https://iisma.kemdikbud.go.id/info/s83-new-york-university/",
    "Georgetown": "https://iisma.kemdikbud.go.id/info/s82-georgetown-university/",
    "Boston University": "https://iisma.kemdikbud.go.id/info/31-boston-university-metropolitan-college/",
}

st.title("Bandingkan Universitas IISMA Pilihanmu")

selected_universities = st.multiselect("Choose universities to compare", list(url_list.keys()))

if st.button("Fetch and Compare Information"):
    if not selected_universities:
        st.warning("Please select at least one university.")
    else:
        comparison_data = {}
        for university in selected_universities:
            url = url_list[university]
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                university_data = {}
                for section, data_tab in [("Requirements", '2'), ("Academic Period", '3'), ("Statistics on Intake", '4')]:
                    tab = soup.find('div', {'data-tab': data_tab, 'role': 'tabpanel'})
                    if tab:
                        content = tab.get_text(strip=True, separator='\n')
                        university_data[section] = content
                    else:
                        university_data[section] = "Not found"
                
                comparison_data[university] = university_data

            except requests.RequestException as e:
                st.error(f"Error fetching data for {university}: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred for {university}: {str(e)}")
        
        # Display comparison
        if comparison_data:
            for section in ["Requirements", "Academic Period", "Statistics on Intake"]:
                st.subheader(section)
                for university in selected_universities:
                    st.text(f"{university}:")
                    st.text(comparison_data[university].get(section, "Not available"))
                    st.text("")  # Add spacing between universities

