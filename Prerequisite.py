import mysql.connector
from mysql.connector import errorcode

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xxxxxx'
}


def create_database_and_tables():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Create the hospital_db database
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
        cursor.execute("USE hospital_db")

        # Create Specialties table
        create_specialties_table = """
        CREATE TABLE IF NOT EXISTS Specialties (
            specialty_id INT AUTO_INCREMENT PRIMARY KEY,
            specialty_name VARCHAR(50)
        )
        """
        cursor.execute(create_specialties_table)

        # Insert data into Specialties table
        insert_specialties = """
        INSERT INTO Specialties (specialty_name) VALUES 
        ('Cardiology'),
        ('Neurology'),
        ('Pediatrics'),
        ('Orthopedics'),
        ('Dermatology')
        """
        cursor.execute(insert_specialties)

        # Create Doctors table
        create_doctors_table = """
        CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            doctor_name VARCHAR(50),
            specialty_id INT,
            FOREIGN KEY (specialty_id) REFERENCES Specialties(specialty_id)
        )
        """
        cursor.execute(create_doctors_table)

        # Insert data into Doctors table
        insert_doctors = """
        INSERT INTO Doctors (doctor_name, specialty_id) VALUES
        ('Dr. John Smith', 1),
        ('Dr. Emily Davis', 1),
        ('Dr. Alice Johnson', 2),
        ('Dr. Michael Brown', 2),
        ('Dr. Bob Brown', 3),
        ('Dr. Linda Clark', 3),
        ('Dr. Carol White', 4),
        ('Dr. Kevin Martinez', 4),
        ('Dr. David Green', 5),
        ('Dr. Laura Wilson', 5)
        """
        cursor.execute(insert_doctors)

        # Create Patients table
        create_patients_table = """
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            age INT,
            sex VARCHAR(10),
            specialty_id INT,
            doctor_id INT,
            issue_description TEXT,
            email VARCHAR(100),
            FOREIGN KEY (specialty_id) REFERENCES Specialties(specialty_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
        """
        cursor.execute(create_patients_table)

        print("Database and tables created, data populated successfully!")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

create_database_and_tables()
