import tkinter as tk
from tkinter import ttk, messagebox
from models import MachineStatus, Log
from api_integration import fetch_machine_status, update_machine_status, fetch_machine_logs, send_local_logs
from datetime import datetime

class RMMApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Remote Monitoring & Management")
        
        # Create a frame to display machine info
        self.machine_frame = ttk.LabelFrame(root, text="Machine Info")
        self.machine_frame.pack(pady=10, padx=10, fill="both", expand="yes")
        
        # Label to show the machine status
        self.status_label = ttk.Label(self.machine_frame, text="Status: Offline")
        self.status_label.pack(pady=5)
        
        # Button to trigger status update
        self.update_status_button = ttk.Button(self.machine_frame, text="Send Status Update", command=self.update_status)
        self.update_status_button.pack(pady=5)
        
        # Create a frame to display logs
        self.logs_frame = ttk.LabelFrame(root, text="Logs")
        self.logs_frame.pack(pady=10, padx=10, fill="both", expand="yes")
        
        # Text widget to display logs
        self.logs_text = tk.Text(self.logs_frame, height=10, state="disabled")
        self.logs_text.pack(pady=5, padx=5)
        
        # Button to sync logs with the server
        self.sync_logs_button = ttk.Button(self.logs_frame, text="Sync Logs with Server", command=self.sync_logs)
        self.sync_logs_button.pack(pady=5)
        
        # Machine ID for which data is fetched
        self.machine_id = "9bca8c21-1a34-49a9-92ac-3c27f4052274"  # Replace with your machine ID

        # Load initial machine status and logs
        self.load_machine_status()
        self.load_logs()

    def load_machine_status(self):
        """
        Fetch the current status of the machine from the server
        and display it in the UI.
        """
        try:
            # Fetch machine status from the server
            machine = fetch_machine_status(self.machine_id)
            
            # Save the machine status in the local database
            MachineStatus.get_or_create(
                machine_id=machine['id'],
                defaults={
                    'name': machine['name'],
                    'status': machine['status'],
                    'last_updated': datetime.now()
                }
            )
            
            # Update the status label in the UI
            self.status_label.config(text=f"Status: {machine['status']}")
        except Exception as e:
            # Show an error message if fetching status fails
            messagebox.showerror("Error", f"Failed to fetch machine status: {e}")

    def update_status(self):
        """
        Allows the user to select the desired status and updates the machine status on the server.
        """
        # Define available statuses
        status_options = ["online", "offline", "maintenance"]

        # Create a new window for status selection
        def update_selected_status():
            selected_status = status_var.get()  # Get the selected status
            try:
                # Send the selected status to the server
                response = update_machine_status(self.machine_id, selected_status)
                
                # Update the status label in the UI
                self.status_label.config(text=f"Status: {response['status']}")
                
                # Show a success message
                messagebox.showinfo("Success", f"Status updated to '{response['status']}' successfully!")
                
                # Close the status selection window
                status_window.destroy()
            except Exception as e:
                # Show an error message if updating status fails
                messagebox.showerror("Error", f"Failed to update status: {e}")

        # Create a new popup window
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Machine Status")
        status_window.geometry("300x200")
        status_window.resizable(False, False)

        # Add a label to the popup
        tk.Label(status_window, text="Select Machine Status:", font=("Arial", 12)).pack(pady=10)
        
        # Dropdown menu for selecting status
        status_var = tk.StringVar(value=status_options[0])
        status_menu = ttk.OptionMenu(status_window, status_var, *status_options)
        status_menu.pack(pady=10)

        # Button to confirm the status update
        ttk.Button(status_window, text="Update Status", command=update_selected_status).pack(pady=10)

    def load_logs(self):
        """
        Fetch logs from the server and display them in the UI.
        """
        try:
            # Fetch logs from the server
            logs = fetch_machine_logs(self.machine_id)
            
            # Enable the text widget for updates
            self.logs_text.config(state="normal")
            self.logs_text.delete("1.0", tk.END)  # Clear existing logs
            
            # Add logs to the text widget
            for log in logs:
                self.logs_text.insert(tk.END, f"{log['level'].upper()}: {log['message']} ({log['created_at']})\n")
            
            # Disable the text widget to prevent editing
            self.logs_text.config(state="disabled")
        except Exception as e:
            # Show an error message if fetching logs fails
            messagebox.showerror("Error", f"Failed to fetch logs: {e}")

    def sync_logs(self):
        """
        Sync local logs with the server.
        """
        try:
            # Get unsynced logs from the local database
            local_logs = Log.select().where(Log.machine_id == self.machine_id)
            
            # Prepare logs for syncing
            logs_data = [
                {
                    "level": log.log_level,
                    "message": log.message,
                    "created_at": log.created_at.strftime("%Y-%m-%dT%H:%M:%S")
                }
                for log in local_logs
            ]
            
            # Send logs to the server
            send_local_logs(self.machine_id, logs_data)
            
            # Show a success message
            messagebox.showinfo("Success", "Logs synced successfully!")
        except Exception as e:
            # Show an error message if syncing logs fails
            messagebox.showerror("Error", f"Failed to sync logs: {e}")


if __name__ == "__main__":
    # Create the main Tkinter window and run the application
    root = tk.Tk()
    app = RMMApp(root)
    root.mainloop()
