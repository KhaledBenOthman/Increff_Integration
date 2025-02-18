📖 Project Overview
This project is designed to automate the extraction and transfer of daily inventory and sales data from our database to an external company's server. The system ensures that the latest data is securely uploaded each day while maintaining a comprehensive log of all operations for monitoring and troubleshooting.

🚀 Project Workflow

1️⃣ Extract Data from Our Database
The system connects to our SQL Server database and runs predefined queries.
Two types of data are extracted:
Inventory Snapshots: The latest inventory status across all stores.
Sales Transactions: Daily sales data, including store details, transaction amounts, and payment methods.

2️⃣ Upload Data to External Server
The generated CSV files are transferred to the other company's SFTP server.
Secure authentication is used to ensure safe data transmission.

3️⃣ Logging & Monitoring
Every step (extraction, file creation, upload, errors) is logged for tracking.
Logs help monitor daily operations and diagnose any failures quickly.

🛠 Technologies Used
Python (for automation and data processing)
SQL Server (for data extraction)
Pandas (for data transformation and CSV generation)
SQLAlchemy & PyODBC (for database connectivity)
Logging Module (for monitoring and debugging)
SFTP (Paramiko Library) (for secure file transfers)


📂 File Structure
bash
Copy
Edit
/Integration_Project
│── .env.py                  # Configuration file (DB & SFTP credentials)
│── Inventory.py             # Script for extracting inventory 
│── Sales.py                 # Script for extracting Sales
│── logging_setup.py         # Centralized logging setup
│── main.py                  # Main execution script
│── logs/                    # Directory for storing log files
│── output/                  # Directory for generated CSV files
└── README.md                # Project documentation
⚙️ Configuration & Setup
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-repo/integration-project.git
cd integration-project
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set Up Database Connection (config.py)

python
Copy
Edit
DB_CONNECTION_STRING = "mssql+pyodbc://username:password@server_ip/Database?driver=ODBC+Driver+17+for+SQL+Server"
Set Up SFTP Credentials (config.py)

python
Copy
Edit
SFTP_HOST = "ftp.companyserver.com"
SFTP_USERNAME = "your_username"
SFTP_PASSWORD = "your_password"
SFTP_UPLOAD_PATH = "/remote/directory/path/"
Run the Integration

bash
Copy
Edit
python main.py
🔍 Monitoring & Logs
Logs are saved in the /logs/ directory.
Example log file: integration_log_2025-02-17.txt
Logs include timestamps for each operation and any errors encountered.