🎟️ QR Code Ticketing System — Streamlit App
This app is a secure ticketing solution built using Streamlit, JWT, PyMySQL, and QR Code generation. It supports two types of users: Attendees who register for events and receive a QR code, and Admins who validate the QR and manage entries.

🌐 Hosted URL
🔗 https://suryaanshqrcodeticketinggit-cqdlltuyahvamg3qwdheze.streamlit.app/

🔁 App Flow Overview
🧍‍♂️ Attendee View (Register Ticket)
Open the app and select "Register Ticket" from the sidebar.

Fill in:

Name

Mobile Number

University

Event Registered For

Submit the form.

✅ A unique QR Code is generated and displayed.

This QR contains a secure JWT token valid for 24 hours.

Attendee presents this QR code at the event.

👮 Admin Flow (Validate QR & Manage Tickets)
A. View All Tickets
Select "Admin View" from the sidebar.

See the list of all registrations.

Each ticket shows:

User details

Status: ✅ Entered, ❌ Denied, or 🟡 Not Entered

QR Code for re-scanning

B. Scanning Tickets at Entry
Admin scans the QR Code shown by the attendee.

This opens a URL like:
https://your-app-url/?token=...

Select "Scan Ticket (Admin Only)" from the sidebar.

The app extracts the token and validates it:

If valid and unused:

Shows ticket details

Admin clicks ✅ Allow Entry or 🚫 Deny Entry

DB updates status to entered or entrydenied

entry_time is logged

If reused or invalid:

Shows error or warning (already entered, expired, or tampered)

📦 Environment Variables (.env)
env
Copy
Edit
SECRET_KEY=your_jwt_secret_key

DB_NAME=defaultdb
HOST=your_host
PORT=25976
USER=avnadmin
PASSWORD=your_password
⚙️ Tech Stack
Streamlit – UI

PyMySQL – MySQL connectivity

JWT – Secure token in QR

qrcode – QR Code generation

Pillow (PIL) – Image handling

dotenv – Environment variable loading

✅ Security Features
Tokens are time-limited (24 hours).

Token carries only the ticket_id, signed with JWT secret.

DB status prevents re-entry or double use.

Admin decides entry manually to avoid auto-grants.

🧪 Testing
Run locally using streamlit run your_app.py

Install dependencies via pip install -r requirements.txt

Deploy to Streamlit Cloud and set the same .env vars

