import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import errorcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xxxxxx',
    'database': 'hospital_db'
}

# Fetch doctors from the database
def fetch_doctors():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("SELECT doctor_id, doctor_name FROM Doctors")
        doctors = cursor.fetchall()
        cursor.close()
        cnx.close()
        return doctors
    except mysql.connector.Error as err:
        print(err)
        return []

# Fetch patients based on selected doctor from the database
def fetch_patients(doctor_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("SELECT patient_id, first_name, last_name, age, sex, issue_description, email FROM Patients WHERE doctor_id = %s", (doctor_id,))
        patients = cursor.fetchall()
        cursor.close()
        cnx.close()
        return patients
    except mysql.connector.Error as err:
        print(err)
        return []

def update_patient_tree(*args):
    doctor_id = int(doctor_var.get().split()[0])
    patients = fetch_patients(doctor_id)
    for item in patient_tree.get_children():
        patient_tree.delete(item)
    for row in patients:
        patient_tree.insert("", "end", values=row)

def send_email(patient_email, prescription):
    msg = MIMEMultipart()
    msg['From'] = 'nirajaiims84@gmail.com'
    msg['To'] = patient_email
    msg['Subject'] = 'Your Prescription'

    msg.attach(MIMEText(prescription))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login('nirajaiims84@gmail.com', 'pnostoxlwaeipkwu ')
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def prescribe_medicine():
    selected_item = patient_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient.")
        return

    patient_info = patient_tree.item(selected_item)['values']
    prescription = prescription_text.get("1.0", tk.END).strip()

    if not prescription:
        messagebox.showerror("Error", "Please enter the prescription.")
        return

    send_email(patient_info[-1], prescription)
    messagebox.showinfo("Success", "Prescription sent successfully!")
    prescription_text.delete("1.0", tk.END)

root = tk.Tk()
root.title("Doctor's Dashboard")

# Doctor dropdown
tk.Label(root, text="Select Doctor:").pack()
doctor_var = tk.StringVar(root)
doctors = fetch_doctors()
doctor_menu = ttk.OptionMenu(root, doctor_var, "", *[f"{d[0]} {d[1]}" for d in doctors], command=update_patient_tree)
doctor_menu.pack()

# Patient tree view
columns = ("ID", "First Name", "Last Name", "Age", "Sex", "Issue Description", "Email")
patient_tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    patient_tree.heading(col, text=col)

patient_tree.pack(fill=tk.BOTH, expand=True)

# Prescription input
tk.Label(root, text="Enter Prescription:").pack()
prescription_text = tk.Text(root, height=10, width=50)
prescription_text.pack()

tk.Button(root, text="Prescribe Medicine", command=prescribe_medicine).pack()

root.mainloop()
