# Inventory Management System

A modern, elegant web application built with Flask for managing inventory across multiple warehouse locations.

##  Features

- **Product Management**: Add, edit, view, and delete products
- **Location Management**: Manage multiple warehouse locations
- **Movement Tracking**: Record product movements between locations
- **Inventory Reports**: Real-time balance reports showing quantities in each location
- **Elegant UI**: Modern, responsive design with smooth animations
- **Dashboard**: Overview with statistics and quick actions
- **Data Management**: Reset and reload  data anytime
- **Persistent Storage**: All data is saved in SQLite database 

##  Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```
cd inventory_app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`


##  Database Schema

### Product Table
- `product_id` (Primary Key, VARCHAR)
- `name` (VARCHAR)
- `description` (VARCHAR)

### Location Table
- `location_id` (Primary Key, VARCHAR)
- `name` (VARCHAR)
- `address` (VARCHAR)

### ProductMovement Table
- `movement_id` (Primary Key, Integer, Auto-increment)
- `timestamp` (DateTime)
- `from_location` (Foreign Key to Location, nullable)
- `to_location` (Foreign Key to Location, nullable)
- `product_name` (Foreign Key to Product)
- `qty` (Integer)


##  Data Management

The application includes a **Data Management** page where you can:
- View current database statistics
- Reset the entire database
- Reload fresh sample data

Access it from: **Dashboard → Data** (in the navigation menu)

##  Data Persistence

- **Database**: SQLite 
- **All changes are automatically saved** - No manual save needed!
- **Data persists** between app restarts
- You can **add your own products** and they'll be saved permanently
- Use the **Reset Database** feature to start fresh with sample data

##  Screenshots

### Dashboard
![Dashboard](https://github.com/Thogaivalli-26/inventory_management/blob/main/templates/inventory%20%20dashboard.png?raw=true)
*Main dashboard showing statistics and quick actions*

### Products List
![Products](https://github.com/Thogaivalli-26/inventory_management/blob/main/templates/inventory%20products.png?raw=true)
*View and manage all products*

### Locations List
![Locations](https://github.com/Thogaivalli-26/inventory_management/blob/main/templates/inventory%20locations.png?raw=true)
*Manage warehouse locations*

### Product Movements
![Movements](https://github.com/Thogaivalli-26/inventory_management/blob/main/templates/inventory%20movements.png?raw=true)
*Track all product movements*

### Inventory Report
![Report](https://github.com/Thogaivalli-26/inventory_management/blob/main/templates/inventory%20report.png?raw=true)
*Balance report showing product quantities in each location*

##  Technical Details

### Technologies Used
- **Backend**: Flask 3.0.0
- **Database**: SQLite with Flask-SQLAlchemy 3.1.1
- **Frontend**: HTML5, CSS3, JavaScript

### Key Features
- **ORM**: Uses SQLAlchemy for database operations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Gradient colors, smooth transitions, and shadows
- **Data Persistence**: SQLite database for permanent storage




