import hashlib
import time
from collections import OrderedDict
import streamlit as st

# This will represent our ledger as a list of dictionaries for better structure
ledger = []

def get_report_card_hash(report_card):
    return hashlib.sha256(report_card.encode()).hexdigest()

def generate_report_card(student_name, grades, previous_hash=None):
    timestamp = time.time()  # Get the current timestamp
    report_card = OrderedDict({
        'timestamp': timestamp,
        'student_name': student_name,
        'grades': grades,
        'previous_hash': previous_hash or 'Genesis'
    })
    
    # Convert the report card dictionary to a string representation
    report_card_str = f"Timestamp: {timestamp}\nStudent Name: {student_name}\n"
    for subject, grade in grades.items():
        report_card_str += f"{subject}: {grade}\n"
    report_card_str += f"Previous Hash: {previous_hash or 'Genesis'}\n"
    
    # Append the report card to the ledger
    ledger.append(report_card)

    # Return the report card string and its hash
    return report_card_str, get_report_card_hash(report_card_str)

def verify_ledger():
    for i in range(1, len(ledger)):
        current_report = ledger[i]
        previous_report = ledger[i - 1]
        
        # Get the current report's previous hash
        current_previous_hash = current_report['previous_hash']
        
        # Generate the hash of the previous report card
        previous_report_str = f"Timestamp: {previous_report['timestamp']}\nStudent Name: {previous_report['student_name']}\n"
        for subject, grade in previous_report['grades'].items():
            previous_report_str += f"{subject}: {grade}\n"
        previous_report_str += f"Previous Hash: {previous_report['previous_hash']}\n"
        
        # Calculate the hash of the previous report
        calculated_previous_hash = get_report_card_hash(previous_report_str)
        
        # Compare the hashes
        if current_previous_hash != calculated_previous_hash:
            return False  # Ledger is corrupted

    return True  # Ledger is valid

# Streamlit UI
st.title("Report Card Ledger")

student_name = st.text_input("Enter Student Name", "Alice")
math_grade = st.text_input("Enter Math Grade", "A")
science_grade = st.text_input("Enter Science Grade", "B")

# Generate the first report card
if st.button("Generate Report Card for Alice"):
    report_card1_str, report_card1_hash = generate_report_card(student_name, {"Math": math_grade, "Science": science_grade})
    st.subheader("Generated Report Card")
    st.text(report_card1_str)
    st.text(f"Hash: {report_card1_hash}")

    # Generate second report card
    student_name2 = st.text_input("Enter Student Name for Second Report Card", "Bob")
    math_grade2 = st.text_input("Enter Math Grade for Second Report Card", "B")
    english_grade2 = st.text_input("Enter English Grade for Second Report Card", "A")

    if st.button("Generate Report Card for Bob"):
        report_card2_str, report_card2_hash = generate_report_card(student_name2, {"Math": math_grade2, "English": english_grade2}, previous_hash=report_card1_hash)
        st.subheader("Generated Report Card for Bob")
        st.text(report_card2_str)
        st.text(f"Hash: {report_card2_hash}")

# Verify the ledger's integrity
if st.button("Verify Ledger Integrity"):
    is_ledger_valid = verify_ledger()
    st.subheader(f"Ledger Integrity: {'Valid' if is_ledger_valid else 'Corrupted'}")
