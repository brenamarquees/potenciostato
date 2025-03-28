import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import csv
import serial
import serial.tools.list_ports
import time
from matplotlib.figure import Figure
import threading
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

class PotentiostatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Potentiostat Interface")
        self.root.geometry("1000x700")
        
        self.serial_connection = None
        self.is_connected = False
        self.is_measuring = False
        self.frequencies = []
        self.values = []
        
        self.create_ui()
        self.update_port_list()
    
    def create_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Connection frame
        connection_frame = ttk.LabelFrame(main_frame, text="Device Connection", padding="10")
        connection_frame.pack(fill=tk.X, pady=5)
        
        # Port selection
        ttk.Label(connection_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_combo = ttk.Combobox(connection_frame, width=20)
        self.port_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Refresh ports button
        refresh_btn = ttk.Button(connection_frame, text="Refresh", command=self.update_port_list)
        refresh_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Baud rate selection
        ttk.Label(connection_frame, text="Baud Rate:").grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.baud_combo = ttk.Combobox(connection_frame, width=10, values=["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.baud_combo.current(0)  # Default to 9600
        
        # Connect button
        self.connect_btn = ttk.Button(connection_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=5, padx=5, pady=5)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Measurement Control", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Start/Stop button
        self.start_btn = ttk.Button(control_frame, text="Start Measurement", command=self.toggle_measurement)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)
        self.start_btn.state(['disabled'])
        
        # Clear button
        clear_btn = ttk.Button(control_frame, text="Clear Data", command=self.clear_data)
        clear_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Export buttons
        export_frame = ttk.Frame(control_frame)
        export_frame.grid(row=0, column=2, padx=5, pady=5)
        
        export_csv_btn = ttk.Button(export_frame, text="Export CSV", command=self.export_csv)
        export_csv_btn.pack(side=tk.LEFT, padx=5)
        
        export_pdf_btn = ttk.Button(export_frame, text="Export PDF", command=self.export_pdf)
        export_pdf_btn.pack(side=tk.LEFT, padx=5)
        
        # Graph frame
        graph_frame = ttk.LabelFrame(main_frame, text="Frequency Response", padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_xlabel('Time (s)')
        self.plot.set_ylabel('Frequency (Hz)')
        self.plot.grid(True)
        
        # Embed matplotlib figure in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Not connected")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=5)
    
    def update_port_list(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.current(0)
    
    def toggle_connection(self):
        if not self.is_connected:
            try:
                port = self.port_combo.get()
                baud_rate = int(self.baud_combo.get())
                
                self.serial_connection = serial.Serial(port, baud_rate, timeout=1)
                self.is_connected = True
                self.connect_btn.config(text="Disconnect")
                self.status_var.set(f"Connected to {port} at {baud_rate} baud")
                self.start_btn.state(['!disabled'])
                
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
        else:
            if self.is_measuring:
                self.toggle_measurement()
            
            if self.serial_connection:
                self.serial_connection.close()
            
            self.is_connected = False
            self.connect_btn.config(text="Connect")
            self.status_var.set("Not connected")
            self.start_btn.state(['disabled'])
    
    def toggle_measurement(self):
        if not self.is_measuring:
            self.is_measuring = True
            self.start_btn.config(text="Stop Measurement")
            self.status_var.set("Measuring...")
            
            # Start measurement thread
            self.measurement_thread = threading.Thread(target=self.read_data)
            self.measurement_thread.daemon = True
            self.measurement_thread.start()
        else:
            self.is_measuring = False
            self.start_btn.config(text="Start Measurement")
            self.status_var.set(f"Connected to {self.port_combo.get()} at {self.baud_combo.get()} baud")
    
    def read_data(self):
        start_time = time.time()
        
        while self.is_measuring:
            try:
                # In a real application, you would parse actual data from the potentiostat
                # Here we simulate receiving frequency data
                if self.serial_connection:
                    # Simulate reading data - in a real app, you'd parse actual potentiostat data
                    # For example: line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    # Simulate a frequency value (random for demonstration)
                    current_time = time.time() - start_time
                    # Simulate a frequency that varies over time (sine wave + noise)
                    frequency = 1000 + 500 * np.sin(current_time / 5) + np.random.normal(0, 50)
                    
                    self.frequencies.append(current_time)
                    self.values.append(frequency)
                    
                    # Update the plot (thread-safe)
                    self.root.after(0, self.update_plot)
                    
                    time.sleep(0.1)  # Adjust based on your potentiostat's data rate
            except Exception as e:
                print(f"Error reading data: {str(e)}")
                self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
                self.is_measuring = False
                self.root.after(0, lambda: self.start_btn.config(text="Start Measurement"))
                break
    
    def update_plot(self):
        if len(self.frequencies) > 0:
            self.plot.clear()
            self.plot.plot(self.frequencies, self.values, 'b-')
            self.plot.set_xlabel('Time (s)')
            self.plot.set_ylabel('Frequency (Hz)')
            self.plot.grid(True)
            self.canvas.draw()
    
    def clear_data(self):
        self.frequencies = []
        self.values = []
        self.update_plot()
    
    def export_csv(self):
        if not self.frequencies:
            messagebox.showinfo("Export", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Time (s)', 'Frequency (Hz)'])
                    for i in range(len(self.frequencies)):
                        writer.writerow([self.frequencies[i], self.values[i]])
                
                messagebox.showinfo("Export", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def export_pdf(self):
        if not self.frequencies:
            messagebox.showinfo("Export", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Create PDF
                c = canvas.Canvas(file_path, pagesize=letter)
                width, height = letter
                
                # Add title
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "Potentiostat Frequency Response")
                
                # Add timestamp
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 70, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Save the plot as a PNG in memory
                buf = io.BytesIO()
                self.fig.savefig(buf, format='png', dpi=300)
                buf.seek(0)
                
                # Add the plot to the PDF
                c.drawImage(buf, 50, height - 500, width=500, height=400)
                
                # Add data table header
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, height - 520, "Data Summary")
                
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 540, f"Number of data points: {len(self.frequencies)}")
                
                if self.values:
                    c.drawString(50, height - 560, f"Minimum frequency: {min(self.values):.2f} Hz")
                    c.drawString(50, height - 580, f"Maximum frequency: {max(self.values):.2f} Hz")
                    c.drawString(50, height - 600, f"Average frequency: {sum(self.values)/len(self.values):.2f} Hz")
                
                c.save()
                messagebox.showinfo("Export", f"Graph and data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PotentiostatApp(root)
    root.mainloop()