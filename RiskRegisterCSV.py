##Author: Andrew Kubat
##Purpose: CSV portion of the Risk Register Automated Management System (RRAMS). This file may be unused, depending on how development goes.

def main():
    print("Might be deleted soon, still planning the project out.")

import csv
from datetime import datetime

# Function to add a new risk entry to the CSV file
def add_risk_csv(file_path, description):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([description, date_now, date_now])
    print("Risk added to CSV successfully.")

# Function to read all risk entries from the CSV file
def read_all_risks_csv(file_path):
    risks = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            risks.append(row)
    return risks

# Function to update a specific risk entry in the CSV file
def edit_risk_csv(file_path, risk_id, new_description):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    risks = read_all_risks_csv(file_path)
    risks[risk_id][0] = new_description
    risks[risk_id][2] = date_now
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(risks)
    print("Risk updated in CSV successfully.")

# Function to delete a specific risk entry from the CSV file
def delete_risk_csv(file_path, risk_id):
    risks = read_all_risks_csv(file_path)
    risks.pop(risk_id)
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(risks)
    print("Risk deleted from CSV successfully.")
