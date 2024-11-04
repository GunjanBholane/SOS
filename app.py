import smtplib
import geocoder
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

# File to save user credentials
CREDENTIALS_FILE = 'credentials.json'

# Declare global entry variables
entry_from_email = None
entry_password = None
entry_to_email = None

def get_location():
    """Get the current location (latitude and longitude) based on IP address."""
    g = geocoder.ip('me')
    return g.latlng if g.ok else None

def send_sos_email(to_email, from_email, password):
    """Send an SOS email with the current location."""
    location = get_location()
    if not location:
        messagebox.showerror("Error", "Failed to get location.")
        return

    subject = "SOS Alert!"
    body = f"Help! I'm in danger. My current location is:\nLatitude: {location[0]}\nLongitude: {location[1]}\n"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Success", "SOS email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error sending SOS email: {e}")

def save_credentials(from_email, password, to_email):
    """Save user credentials to a JSON file."""
    credentials = {
        'from_email': from_email,
        'password': password,
        'to_email': to_email
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)

def load_credentials():
    """Load user credentials from a JSON file."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return None

def on_send():
    """Handle the send button click event."""
    from_email = entry_from_email.get()
    password = entry_password.get()
    to_email = entry_to_email.get()
    
    if from_email and password and to_email:
        save_credentials(from_email, password, to_email)
        send_sos_email(to_email, from_email, password)
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def main():
    """Main function to run the SOS email program with GUI."""
    global entry_from_email, entry_password, entry_to_email  # Declare them as global
    credentials = load_credentials()
    
    # Create the main window
    window = tk.Tk()
    window.title("SOS Email Sender")
    
    # Set the size of the window
    window.geometry("400x350")
    window.configure(bg='white')

    # Header Label
    header_label = tk.Label(window, text="SOS Email Sender", font=("Helvetica", 18, "bold"), bg="white", fg="#333")
    header_label.pack(pady=10)

    # Frame to hold the input fields
    frame = tk.Frame(window, bg='white')
    frame.pack(pady=10)

    # Create and place labels and entry fields
    tk.Label(frame, text="Your Gmail Address:", bg='white').grid(row=0, column=0, sticky="w", pady=5)
    entry_from_email = tk.Entry(frame, width=30, bg='lightyellow')
    entry_from_email.grid(row=1, column=0, padx=10, pady=5)

    tk.Label(frame, text="App Password:", bg='white').grid(row=2, column=0, sticky="w", pady=5)
    entry_password = tk.Entry(frame, show='*', width=30, bg='lightyellow')
    entry_password.grid(row=3, column=0, padx=10, pady=5)

    tk.Label(frame, text="Recipient Email:", bg='white').grid(row=4, column=0, sticky="w", pady=5)
    entry_to_email = tk.Entry(frame, width=30, bg='lightyellow')
    entry_to_email.grid(row=5, column=0, padx=10, pady=5)

    # Pre-fill fields if credentials are loaded
    if credentials:
        entry_from_email.insert(0, credentials['from_email'])
        entry_password.insert(0, credentials['password'])
        entry_to_email.insert(0, credentials['to_email'])

    # Create and place the SOS button with specified style
    send_button = tk.Button(window, text="SOS", command=on_send,
                             bg='#ff4b5c', fg='white', font=('Helvetica', 16, 'bold'), 
                             relief='flat', width=10, height=2)
    send_button.pack(pady=20)

    # Add a subtle border for the main window
    window.configure(highlightbackground='#d4e157', highlightthickness=3)

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()
