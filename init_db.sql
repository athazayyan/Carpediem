
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);


INSERT INTO knowledge (question, answer) VALUES 
    ('What is Streamlit?', 'Streamlit is an open-source app framework for Machine Learning and Data Science projects.'),
    ('What is Pillow?', 'Pillow is a Python Imaging Library (PIL) fork that provides various image processing capabilities.'),
    ('How do you use BeautifulSoup?', 'BeautifulSoup is used for web scraping by parsing HTML or XML documents.'),
    ('What is SQLite?', 'SQLite is a lightweight, disk-based database that doesn’t require a separate server process.'),
    ('How to install requests library?', 'You can install the requests library using the command `pip install requests`.');
