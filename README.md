# 🎟️ QR Code Ticketing System  

**A secure event management solution** built with Streamlit, JWT, and MySQL.  
🌐 **Hosted App**: [Access Here](https://suryaanshqrcodeticketinggit-cqdlltuyahvamg3qwdheze.streamlit.app/)  

---

## 🔁 App Flow  

### 🧍‍♂️ Attendee View (Register Ticket)  
1. Select **"Register Ticket"** in sidebar  
2. Submit:  
   - **Name**  
   - **Mobile Number**  
   - **University**  
   - **Event Registered For**  
3. Receive **unique QR Code** with 24-hour JWT token  

### 👮 Admin Flow  
#### A. View All Tickets  
- Select **"Admin View"**  
- See registrations with:  
  - User details  
  - Status: ✅ Entered / ❌ Denied / 🟡 Not Entered  
  - QR Code for re-scanning  

#### B. Validate Tickets at Entry  
1. Scan attendee's QR code (opens URL with `?token=...`)  
2. Select **"Scan Ticket (Admin Only)"**  
3. System checks:  
   - ✅ **Valid & Unused**: Shows details → Admin approves/denies entry  
   - ⚠️ **Invalid**: Shows error (expired/tampered/already used)  

---


### 🔧 Tech Stack  
- **Streamlit** – Frontend UI  
- **PyMySQL** – MySQL Database Connectivity  
- **JWT** – Secure Token Generation/Validation  
- **qrcode** – QR Code Generation  
- **Pillow** – Image Processing  
- **python-dotenv** – Environment Management  

---

## 🔒 Security Features  
- ⏳ **24-hour token validity**  
- 🔐 **JWT-signed tokens** (carry only ticket_id)  
- 🚫 **Double-entry prevention** via DB status checks  
- 👮 **Manual approval** by admins for entry grants  

---

