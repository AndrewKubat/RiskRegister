##Author: Andrew Kubat
##Purpose: SQL portion of the Risk Register Automated Management System (RRAMS). This file may be unused, depending on how development goes.

def main():
    print("Might be deleted soon, still planning the project out.")


import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('risk_reg.db')
cursor = conn.cursor()

# Create the Risk Register table
cursor.execute('''
CREATE TABLE IF NOT EXISTS RiskRegister (
    RiskID INTEGER PRIMARY KEY AUTOINCREMENT,
    RiskDescription TEXT NOT NULL,
    DateCreated TEXT NOT NULL,
    DateLastEdited TEXT NOT NULL
)
''')

# Function to add a new risk entry
def add_risk(description):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO RiskRegister (RiskDescription, DateCreated, DateLastEdited)
    VALUES (?, ?, ?)
    ''', (description, date_now, date_now))
    conn.commit()
    print("Risk added successfully.")

# Function to edit an existing risk entry
def edit_risk(risk_id, new_description):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    UPDATE RiskRegister
    SET RiskDescription = ?, DateLastEdited = ?
    WHERE RiskID = ?
    ''', (new_description, date_now, risk_id))
    conn.commit()
    print("Risk updated successfully.")

# Function to delete a risk entry
def delete_risk(risk_id):
    cursor.execute('''
    DELETE FROM RiskRegister
    WHERE RiskID = ?
    ''', (risk_id,))
    conn.commit()
    print("Risk deleted successfully.")

# Function to retrieve and print all risk entries
def view_all_risks():
    cursor.execute('SELECT * FROM RiskRegister')
    risks = cursor.fetchall()
    for risk in risks:
        print(risk)

# Example usage
add_risk('This is a sample risk description.')
view_all_risks()
edit_risk(1, 'This is an updated risk description.')
view_all_risks()
delete_risk(1)
view_all_risks()

# Close the connection
conn.close()