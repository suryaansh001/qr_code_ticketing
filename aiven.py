import streamlit as st
import qrcode
import jwt
import io
from PIL import Image
from datetime import datetime, timedelta
import pymysql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# JWT Secret Key from .env
SECRET_KEY = os.getenv("SECRET_KEY")

# Aiven credentials from .env
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
PASSWORD = os.getenv("PASSWORD")
PORT = (os.getenv("PORT"))
USER = os.getenv("USER")

# pymysql connection
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db=DB_NAME,
  host=HOST,
  password=PASSWORD,
  read_timeout=timeout,
  port=25976,
  user=USER,
  write_timeout=timeout,
)
# Create table if not exists
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                mobile_number VARCHAR(20),
                university VARCHAR(255),
                event_registered_for VARCHAR(255),
                status VARCHAR(20) DEFAULT 'not_entered',
                entry_time DATETIME NULL
            )
        """)
        connection.commit()

create_table()

# QR Code Generator

# QR Code Generator
def generate_qr(ticket_id):
    payload = {
        "ticket_id": ticket_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Replace localhost with deployed Streamlit URL
    qr_data = f"https://suryaanshqrcodeticketinggit-cqdlltuyahvamg3qwdheze.streamlit.app/?token={token}"

    qr = qrcode.make(qr_data)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)
    return buf, token

# Token Scanner and Validator
if "token" in st.query_params:
    st.header("🔍 Ticket Validation")
    token = st.query_params["token"]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        ticket_id = decoded["ticket_id"]

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
            ticket = cursor.fetchone()

            if not ticket:
                st.error("Ticket not found!")
            elif ticket['status'] == 'entered':
                st.warning("Ticket already used!")
                st.markdown(f"**Entry Time:** {ticket['entry_time']}")
            else:
                cursor.execute("""
                    UPDATE tickets SET status='entered', entry_time=%s WHERE id=%s
                """, (datetime.now(), ticket_id))
                connection.commit()
                st.success("✅ Ticket validated successfully!")
                st.markdown(f"**Name:** {ticket['name']}")
                st.markdown(f"**University:** {ticket['university']}")
                st.markdown(f"**Event:** {ticket['event_registered_for']}")
                st.markdown(f"**Time Logged:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except jwt.ExpiredSignatureError:
        st.error("⏰ This ticket has expired.")
    except jwt.InvalidTokenError:
        st.error("❌ Invalid token.")

else:
    # UI
    st.title("🎟️ QR Code Ticketing System")

    menu = st.sidebar.selectbox("Select Role", ["Register Ticket", "Admin View"])

    if menu == "Register Ticket":
        st.header("Register for Event")
        with st.form("register_form"):
            name = st.text_input("Name")
            mobile = st.text_input("Mobile Number")
            university = st.text_input("University")
            event = st.text_input("Event Registered For")
            submitted = st.form_submit_button("Generate Ticket")

            if submitted:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO tickets (name, mobile_number, university, event_registered_for)
                        VALUES (%s, %s, %s, %s)
                    """, (name, mobile, university, event))
                    connection.commit()
                    ticket_id = cursor.lastrowid

                qr_buf, token = generate_qr(ticket_id)
                st.success("Ticket registered successfully!")
                st.image(Image.open(qr_buf), caption=f"Ticket ID: {ticket_id}")

    elif menu == "Admin View":
        st.header("Admin - View All Tickets")
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tickets")
            tickets = cursor.fetchall()
            for t in tickets:
                st.markdown(f"**Name:** {t['name']}")
                st.markdown(f"**Mobile:** {t['mobile_number']}")
                st.markdown(f"**University:** {t['university']}")
                st.markdown(f"**Event:** {t['event_registered_for']}")
                st.markdown(f"**Status:** {'✅ Entered' if t['status'] == 'entered' else '❌ Not Entered'}")
                st.markdown(f"**Entry Time:** {t['entry_time'] if t['entry_time'] else 'N/A'}")
                qr_buf, _ = generate_qr(t['id'])
                st.image(Image.open(qr_buf), caption=f"Ticket ID: {t['id']}")
                st.markdown("---")
