import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import json
import os
from difflib import get_close_matches
import folium
from streamlit_folium import st_folium
import re
import pandas as pd
import plotly.graph_objects as go

test = st.sidebar.radio("Pilihan Menu", ["Banding Univ", "chatbot-bantu-persiapan IISMA", "Univ Map"])
if test == "chatbot-bantu-persiapan IISMA":
    JSON_FILE = os.path.join(os.path.dirname(__file__), "ilmu.json")
    st.image("penyu2.png")
    def akses_ilmu(file_path: str) -> dict:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return {"input": []}
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_ilmu(file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def cari_jawaban(user_input: str, inputs: list[str]) -> str | None:
        matches = get_close_matches(user_input, inputs, n=1, cutoff=0.8)
        return matches[0] if matches else None

    def dapat_jawaban(input: str, basis_ilmu: dict) -> str | None:
        for q in basis_ilmu["input"]:
            if q["input"].lower() == input.lower():
                return q["output"]
        return None

    def tambah_pengetahuan(pertanyaan: str, jawaban: str):
        basis_ilmu = akses_ilmu(JSON_FILE)
        basis_ilmu["input"].append({"input": pertanyaan, "output": jawaban})
        save_ilmu(JSON_FILE, basis_ilmu)

    def main():
        st.title("Penyu dan IISMA-Mu")
        st.text("Kalau aku tak tahu, bisa train aku ya") 
        st.text("usahakan pakai bahasa Inggris")
        col1, col2, col3 = st.columns([3, 1]) 
        with col2:
            if 'pertanyaan' not in st.session_state:
                st.session_state.pertanyaan = ""

            pertanyaan = st.text_area("Anda:", value=st.session_state.pertanyaan, height=100)
            st.session_state.pertanyaan = pertanyaan

            if st.button("Tanya"):
                if pertanyaan:
                    basis_ilmu = akses_ilmu(JSON_FILE)
                    best_match = cari_jawaban(pertanyaan, [q["input"] for q in basis_ilmu["input"]])

                    if best_match:
                        output = dapat_jawaban(best_match, basis_ilmu)
                        st.write(f"Bot: {output}")
                    else:
                        st.write("Bot: Maaf, saya tidak mengerti pertanyaan Anda. Ajarin saya dong!")

                        jawaban_baru = st.text_area("Jawaban yang benar:", height=100)
                        if st.button("Simpan Jawaban"):
                            if jawaban_baru.lower() != "skip":
                                tambah_pengetahuan(pertanyaan, jawaban_baru)
                                st.success(f"Pengetahuan baru ditambahkan: '{pertanyaan}': '{jawaban_baru}'")
                            else:
                                st.info("Pertanyaan dilewati.")
                else:
                    st.warning("Mohon masukkan pertanyaan terlebih dahulu.")


    if __name__ == "__main__":
        main()


if test == "Banding Univ":
    url_list = {
        "University of Michigan": "https://iisma.kemdikbud.go.id/info/s80-university-of-michigan/",
        "NYU": "https://iisma.kemdikbud.go.id/info/s83-new-york-university/",
        "Georgetown": "https://iisma.kemdikbud.go.id/info/s82-georgetown-university/",
        "Boston University": "https://iisma.kemdikbud.go.id/info/31-boston-university-metropolitan-college/",
        "University of Toronto": "https://iisma.kemdikbud.go.id/info/s100-university-of-toronto/",
        "Arizona State University": "https://iisma.kemdikbud.go.id/info/56-arizona-state-university/",
        "University of Pennsylvania": "https://iisma.kemdikbud.go.id/info/05-the-university-of-pennsylvania-college-of-liberal-and-professional-studies/",
        "Yale University": "https://iisma.kemdikbud.go.id/info/06-yale-university/",
        "Penn State University": "https://iisma.kemdikbud.go.id/info/29-penn-state-university",
        "University of California, Davis": "https://iisma.kemdikbud.go.id/info/30-university-of-california-davis/",
        "UC Chile": "https://iisma.kemdikbud.go.id/info/35-uc-chile/",
        "Michigan State University": "https://iisma.kemdikbud.go.id/info/45-michigan-state-university/",
        "University of Colorado Boulder": "https://iisma.kemdikbud.go.id/info/64-university-of-colorado-boulder/",
        "University of British Columbia": "https://iisma.kemdikbud.go.id/info/13-university-of-british-columbia/",
        "University of Waterloo": "https://iisma.kemdikbud.go.id/info/42-university-of-waterloo/",
        "Western University": "https://iisma.kemdikbud.go.id/info/46-western-university/",
        "University of Chicago": "https://iisma.kemdikbud.go.id/info/03-university-of-chicago/",
        "University of Texas at Austin": "https://iisma.kemdikbud.go.id/info/21-university-of-texas-at-austin/",
        "Cornell University": "https://iisma.kemdikbud.go.id/info/79-cornell-university/",
        "National Taiwan Normal University": "https://iisma.kemdikbud.go.id/info/s88-national-taiwan-normal-university/",
        "National Sun Yat-sen University": "https://iisma.kemdikbud.go.id/info/s116-national-sun-yat-sen-university/",
        "Prince of Songkla University": "https://iisma.kemdikbud.go.id/info/s90-prince-of-songkla-university/",
        "Mahidol University": "https://iisma.kemdikbud.go.id/info/s118-mahidol-university/",
        "Osaka University": "https://iisma.kemdikbud.go.id/info/18-osaka-university/",
        "Singapore Management University": "https://iisma.kemdikbud.go.id/info/74-singapore-management-university/",
        "Hanyang University": "https://iisma.kemdikbud.go.id/info/44-hanyang-university-seoul-campus/",
        "National Taiwan University of Science and Technology": "https://iisma.kemdikbud.go.id/info/71-national-taiwan-university-of-science-and-technology-taiwan-tech",
        "Korea University": "https://iisma.kemdikbud.go.id/info/23-korea-university/",
        "Universiti Malaya": "https://iisma.kemdikbud.go.id/info/17-universiti-malaya/",
        "Universiti Kebangsaan Malaysia": "https://iisma.kemdikbud.go.id/info/38-universiti-kebangsaan-malaysia/",
        "Universiti Sains Malaysia": "https://iisma.kemdikbud.go.id/info/40-universiti-sains-malaysia/",
        "Nanyang Technological University": "https://iisma.kemdikbud.go.id/info/04-nanyang-technological-university/",
        "Keio University": "https://iisma.kemdikbud.go.id/info/52-keio-university/",
        "National Taiwan University": "https://iisma.kemdikbud.go.id/info/18-national-taiwan-university/",
        "Chulalongkorn University": "https://iisma.kemdikbud.go.id/info/55-chulalongkorn-university/",
        "Middle East Technical University": "https://iisma.kemdikbud.go.id/info/73-middle-east-technical-university/",
        "Sophia University": "https://iisma.kemdikbud.go.id/info/s98-sophia-university/",
        "Taipei Medical University": "https://iisma.kemdikbud.go.id/info/s117-taipei-medical-university-tmu/",
        "National University of Singapore": "https://iisma.kemdikbud.go.id/info/s112-national-university-of-singapore-nus/",
        "National Cheng Kung University": "https://iisma.kemdikbud.go.id/info/s115-national-cheng-kung-university-ncku/",
        "University of New South Wales": "https://iisma.kemdikbud.go.id/info/12-university-of-new-south-wales/",
        "University of Canterbury": "https://iisma.kemdikbud.go.id/info/66-university-of-canterbury/",
        "Massey University": "https://iisma.kemdikbud.go.id/info/s111-massey-university/",
        "University of Waikato": "https://iisma.kemdikbud.go.id/info/s120-university-of-waikato/",
        "Australian National University": "https://iisma.kemdikbud.go.id/info/09-the-australian-national-university/",
        "University of Adelaide": "https://iisma.kemdikbud.go.id/info/32-the-university-of-adelaide/",
        "University of Queensland": "https://iisma.kemdikbud.go.id/info/14-the-university-of-queensland/",
        "University of Sydney": "https://iisma.kemdikbud.go.id/info/11-university-of-sydney/",
        "University of Auckland": "https://iisma.kemdikbud.go.id/info/25-university-of-auckland/",
        "University of Melbourne": "https://iisma.kemdikbud.go.id/info/10-university-of-melbourne/",
        "Monash University": "https://iisma.kemdikbud.go.id/info/15-monash-university/",
        "University of Western Australia": "https://iisma.kemdikbud.go.id/info/27-the-university-of-western-australia/",
        "University of Otago": "https://iisma.kemdikbud.go.id/info/51-university-of-otago/",
        "Victoria University of Wellington": "https://iisma.kemdikbud.go.id/info/62-victoria-university-of-wellington/",
        "University of Granada": "https://iisma.kemdikbud.go.id/info/s89-university-of-granada/",
        "KTH Royal Institute of Technology": "https://iisma.kemdikbud.go.id/info/s113-kth-royal-institute-of-technology/",
        "Lund University": "https://iisma.kemdikbud.go.id/info/s114-lund-university/",
        "Palacký University Olomouc": "https://iisma.kemdikbud.go.id/info/76-palacky-university-olomouc/",
        "Vrije Universiteit Amsterdam": "https://iisma.kemdikbud.go.id/info/54-vrije-universiteit-amsterdam/",
        "Leiden University": "https://iisma.kemdikbud.go.id/info/73-leiden-university/",
        "Maastricht University": "https://iisma.kemdikbud.go.id/info/59-maastricht-university/",
        "KU Leuven": "https://iisma.kemdikbud.go.id/info/20-ku-leuven/",
        "University of Szeged": "https://iisma.kemdikbud.go.id/info/75-university-of-szeged",
        "University of Pisa": "https://iisma.kemdikbud.go.id/info/72-university-of-pisa/",
        "Humboldt University of Berlin": "https://iisma.kemdikbud.go.id/info/37-humboldt-universitat-zu-berlin/",
        "University of Zagreb": "https://iisma.kemdikbud.go.id/info/77-university-of-zagreb/",
        "University of Warsaw": "https://iisma.kemdikbud.go.id/info/68-university-of-warsaw/",
        "Lomonosov Moscow State University": "https://iisma.kemdikbud.go.id/info/24-m-v-lomonosov-moscow-state-university/",
        "Radboud University": "https://iisma.kemdikbud.go.id/info/57-radboud-university/",
        "Vytautas Magnus University": "https://iisma.kemdikbud.go.id/info/78-vytautas-magnus-university/",
        "Sciences Po": "https://iisma.kemdikbud.go.id/info/lolos-67-sciences-po/",
        "Universitat Pompeu Fabra": "https://iisma.kemdikbud.go.id/info/60-universitat-pompeu-fabra/",
        "Sapienza University of Rome": "https://iisma.kemdikbud.go.id/info/47-sapienza-university-of-rome/",
        "University of Padua": "https://iisma.kemdikbud.go.id/info/63-university-of-padua/",
        "Universidad Autonoma de Madrid": "https://iisma.kemdikbud.go.id/info/53-universidad-autonoma-de-madrid/",
        "University of Groningen": "https://iisma.kemdikbud.go.id/info/s81-university-of-groningen/",
        "Belarusian State University": "https://iisma.kemdikbud.go.id/info/s84-belarusian-state-university/",
        "Aalto University": "https://iisma.kemdikbud.go.id/info/s85-aalto-university/",
        "University of Pécs": "https://iisma.kemdikbud.go.id/info/s86-university-of-pecs/",
        "University of Siena": "https://iisma.kemdikbud.go.id/info/s97-university-of-siena/",
        "Technische Universität Dresden": "https://iisma.kemdikbud.go.id/info/s99-technische-universitat-dresden/",
        "Aix-Marseille University": "https://iisma.kemdikbud.go.id/info/s104-aix-marseille-university/",
        "Université de Caen Normandie": "https://iisma.kemdikbud.go.id/info/s105-universite-de-caen-normandie/",
        "Charles University": "https://iisma.kemdikbud.go.id/info/s106-charles-university/",
        "Saint Petersburg State University": "https://iisma.kemdikbud.go.id/info/s107-saint-petersburg-state-university/",
        "RUDN University": "https://iisma.kemdikbud.go.id/info/s108-peoples-friendship-university-of-russia-rudn-university/",
        "Higher School of Economics": "https://iisma.kemdikbud.go.id/info/s109-higher-school-of-economics-national-research-university/",
        "ITMO University": "https://iisma.kemdikbud.go.id/info/s110-information-technologies-mechanics-and-optics-itmo-university/",
        "University of Limerick": "https://iisma.kemdikbud.go.id/info/s96-university-of-limerick/",
        "University of Southampton": "https://iisma.kemdikbud.go.id/info/s91-university-of-southampton/",
        "Queen's University Belfast": "https://iisma.kemdikbud.go.id/info/s94-queens-university-belfast/",
        "University of Bristol": "https://iisma.kemdikbud.go.id/info/s87-university-of-bristol/",
        "Lancaster University": "https://iisma.kemdikbud.go.id/info/39-lancaster-university/",
        "University of Leicester": "https://iisma.kemdikbud.go.id/info/61-university-of-leicester/",
        "University of Galway": "https://iisma.kemdikbud.go.id/info/65-university-of-galway/",
        "University of Birmingham": "https://iisma.kemdikbud.go.id/info/28-university-of-birmingham/",
        "Newcastle University": "https://iisma.kemdikbud.go.id/info/36-newcastle-university/",
        "University of Edinburgh": "https://iisma.kemdikbud.go.id/info/07-university-of-edinburgh/",
        "University College Dublin": "https://iisma.kemdikbud.go.id/info/48-university-college-dublin/",
        "University College Cork": "https://iisma.kemdikbud.go.id/info/33-university-college-cork/",
        "University of Glasgow": "https://iisma.kemdikbud.go.id/info/22-university-of-glasgow/",
        "University of Liverpool": "https://iisma.kemdikbud.go.id/info/50-university-of-liverpool/",
        "University of Leeds": "https://iisma.kemdikbud.go.id/info/26-university-of-leeds/",
        "University of Sussex": "https://iisma.kemdikbud.go.id/info/58-university-of-sussex/",
        "University of Warwick": "https://iisma.kemdikbud.go.id/info/s16-university-of-warwick/",
        "University of York": "https://iisma.kemdikbud.go.id/info/43-university-of-york/",
        "University College London": "https://iisma.kemdikbud.go.id/info/02-university-college-london/",
        "Queen Mary University of London": "https://iisma.kemdikbud.go.id/info/34-queen-mary-university-of-london/",
        "University of Manchester": "https://iisma.kemdikbud.go.id/info/s87-the-university-of-manchester/",
        "Durham University": "https://iisma.kemdikbud.go.id/info/s92-durham-university/",
        "University of Sheffield": "https://iisma.kemdikbud.go.id/info/s119-the-university-of-sheffield/",
        "Loughborough University": "https://iisma.kemdikbud.go.id/info/s95-loughborough-university/",
        "University of Bath": "https://iisma.kemdikbud.go.id/info/s93-university-of-bath/",
        "University of Limerick": "https://iisma.kemdikbud.go.id/info/s96-university-of-limerick/",
        "University of Southampton": "https://iisma.kemdikbud.go.id/info/s91-university-of-southampton/",
        "Queen's University Belfast": "https://iisma.kemdikbud.go.id/info/s94-queens-university-belfast/",
        "University of Bristol": "https://iisma.kemdikbud.go.id/info/s87-university-of-bristol/",
        "Lancaster University": "https://iisma.kemdikbud.go.id/info/39-lancaster-university/",
        "University of Leicester": "https://iisma.kemdikbud.go.id/info/61-university-of-leicester/",
        "University of Galway": "https://iisma.kemdikbud.go.id/info/65-university-of-galway/",
        "University of Birmingham": "https://iisma.kemdikbud.go.id/info/28-university-of-birmingham/"
    }

    st.title("Bandingkan Universitas IISMA Pilihanmu")

    selected_universities = st.multiselect("Choose universities to compare", list(url_list.keys()), key="university_selector")

    def extract_scores(text):
        toefl = re.search(r'TOEFL iBT:?\s*(\d+)', text)
        ielts = re.search(r'IELTS:?\s*([\d.]+)', text)
        duolingo = re.search(r'Duolingo English Test:?\s*(\d+)', text)
        
        return {
            'TOEFL': int(toefl.group(1)) if toefl else None,
            'IELTS': float(ielts.group(1)) if ielts else None,
            'Duolingo': int(duolingo.group(1)) if duolingo else None
        }

    def extract_intake_stats(text):
        applicants = re.search(r'Applicants\s*:\s*(\d+)', text)
        awardees = re.search(r'Awardees\s*:\s*(\d+)', text)
        stats = {}
        if applicants:
            stats['Applicants'] = int(applicants.group(1))
        if awardees:
            stats['Awardees'] = int(awardees.group(1))
        return stats

    def extract_academic_dates(text):
        start_date = re.search(r'Start Date\s*:\s*(\d{2}/\d{2}/\d{4})', text)
        end_date = re.search(r'End Date\s*:\s*(\d{2}/\d{2}/\d{4})', text)
        return {
            'Start Date': datetime.strptime(start_date.group(1), '%d/%m/%Y') if start_date else None,
            'End Date': datetime.strptime(end_date.group(1), '%d/%m/%Y') if end_date else None
        }
    

    if st.button("Bandingkan", key="banding"):
        if not selected_universities:
            st.warning("Please select at least one university.")
        else:
            comparison_data = {}
            scores_data = {}
            intake_data = {}
            academic_dates = {}
            
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
                            if section == "Requirements":
                                scores_data[university] = extract_scores(content)
                            elif section == "Statistics on Intake":
                                print(f"Raw Statistics on Intake for {university}:")
                                print(content)
                                intake_data[university] = extract_intake_stats(content)
                            elif section == "Academic Period":
                                academic_dates[university] = extract_academic_dates(content)
                        else:
                            university_data[section] = "Not found"
                            
                    comparison_data[university] = university_data
                    
                except requests.RequestException as e:
                    st.error(f"Error fetching data for {university}: {str(e)}")
                except Exception as e:
                    st.error(f"An unexpected error occurred for {university}: {str(e)}")
            
            if comparison_data:
                for section in ["Requirements", "Academic Period", "Statistics on Intake"]:
                    st.subheader(section)
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        for university in selected_universities:
                            st.text(f"{university}:")
                            st.text(comparison_data[university].get(section, "Not available"))
                            st.text("")
                    
                    if section == "Requirements":
                        with col2:
                            df = pd.DataFrame(scores_data).T
                            fig = go.Figure()
                            for score_type in ['TOEFL', 'IELTS', 'Duolingo']:
                                fig.add_trace(go.Bar(
                                    x=df.index,
                                    y=df[score_type],
                                    name=score_type
                                ))
                            fig.update_layout(
                                title="English Test Score Requirements",
                                xaxis_title="University",
                                yaxis_title="Score",
                                barmode='group'
                            )
                            st.plotly_chart(fig)

            
                st.subheader("Statistics on Intake")
                if intake_data:
                    intake_df = pd.DataFrame(intake_data).T
                    if not intake_df.empty and 'Applicants' in intake_df.columns and 'Awardees' in intake_df.columns:
                        fig_intake = go.Figure()
                        for stat in ['Applicants', 'Awardees']:
                            fig_intake.add_trace(go.Bar(
                                x=intake_df.index,
                                y=intake_df[stat],
                                name=stat
                            ))
                        fig_intake.update_layout(
                            title="Applicants and Awardees",
                            xaxis_title="University",
                            yaxis_title="Number of Students",
                            barmode='group'
                        )
                        st.plotly_chart(fig_intake)
                    else:
                        st.warning("Intake data is incomplete or in an unexpected format.")
                else:
                    st.info("No intake data available for the selected universities.")

            
               


    
if test == "Univ Map":
    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    import random

    def display_interactive_university_map():
        st.title("🌍 University Explorer: Around the World in 80 Clicks!")
        st.write("Discover universities globally and test your geography knowledge!")

        universities = {
        "University of Michigan": [42.2780, -83.7382],
        "NYU": [40.7295, -73.9965],
        "Georgetown": [38.9084, -77.0377],
        "Boston University": [42.3505, -71.1054],
        "University of Toronto": [43.6629, -79.3957],
        "Arizona State University": [33.4236, -111.9310],
        "University of Pennsylvania": [39.9526, -75.1652],
        "Yale University": [41.3163, -72.9224],
        "Penn State University": [40.7982, -77.8599],
        "University of California, Davis": [38.5382, -121.7617],
        "UC Chile": [-33.4553, -70.6517],
        "Michigan State University": [42.7010, -84.4828],
        "University of Colorado Boulder": [40.0150, -105.2705],
        "University of British Columbia": [49.2606, -123.2460],
        "University of Waterloo": [43.4723, -80.5449],
        "Western University": [43.0095, -81.2731],
        "University of Chicago": [41.7886, -87.5987],
        "University of Texas at Austin": [30.2849, -97.7341],
        "Cornell University": [42.4533, -76.4736],
        "National Taiwan Normal University": [25.0210, 121.5284],
        "National Sun Yat-sen University": [22.6204, 120.3122],
        "Prince of Songkla University": [7.0077, 100.5161],
        "Mahidol University": [13.7513, 100.5030],
        "Osaka University": [34.6937, 135.5023],
        "Singapore Management University": [1.2944, 103.8557],
        "Hanyang University": [37.5487, 127.0438],
        "National Taiwan University of Science and Technology": [25.0469, 121.5474],
        "Korea University": [37.5890, 127.0020],
        "Universiti Malaya": [3.1298, 101.6581],
        "Universiti Kebangsaan Malaysia": [2.9314, 101.7764],
        "Universiti Sains Malaysia": [5.3556, 100.3230],
        "Nanyang Technological University": [1.3454, 103.6831],
        "Keio University": [35.6499, 139.7104],
        "National Taiwan University": [25.0141, 121.5397],
        "Chulalongkorn University": [13.7400, 100.5334],
        "Middle East Technical University": [39.8666, 32.5837],
        "Sophia University": [35.6928, 139.7036],
        "Taipei Medical University": [25.0343, 121.5645],
        "National University of Singapore": [1.2966, 103.7764],
        "National Cheng Kung University": [22.9991, 120.2152],
        "University of New South Wales": [-33.9189, 151.2334],
        "University of Canterbury": [-43.5236, 172.6362],
        "Massey University": [-40.3530, 175.6072],
        "University of Waikato": [-37.7870, 175.2836],
        "Australian National University": [-35.3075, 149.1244],
        "University of Adelaide": [-34.9212, 138.5994],
        "University of Queensland": [-27.4974, 153.0120],
        "University of Sydney": [-33.8889, 151.2070],
        "University of Auckland": [-36.8485, 174.7633],
        "University of Melbourne": [-37.8136, 144.9631],
        "Monash University": [-37.9128, 145.1344],
        "University of Western Australia": [-31.9505, 115.8605],
        "University of Otago": [-45.8742, 170.5036],
        "Victoria University of Wellington": [-41.2924, 174.7787],
        "University of Granada": [37.1882, -3.6067],
        "KTH Royal Institute of Technology": [59.3470, 18.0728],
        "Lund University": [55.7052, 13.1910],
        "Palacký University Olomouc": [49.5947, 17.2510],
        "Vrije Universiteit Amsterdam": [52.3333, 4.8667],
        "Leiden University": [52.1601, 4.4981],
        "Maastricht University": [50.8514, 5.6900],
        "KU Leuven": [50.8796, 4.7009],
        "University of Szeged": [46.2530, 20.1411],
        "University of Pisa": [43.7166, 10.4016],
        "Humboldt University of Berlin": [52.5176, 13.3882],
        "University of Zagreb": [45.8150, 15.9819],
        "University of Warsaw": [52.2298, 21.0118],
        "Lomonosov Moscow State University": [55.7023, 37.5731],
        "Radboud University": [51.8424, 5.8730],
        "Vytautas Magnus University": [54.8970, 23.9036],
        "Sciences Po": [48.8550, 2.3322],
        "Universitat Pompeu Fabra": [41.3791, 2.1895],
        "Sapienza University of Rome": [41.9031, 12.4564],
        "University of Padua": [45.4064, 11.8768],
        "Universidad Autonoma de Madrid": [40.4594, -3.6884],
        "University of Groningen": [53.2194, 6.5665],
        "Belarusian State University": [53.9006, 27.5590],
        "Aalto University": [60.2955, 24.7136],
        "University of Pécs": [46.0792, 18.2334],
        "University of Siena": [43.3188, 11.3308],
        "Technische Universität Dresden": [51.0504, 13.7373],
        "Aix-Marseille University": [43.2965, 5.3698],
        "Université de Caen Normandie": [49.4144, -0.6885],
        "Charles University": [50.0755, 14.4378],
        "Saint Petersburg State University": [59.9386, 30.3141],
        "RUDN University": [55.7176, 37.6260],
        "Higher School of Economics": [55.7590, 37.6173],
        "ITMO University": [59.9343, 30.3351],
        "University of Limerick": [52.6648, -8.6267],
        "University of Southampton": [50.9268, -1.3966],
        "Queen's University Belfast": [54.5973, -5.9301],
        "University of Bristol": [51.4545, -2.5879],
        "Lancaster University": [54.0482, -2.8008],
        "University of Leicester": [52.6369, -1.1398],
        "University of Galway": [53.2767, -9.0568],
        "University of Birmingham": [52.3784, -1.3004],
        "Newcastle University": [54.9784, -1.6174],
        "University of Edinburgh": [55.9444, -3.1883],
        "University College Dublin": [53.3065, -6.2224],
        "Syiah Kuala University": [5.5502, 95.3164],
        "University College Cork": [51.8970, -8.4706]
    }

       
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'visited' not in st.session_state:
            st.session_state.visited = set()

        
        with st.sidebar:
            st.header("🏆 Explorer Stats")
            st.metric("Score", st.session_state.score)
            st.metric("Universities Visited", len(st.session_state.visited))
            if st.button("Reset Game"):
                st.session_state.score = 0
                st.session_state.visited = set()
                st.experimental_rerun()

        # Search and Quiz mode
        mode = st.radio("Choose your mode:", ["🔍 Search", "❓ Quiz"])

        m = folium.Map(location=[20, 0], zoom_start=2)

        def get_marker_color(name):
            if name in st.session_state.visited:
                return 'green'
            return 'blue'

        # Add markers for all universities
        for name, coord in universities.items():
            color = get_marker_color(name)
            folium.Marker(
                location=coord,
                popup=name,
                icon=folium.Icon(color=color, icon='university')
            ).add_to(m)

        if mode == "🔍 Search":
            search_query = st.text_input("🔍 Search for a university:", 
                                        help="Enter a university name to highlight it on the map")
            if search_query:
                matching_universities = {name: coord for name, coord in universities.items() 
                                        if search_query.lower() in name.lower()}
                if matching_universities:
                    first_match = list(matching_universities.values())[0]
                    m.location = first_match
                    m.zoom_start = 8
                    for name in matching_universities:
                        if name not in st.session_state.visited:
                            st.session_state.score += 10
                            st.session_state.visited.add(name)
                    st.success(f"You've discovered {len(matching_universities)} new universities! +{len(matching_universities) * 10} points!")
                else:
                    st.warning("No matching universities found. Try another search!")

        elif mode == "❓ Quiz":
            if 'quiz_university' not in st.session_state or st.button("New Question"):
                st.session_state.quiz_university = random.choice(list(universities.keys()))
            
            st.write(f"Where is **{st.session_state.quiz_university}** located?")
            user_guess = [
                st.number_input("Latitude", -90.0, 90.0, 0.0),
                st.number_input("Longitude", -180.0, 180.0, 0.0)
            ]
            
            if st.button("Check Answer"):
                actual_location = universities[st.session_state.quiz_university]
                distance = ((user_guess[0] - actual_location[0])**2 + (user_guess[1] - actual_location[1])**2)**0.5
                
                if distance < 5:
                    points = 50
                    st.balloons()
                    st.success(f"Excellent! You're within 5 degrees. +{points} points!")
                elif distance < 10:
                    points = 30
                    st.success(f"Great! You're within 10 degrees. +{points} points!")
                elif distance < 20:
                    points = 10
                    st.info(f"Not bad! You're within 20 degrees. +{points} points!")
                else:
                    points = 0
                    st.error("Oops! That's quite far off. Try again!")
                
                st.session_state.score += points
                if st.session_state.quiz_university not in st.session_state.visited:
                    st.session_state.visited.add(st.session_state.quiz_university)
                
                m.location = actual_location
                m.zoom_start = 4
                folium.Marker(
                    location=actual_location,
                    popup=st.session_state.quiz_university,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)

       
        st_folium(m, width=725, height=500)

      
        st.info("📌 Blue: Undiscovered | 🟢 Green: Visited | 🔴 Red: Quiz Answer")
        st.write(f"Total universities: {len(universities)} | Discovered: {len(st.session_state.visited)}")

    if __name__ == "__main__":
        display_interactive_university_map()
