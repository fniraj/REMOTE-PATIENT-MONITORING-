import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import errorcode

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xxxxxxx',
    'database': 'hospital_db'
}

# Fetch specialties from the database
def fetch_specialties():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("SELECT specialty_id, specialty_name FROM Specialties")
        specialties = cursor.fetchall()
        cursor.close()
        cnx.close()
        return specialties
    except mysql.connector.Error as err:
        print(err)
        return []

# Fetch doctors based on selected specialty from the database
def fetch_doctors(specialty_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("SELECT doctor_id, doctor_name FROM Doctors WHERE specialty_id = %s", (specialty_id,))
        doctors = cursor.fetchall()
        cursor.close()
        cnx.close()
        return doctors
    except mysql.connector.Error as err:
        print(err)
        return []

def update_doctor_dropdown(*args):
    specialty_id = int(specialty_var.get().split()[0])
    doctors = fetch_doctors(specialty_id)
    doctor_var.set('')
    doctor_menu['menu'].delete(0, 'end')
    for doctor_id, doctor_name in doctors:
        doctor_menu['menu'].add_command(label=doctor_name, command=lambda name=doctor_name: doctor_var.set(f"{doctor_id} {doctor_name}"))

def submit_patient_info():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    age = age_entry.get()
    sex = sex_var.get()
    specialty_id = int(specialty_var.get().split()[0])
    doctor_id = int(doctor_var.get().split()[0])
    issue_description = issue_description_entry.get("1.0", tk.END).strip()
    email = email_entry.get()

    if not all([first_name, last_name, age, sex, specialty_id, doctor_id, issue_description, email]):
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        add_patient = ("INSERT INTO Patients (first_name, last_name, age, sex, specialty_id, doctor_id, issue_description, email) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        data_patient = (first_name, last_name, age, sex, specialty_id, doctor_id, issue_description, email)

        cursor.execute(add_patient, data_patient)
        cnx.commit()

        cursor.close()
        cnx.close()

        messagebox.showinfo("Success", "Patient information submitted successfully!")
        clear_patient_form()
    except mysql.connector.Error as err:
        print(err)
        messagebox.showerror("Error", "Failed to save patient information.")

def clear_patient_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    sex_var.set('')
    specialty_var.set('')
    doctor_var.set('')
    issue_description_entry.delete("1.0", tk.END)
    email_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Patient Information")

# Input fields
tk.Label(root, text="First Name:").grid(row=0, column=0)
tk.Label(root, text="Last Name:").grid(row=1, column=0)
tk.Label(root, text="Age:").grid(row=2, column=0)
tk.Label(root, text="Sex:").grid(row=3, column=0)
tk.Label(root, text="Specialty:").grid(row=4, column=0)
tk.Label(root, text="Doctor:").grid(row=5, column=0)
tk.Label(root, text="Issue Description:").grid(row=6, column=0)
tk.Label(root, text="Email:").grid(row=7, column=0)

first_name_entry = tk.Entry(root)
last_name_entry = tk.Entry(root)
age_entry = tk.Entry(root)
issue_description_entry = tk.Text(root, height=5, width=40)
email_entry = tk.Entry(root)

sex_var = tk.StringVar(root)
sex_menu = ttk.OptionMenu(root, sex_var, "", "Male", "Female")
sex_menu.grid(row=3, column=1)

specialty_var = tk.StringVar(root)
doctor_var = tk.StringVar(root)

specialties = fetch_specialties()
specialty_menu = ttk.OptionMenu(root, specialty_var, "", *[f"{s[0]} {s[1]}" for s in specialties], command=update_doctor_dropdown)
specialty_menu.grid(row=4, column=1)
doctor_menu = ttk.OptionMenu(root, doctor_var, "")
doctor_menu.grid(row=5, column=1)

first_name_entry.grid(row=0, column=1)
last_name_entry.grid(row=1, column=1)
age_entry.grid(row=2, column=1)
issue_description_entry.grid(row=6, column=1)
email_entry.grid(row=7, column=1)

tk.Button(root, text="Submit", command=submit_patient_info).grid(row=8, column=0, columnspan=2)

root.mainloop()
