# Culex – Photography Booking SaaS Platform

Culex is a Software-as-a-Service (SaaS) platform designed to connect **photographers** with **clients** in a simple and efficient way.  
The platform allows photographers to showcase their portfolios, manage bookings, and handle client requests, while clients can easily browse photographers, view portfolios, and book photography services.

Culex focuses on usability, transparency, and smooth collaboration between creatives and customers.

---

## Live Application

- **Render Deployment:**  
  https://culex.onrender.com

---

## UI & Product Design

- **Figma UI Prototype:**  
  https://www.figma.com/make/hzd5r59uzMhT5X4HQJMppx/Photography-Booking-Platform?p=f&t=bawI7WMjtcMP8HuL-0

- **Miro Kanban Board:**  
  https://miro.com/app/board/uXjVJuJ6N5E=/?share_link_id=663380797010

---

##  Demo

- **Video Demo of the App:**  
  https://youtu.be/1N7cYVI5iBM

---

##  Feedback Sessions

- Sprint1: https://youtu.be/-wnqEXZdYgQ
- Sprint2: https://youtu.be/irD998umEpM
- Sprint3: https://youtu.be/g_Iz2oM2090

---


## Features

### For Photographers
- Register and log in as a photographer
- Create and manage a professional profile
- Upload and showcase portfolio images
- Manage availability and booking requests

### For Clients
- Register and log in as a client
- Browse photographers and portfolios
- Book photography services
- Manage bookings and requests
- Leave a review and rating as a client

---

## Architecture & Tech Stack

Culex is built as an **all-in-one Flask web application**.  
There is **no separate frontend framework (such as React or Vue)** and **no standalone backend API**.

### Application Architecture

- **Backend Logic**
  - Implemented in **Python (Flask)**
  - Handles routing, authentication, business logic, and security
  - Manages database interactions and file storage
  - Core logic is organized in Python modules (e.g. `routes/`, `models.py`)

- **Frontend Rendering**
  - HTML pages are generated **server-side** using **Jinja2 templates**
  - Templates are stored in the `templates/` directory
  - Static assets (CSS, JavaScript, images) are served via Flask
  - The rendered pages are sent directly to the browser

This architecture keeps the application simple, cohesive, and easy to deploy, making it ideal for an MVP.

---

### Technologies Used

- **Language:** Python  
- **Web Framework:** Flask  
- **Templating Engine:** Jinja2  
- **Database:** PostgreSQL (via Supabase)  
- **Authentication:** Custom (Flask Sessions & Werkzeug Security)  
- **File Storage:** Supabase Storage  
- **Deployment:** Render  

---

## Installation & Running the App Locally

### 1. Create & Activate a Virtual Environment

It is best practice to run Python applications in a virtual environment to manage dependencies.

**Windows**
```bash
python -m venv .venv
.\.venv\Scripts\activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
The application requires database and API credentials.

1. Create a new `.env` file in the root directory (same level as `run.py`).
2. Copy the contents of `.env.example` into `.env`.
3. Update the following variables if needed:
   - `DB_*`
   - `SUPABASE_*`

> **Note:** The example file may contain test credentials. Replace them if you want to use your own database or Supabase project.

### 4. Run the Application
Start the Flask development server:

```bash
python run.py
```

You should see output indicating that the server is running (usually on port 5000).

### 5. Access the App
Open your web browser and navigate to:

```
http://localhost:5000
```

You can now register an account, log in, and explore the platform (booking photographers, managing portfolios, etc.).
