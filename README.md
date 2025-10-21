# Inventory Management System

A modern, elegant web application built with Flask for managing inventory across multiple warehouse locations.

##  Features

- **Product Management**: Add, edit, view, and delete products
- **Location Management**: Manage multiple warehouse locations
- **Movement Tracking**: Record product movements between locations
- **Inventory Reports**: Real-time balance reports showing quantities in each location
- **Elegant UI**: Modern, responsive design with smooth animations
- **Dashboard**: Overview with statistics and quick actions
- **Sample Data**: Automatically loads 10 products, 5 locations, and 30+ movements on first run
- **Data Management**: Reset and reload sample data anytime
- **Persistent Storage**: All data is saved in SQLite database (inventory.db)

##  Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
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

**Note:** On first run, the application will automatically create the database and populate it with sample data including:
- 10 Products (Laptops, Mice, Keyboards, Monitors, etc.)
- 5 Locations (2 Warehouses + 3 Retail Stores)
- 30+ Product Movements (stock arrivals, transfers, sales)


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
- `product_id` (Foreign Key to Product)
- `qty` (Integer)

##  Pre-loaded Sample Data

### Products (10 items)
1. **PROD001** - Dell Laptop XPS 15
2. **PROD002** - Logitech Wireless Mouse
3. **PROD003** - Mechanical Keyboard RGB
4. **PROD004** - Samsung 24" Monitor
5. **PROD005** - HP Printer LaserJet
6. **PROD006** - External Hard Drive 2TB
7. **PROD007** - USB-C Hub Adapter
8. **PROD008** - Webcam HD 1080p
9. **PROD009** - Wireless Headphones
10. **PROD010** - Office Chair Executive

### Locations (5 warehouses)
1. **WH001** - Main Warehouse (123 Industrial Ave)
2. **WH002** - Secondary Warehouse (456 Storage Blvd)
3. **STORE001** - Retail Store Downtown (789 Market St)
4. **STORE002** - Retail Store Mall (321 Commerce Dr)
5. **STORE003** - Retail Store Airport (555 Airport Rd)

### Movements (30+ transactions)
The sample data includes realistic inventory movements:
- Initial stock arrivals to warehouses
- Transfers between warehouses and retail stores
- Sales from retail stores
- Restocking operations

**All this data is automatically loaded when you first run the app!**

##  Data Management

The application includes a **Data Management** page where you can:
- View current database statistics
- Reset the entire database
- Reload fresh sample data

Access it from: **Dashboard → Data** (in the navigation menu)

##  Data Persistence

- **Database**: SQLite (stored in `instance/inventory.db`)
- **All changes are automatically saved** - No manual save needed!
- **Data persists** between app restarts
- You can **add your own products** and they'll be saved permanently
- Use the **Reset Database** feature to start fresh with sample data

##  Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Main dashboard showing statistics and quick actions*

### Products List
![Products](screenshots/products.png)
*View and manage all products*

### Add Product
![Add Product](screenshots/add_product.png)
*Form to add new products*

### Locations List
![Locations](screenshots/locations.png)
*Manage warehouse locations*

### Product Movements
![Movements](screenshots/movements.png)
*Track all product movements*

### Inventory Report
![Report](screenshots/report.png)
*Balance report showing product quantities in each location*

##  Usage Examples

### Creating Products
1. Navigate to **Products** → **Add Product**
2. Enter Product ID (e.g., PROD011)
3. Enter Product Name (e.g., Laptop)
4. Add optional description
5. Click **Add Product**

### Creating Locations
1. Navigate to **Locations** → **Add Location**
2. Enter Location ID (e.g., WH003)
3. Enter Location Name (e.g., Main Warehouse)
4. Add optional address
5. Click **Add Location**

##  How to Add Your Own Data

Want to add more data? Here's how:

### Adding Products
1. Navigate to **Products** → **Add Product**
2. Enter Product ID (e.g., PROD011)
3. Enter Product Name (e.g., Tablet)
4. Add optional description
5. Click **Add Product**

### Adding Locations
1. Navigate to **Locations** → **Add Location**
2. Enter Location ID (e.g., WH003)
3. Enter Location Name (e.g., New Warehouse)
4. Add optional address
5. Click **Add Location**

### Recording Movements

Navigate to **Movements** → **Add Movement** and choose:

#### Receiving New Stock
- **From Location**: Leave blank (External Source)
- **To Location**: Select warehouse
- **Product**: Select product
- **Quantity**: Enter amount

#### Moving Between Warehouses
- **From Location**: Select source warehouse
- **To Location**: Select destination warehouse
- **Product**: Select product
- **Quantity**: Enter amount

#### Selling/Removing Stock
- **From Location**: Select warehouse
- **To Location**: Leave blank (External Destination)
- **Product**: Select product
- **Quantity**: Enter amount

**All your data is automatically saved to the database!**

##  Design Highlights

- **Color Scheme**: Modern purple/blue gradient theme
- **Typography**: Clean, readable Segoe UI font
- **Layout**: Grid-based responsive design
- **Icons**: Font Awesome icons throughout
- **Animations**: Smooth hover effects and transitions
- **Cards**: Beautiful card-based UI components

##  Technical Details

### Technologies Used
- **Backend**: Flask 3.0.0
- **Database**: SQLite with Flask-SQLAlchemy 3.1.1
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4.0

### Key Features
- **ORM**: Uses SQLAlchemy for database operations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Flash Messages**: User feedback for all actions
- **Modern UI**: Gradient colors, smooth transitions, and shadows
- **Report Generation**: Dynamic SQL queries for balance calculation
- **Auto-initialization**: Loads sample data on first run
- **Data Persistence**: SQLite database for permanent storage

##  Security Note

 **Important**: This is a demonstration application. For production use:
- Change the `SECRET_KEY` in `app.py`
- Use a production database (PostgreSQL/MySQL)
- Add user authentication
- Implement proper input validation
- Add CSRF protection
- Use environment variables for configuration

##  Notes

- **Movement Logic**: 
  - Leave "From Location" blank when receiving new stock
  - Leave "To Location" blank when selling/removing stock
  - Fill both for transfers between locations
  
- **Balance Calculation**: 
  - Stock IN (+): When product moves TO a location
  - Stock OUT (-): When product moves FROM a location
  - Net Balance = Total IN - Total OUT

- **Sample Data**:
  - Automatically loaded on first run
  - Can be reset anytime from Data Management page
  - All user-added data is saved permanently

