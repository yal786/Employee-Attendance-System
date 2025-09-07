import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date

class SimpleAttendanceSystem:
    def __init__(self):
        self.employees = {}
        self.attendance_records = []
        self.employees_file = "employees.json"
        self.attendance_file = "attendance.json"
        
        self.load_data()
        self.setup_gui()
    
    def load_data(self):
        """Load employees and attendance data"""
        # Load employees
        if os.path.exists(self.employees_file):
            try:
                with open(self.employees_file, 'r') as f:
                    self.employees = json.load(f)
            except:
                self.employees = {}
        
        # Load attendance records
        if os.path.exists(self.attendance_file):
            try:
                with open(self.attendance_file, 'r') as f:
                    self.attendance_records = json.load(f)
            except:
                self.attendance_records = []
    
    def save_data(self):
        """Save employees and attendance data"""
        with open(self.employees_file, 'w') as f:
            json.dump(self.employees, f, indent=2)
        
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_records, f, indent=2)
    
    def setup_gui(self):
        """Setup the GUI"""
        self.root = tk.Tk()
        self.root.title("Simple Attendance Management System")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Attendance Management System", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Employee Management Frame
        emp_frame = ttk.LabelFrame(main_frame, text="Employee Management")
        emp_frame.pack(fill=tk.X, pady=10)
        
        # Add Employee
        ttk.Label(emp_frame, text="Employee Name:").pack(anchor=tk.W, padx=10, pady=5)
        self.name_entry = ttk.Entry(emp_frame, width=30)
        self.name_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(emp_frame, text="Employee ID:").pack(anchor=tk.W, padx=10, pady=5)
        self.id_entry = ttk.Entry(emp_frame, width=30)
        self.id_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Button(emp_frame, text="Add Employee", 
                  command=self.add_employee).pack(anchor=tk.W, padx=10, pady=10)
        
        # Attendance Frame
        att_frame = ttk.LabelFrame(main_frame, text="Mark Attendance")
        att_frame.pack(fill=tk.X, pady=10)
        
        # Employee selection
        ttk.Label(att_frame, text="Select Employee:").pack(anchor=tk.W, padx=10, pady=5)
        self.employee_var = tk.StringVar()
        self.employee_combo = ttk.Combobox(att_frame, textvariable=self.employee_var, 
                                          width=40, state="readonly")
        self.employee_combo.pack(anchor=tk.W, padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(att_frame)
        buttons_frame.pack(anchor=tk.W, padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Mark Present", 
                  command=lambda: self.mark_attendance("Present")).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Mark Absent", 
                  command=lambda: self.mark_attendance("Absent")).pack(side=tk.LEFT, padx=5)
        
        # Records Frame
        records_frame = ttk.LabelFrame(main_frame, text="Attendance Records")
        records_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for records
        self.tree = ttk.Treeview(records_frame, columns=('ID', 'Name', 'Date', 'Time', 'Status'), 
                                show='headings', height=10)
        
        # Define headings
        self.tree.heading('ID', text='Employee ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Status', text='Status')
        
        # Define column widths
        self.tree.column('ID', width=100)
        self.tree.column('Name', width=150)
        self.tree.column('Date', width=100)
        self.tree.column('Time', width=100)
        self.tree.column('Status', width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Refresh Records", 
                  command=self.refresh_records).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export to CSV", 
                  command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear All Records", 
                  command=self.clear_records).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Initialize display
        self.update_employee_list()
        self.refresh_records()
    
    def add_employee(self):
        """Add a new employee"""
        name = self.name_entry.get().strip()
        emp_id = self.id_entry.get().strip()
        
        if not name or not emp_id:
            messagebox.showerror("Error", "Please enter both name and ID")
            return
        
        if emp_id in self.employees:
            messagebox.showerror("Error", "Employee ID already exists")
            return
        
        self.employees[emp_id] = name
        self.save_data()
        self.update_employee_list()
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        
        self.status_label.config(text=f"Added employee: {name} (ID: {emp_id})")
        messagebox.showinfo("Success", f"Employee {name} added successfully!")
    
    def update_employee_list(self):
        """Update the employee dropdown list"""
        employee_list = [f"{emp_id} - {name}" for emp_id, name in self.employees.items()]
        self.employee_combo['values'] = employee_list
    
    def mark_attendance(self, status):
        """Mark attendance for selected employee"""
        selection = self.employee_var.get()
        if not selection:
            messagebox.showerror("Error", "Please select an employee")
            return
        
        emp_id = selection.split(' - ')[0]
        emp_name = self.employees[emp_id]
        
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        
        # Check if already marked today
        for record in self.attendance_records:
            if record['emp_id'] == emp_id and record['date'] == today:
                if messagebox.askyesno("Confirmation", 
                    f"Attendance already marked for {emp_name} today.\nDo you want to update it?"):
                    record['status'] = status
                    record['time'] = current_time
                    self.save_data()
                    self.refresh_records()
                    self.status_label.config(text=f"Updated attendance for {emp_name}: {status}")
                return
        
        # Add new record
        record = {
            'emp_id': emp_id,
            'name': emp_name,
            'date': today,
            'time': current_time,
            'status': status
        }
        
        self.attendance_records.append(record)
        self.save_data()
        self.refresh_records()
        
        self.status_label.config(text=f"Marked {emp_name} as {status}")
        messagebox.showinfo("Success", f"Marked {emp_name} as {status}")
    
    def refresh_records(self):
        """Refresh the records display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add records (show latest first)
        for record in reversed(self.attendance_records):
            self.tree.insert('', 'end', values=(
                record['emp_id'],
                record['name'],
                record['date'],
                record['time'],
                record['status']
            ))
    
    def export_csv(self):
        """Export records to CSV"""
        if not self.attendance_records:
            messagebox.showwarning("Warning", "No records to export")
            return
        
        try:
            import csv
            filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Employee ID', 'Name', 'Date', 'Time', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for record in self.attendance_records:
                    writer.writerow({
                        'Employee ID': record['emp_id'],
                        'Name': record['name'],
                        'Date': record['date'],
                        'Time': record['time'],
                        'Status': record['status']
                    })
            
            messagebox.showinfo("Success", f"Records exported to {filename}")
            self.status_label.config(text=f"Exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def clear_records(self):
        """Clear all attendance records"""
        if messagebox.askyesno("Confirmation", 
            "Are you sure you want to clear ALL attendance records?\nThis action cannot be undone."):
            self.attendance_records = []
            self.save_data()
            self.refresh_records()
            self.status_label.config(text="All records cleared")
            messagebox.showinfo("Success", "All records cleared")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleAttendanceSystem()
    app.run()
