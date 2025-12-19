
How to install the app:

Prerequisites
Python (Version 3.8 or higher recommended)
Git (to clone the repository)

1. Create a Virtual Environment
It is best practice to run Python applications in a virtual environment to manage dependencies. Run these commands in the terminal of your interpreter (ex. Visual Studio Code) in order to activate your virtual environment.

Windows: 
python -m venv .venv
.\.venv\Scripts\activate.ps1
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

2. Install Dependencies
Install the required Python packages listed in requirements.txt:
pip install -r requirements.txt

3. Configure Environment Variables
The application requires database and API credentials to run. A sample configuration file is provided.

Create a new file named .env in the root directory (same level as run.py).
Copy the contents of .env.example into your new .env file.
Note: The example file appears to contain pre-configured credentials for testing. If you wish to use your own database, update the DB_* and SUPABASE_* variables in .env accordingly.

4. Run the Application

Start the Flask server:
python run.py

You should see output indicating the server is running, typically on port 5000.

5. Access the App
Open your web browser and navigate to:
http://localhost:5000


Video Demo of App: https://youtu.be/1N7cYVI5iBM

You can now register a new account, log in, and explore the features (booking

photographers, managing portfolios, etc.).
