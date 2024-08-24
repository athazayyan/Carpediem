import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import json
from difflib import get_close_matches
from pathlib import Path
import sqlite3
from sqlite3 import Error

test = st.sidebar.radio("Pilihan Menu", ["Banding Univ", "chatbot-bantu-persiapan IISMA"])

if test == "chatbot-bantu-persiapan IISMA":
   


    # Function to create a database connection
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            st.error(f"Error: {e}")
        return conn

    # Function to create the knowledge table
    def create_table(conn):
        try:
            sql_create_table = """ 
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            ); 
            """
            c = conn.cursor()
            c.execute(sql_create_table)
        except Error as e:
            st.error(f"Error: {e}")

    # Function to insert a new entry
    def add_knowledge(conn, question, answer):
        sql = ''' 
        INSERT INTO knowledge(question, answer)
        VALUES(?, ?)
        '''
        cur = conn.cursor()
        cur.execute(sql, (question, answer))
        conn.commit()
        return cur.lastrowid

    # Function to query the database
    def get_knowledge(conn, question):
        cur = conn.cursor()
        cur.execute("SELECT answer FROM knowledge WHERE question=?", (question,))
        rows = cur.fetchall()
        return rows

    # Main function for Streamlit
    def main():
        st.title("Chatbot with SQLite")

        database = "knowledge.db"  # Your SQLite database file

        # Create connection to database
        conn = create_connection(database)

        # Create table if not exists
        if conn:
            create_table(conn)

        question = st.text_input("Ask a question:")

        if st.button("Submit"):
            if question:
                answer = get_knowledge(conn, question)
                if answer:
                    st.write(f"Answer: {answer[0][0]}")
                else:
                    st.write("I don't know the answer. Please teach me.")
                    new_answer = st.text_input("Your answer:")
                    if st.button("Add to database"):
                        if new_answer:
                            add_knowledge(conn, question, new_answer)
                            st.success("Knowledge added successfully!")
                        else:
                            st.error("Please provide an answer before adding to the database.")
            else:
                st.error("Please enter a question.")

    if __name__ == '__main__':
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
                        st.text("")  



