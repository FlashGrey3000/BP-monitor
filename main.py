import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt


conn = mysql.connector.connect(host="localhost", user="root", passwd="root")

cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS BloodPressureMonitor")
cur.execute("USE BloodPressureMonitor")
cur.execute("""CREATE TABLE IF NOT EXISTS BloodPressureTable(
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            time TIME,
            Systolic INT,
            Diastolic INT,
            Pulse INT
            )
            """)
conn.commit()
cur.close()
conn.close()

def submit():
    date = date_entry.get()
    time = time_entry.get()
    systolic = int(systolic_entry.get())
    diastolic = int(diastolic_entry.get())
    pulse = int(pulse_entry.get())

    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"Systolic: {systolic}")
    print(f"Diastolic: {diastolic}")

    conn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="BloodPressureMonitor")
    cur = conn.cursor()
    
    cur.execute("INSERT INTO BloodPressureTable (date, time, systolic, diastolic, pulse) VALUES (%s, %s, %s, %s, %s)", (date, time, systolic, diastolic, pulse))
    
    conn.commit()
    
    cur.close()
    conn.close()


def show_graph():
    # Placeholder for showing the graph
    print("Showing Graph...")
    conn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="BloodPressureMonitor")
    cur = conn.cursor()
    # Execute the SQL query
    query = "SELECT * FROM BloodPressureTable ORDER BY date DESC LIMIT 30"
    cur.execute(query)

    # Fetch all the rows
    latest_records = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    dates=[]
    systolic_values=[]
    diastolic_values=[]
    pulse_values=[]

    # Print the fetched records
    for record in latest_records:
        print(record)
        print(record[1])
        dates.append(record[1])
        systolic_values.append(record[3])
        diastolic_values.append(record[4])
        pulse_values.append(record[5])

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot systolic values
    plt.plot(dates, systolic_values, label='Systolic', marker='o')

    # Plot diastolic values
    plt.plot(dates, diastolic_values, label='Diastolic', marker='x')

    plt.plot(dates, pulse_values, label='Pulse', marker='v')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Blood Pressure Readings')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.legend()

    plt.xticks(ticks=dates)

    # Display the plot
    plt.tight_layout()
    plt.show()


# Create the main application window
root = tk.Tk()
root.title("Blood Pressure Entry")

# Create and place input fields and labels
date_label = ttk.Label(root, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = ttk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=10)

time_label = ttk.Label(root, text="Time:")
time_label.grid(row=1, column=0, padx=10, pady=10)
time_entry = ttk.Entry(root)
time_entry.grid(row=1, column=1, padx=10, pady=10)

systolic_label = ttk.Label(root, text="Systolic:")
systolic_label.grid(row=2, column=0, padx=10, pady=10)
systolic_entry = ttk.Entry(root)
systolic_entry.grid(row=2, column=1, padx=10, pady=10)

diastolic_label = ttk.Label(root, text="Diastolic:")
diastolic_label.grid(row=3, column=0, padx=10, pady=10)
diastolic_entry = ttk.Entry(root)
diastolic_entry.grid(row=3, column=1, padx=10, pady=10)

pulse_label = ttk.Label(root, text="Pulse:")
pulse_label.grid(row=4, column=0, padx=10, pady=10)
pulse_entry = ttk.Entry(root)
pulse_entry.grid(row=4, column=1, padx=10, pady=10)

# Create Submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create Show Graph button
show_graph_button = ttk.Button(root, text="Show Graph", command=show_graph)
show_graph_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()