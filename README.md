# 🌐 Automatic Network Devices Configurator

Web application designed for the automation and rapid static configuration of network device interfaces (routers, PCs, and switches) running inside **GNS3** network emulation environments. 

Developed with a **Django** backend, **Netmiko** for SSH/Telnet orchestration, a persistent **PostgreSQL** relational database, and fully containerized via **Docker Compose** for seamless deployment.

---

## 📌 Key Features

- ⚡ **Rapid Static Interface Provisioning:** Automatically pushes interface configurations (IP addressing, subnets, descriptions, state) to target devices in GNS3.
- 🔀 **Multi-Device Support:** Supports common network appliances configured in GNS3 topologies (Cisco IOS Routers, Cisco Switches, and Virtual PCs/VPCS).
- 🛠️ **Automated CLI Execution:** Utilizes **Netmiko** to handle SSH/Telnet handshakes, command serialization, prompt detection, and error catching.
- 🗄️ **Persistent Inventory:** Backed by **PostgreSQL** to manage topology metadata, interface assignments, device credentials, and execution logs.
- 🐳 **Full Dockerization:** Complete container stack via Docker Compose for easy local development without dependency conflicts.

---

## 🏗️ Architecture & Tech Stack

```text
Automatic-Network-Devices-Configurator/
│
├── .env.example              # Template for environment variables (DB, Django secrets)
├── docker-compose.yml        # Multi-container orchestration (Web + PostgreSQL)
├── Dockerfile                # Web service container definition
├── requirements.txt          # Python dependencies (Django, Netmiko, psycopg2, etc.)
│
├── core/                     # Django project configuration (settings, wsgi, urls)
│
├── configurator/             # Django application for network logic
│   ├── models.py             # Database models (Devices, Interfaces, Logs)
│   ├── views.py              # Application logic & UI endpoints
│   ├── tasks.py / services.py# Netmiko SSH/Telnet execution workers
│   └── templates/            # Web dashboard templates
│
└── README.md
Components
Backend: Python & Django (REST/MVC pattern)

Network Automation Engine: Netmiko (SSH / Telnet handling)

Database: PostgreSQL (Stores device catalog, interface tables, deployment logs)

Target Topology: GNS3 Network Simulation Server

Containerization: Docker & Docker Compose

🚀 Getting Started
Prerequisites
Ensure you have the following installed on your host system:

Docker Desktop & Docker Compose

GNS3 running a topology with network devices reachable from the Docker bridge/host network.

Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/LiviuGhilinta/Automatic-Network-Devices-Configurator.git](https://github.com/LiviuGhilinta/Automatic-Network-Devices-Configurator.git)
cd Automatic-Network-Devices-Configurator
Configure Environment Variables:
Copy the example environment configuration:

Bash
cp .env.example .env
(Ensure database credentials and DEBUG mode match your environment).

Build and launch containers:

Bash
docker compose up --build -d
Apply database migrations:

Bash
docker compose exec web python manage.py migrate
Create a superuser (Optional, for admin access):

Bash
docker compose exec web python manage.py createsuperuser
Access the application:
Open your browser and navigate to:

Plaintext
http://localhost:8000
🔌 Connecting to GNS3 Topology
Ensure the Docker container can route traffic to your GNS3 management network (via GNS3 Cloud Node or local Host-Only adapter).

Configure Telnet/SSH access and IP reachability on your GNS3 nodes.

Add the devices into the application inventory with:

Hostname / Label

IP Address & Management Port (SSH: 22 / Telnet: 23 or GNS3 console ports)

Device Type (e.g., cisco_ios, generic_termserver)

Credentials (Username, Password, Enable Secret)

Select desired interfaces, assign static configurations, and execute the automated push.

👤 Author
Liviu Ghilință

GitHub: @LiviuGhilinta
