from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    movements = db.relationship('ProductMovement', backref='product', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.product_id}>'

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    movements_from = db.relationship('ProductMovement', foreign_keys='ProductMovement.from_location', backref='from_loc', lazy=True)
    movements_to = db.relationship('ProductMovement', foreign_keys='ProductMovement.to_location', backref='to_loc', lazy=True)

    def __repr__(self):
        return f'<Location {self.location_id}>'
    
    def get_inventory(self):
        """Get inventory balance for this location"""
        balances = db.session.query(
            Product.product_id,
            Product.name,
            func.sum(
                db.case(
                    (ProductMovement.to_location == self.location_id, ProductMovement.qty),
                    else_=0
                ) - db.case(
                    (ProductMovement.from_location == self.location_id, ProductMovement.qty),
                    else_=0
                )
            ).label('balance')
        ).join(
            ProductMovement, Product.product_id == ProductMovement.product_id
        ).filter(
            db.or_(
                ProductMovement.to_location == self.location_id,
                ProductMovement.from_location == self.location_id
            )
        ).group_by(
            Product.product_id
        ).having(
            func.sum(
                db.case(
                    (ProductMovement.to_location == self.location_id, ProductMovement.qty),
                    else_=0
                ) - db.case(
                    (ProductMovement.from_location == self.location_id, ProductMovement.qty),
                    else_=0
                )
            ) > 0
        ).all()
        
        return balances

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'

# Create tables (no sample data)
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    products_count = Product.query.count()
    locations_count = Location.query.count()
    movements_count = ProductMovement.query.count()
    return render_template('index.html', 
                         products_count=products_count,
                         locations_count=locations_count,
                         movements_count=movements_count)

# Product Routes
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id'].strip().upper()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        initial_location = request.form.get('initial_location')
        initial_qty = request.form.get('initial_qty', '0')
        
        existing = Product.query.get(product_id)
        if existing:
            flash('Product ID already exists!', 'danger')
            return redirect(url_for('add_product'))
        
        # Add product
        new_product = Product(product_id=product_id, name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        
        # Add initial stock movement if location and quantity provided
        if initial_location and int(initial_qty) > 0:
            initial_movement = ProductMovement(
                from_location=None,
                to_location=initial_location,
                product_id=product_id,
                qty=int(initial_qty)
            )
            db.session.add(initial_movement)
            db.session.commit()
            flash(f'Product added successfully with {initial_qty} units in warehouse!', 'success')
        else:
            flash('Product added successfully!', 'success')
        
        return redirect(url_for('products'))
    
    locations = Location.query.all()
    return render_template('product_form.html', product=None, action='Add', locations=locations)

@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name'].strip()
        product.description = request.form.get('description', '').strip()
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('product_form.html', product=product, action='Edit', locations=[])

@app.route('/product/delete/<product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except:
        flash('Cannot delete product with existing movements!', 'danger')
    return redirect(url_for('products'))

# Location Routes
@app.route('/locations')
def locations():
    all_locations = Location.query.all()
    # Get inventory for each location
    location_inventory = {}
    for location in all_locations:
        location_inventory[location.location_id] = location.get_inventory()
    
    return render_template('locations.html', locations=all_locations, location_inventory=location_inventory)

@app.route('/location/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id'].strip().upper()
        name = request.form['name'].strip()
        address = request.form.get('address', '').strip()
        
        existing = Location.query.get(location_id)
        if existing:
            flash('Location ID already exists!', 'danger')
            return redirect(url_for('add_location'))
        
        new_location = Location(location_id=location_id, name=name, address=address)
        db.session.add(new_location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('location_form.html', location=None, action='Add')

@app.route('/location/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        location.name = request.form['name'].strip()
        location.address = request.form.get('address', '').strip()
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('location_form.html', location=location, action='Edit')

@app.route('/location/delete/<location_id>')
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    try:
        db.session.delete(location)
        db.session.commit()
        flash('Location deleted successfully!', 'success')
    except:
        flash('Cannot delete location with existing movements!', 'danger')
    return redirect(url_for('locations'))

# Movement Routes
@app.route('/movements')
def movements():
    all_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=all_movements)

@app.route('/movement/add', methods=['GET', 'POST'])
def add_movement():
    if request.method == 'POST':
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        product_id = request.form['product_id']
        qty = int(request.form['qty'])
        
        if not from_location and not to_location:
            flash('At least one location (from or to) must be specified!', 'danger')
            return redirect(url_for('add_movement'))
        
        if qty <= 0:
            flash('Quantity must be greater than 0!', 'danger')
            return redirect(url_for('add_movement'))
        
        new_movement = ProductMovement(
            from_location=from_location,
            to_location=to_location,
            product_id=product_id,
            qty=qty
        )
        db.session.add(new_movement)
        db.session.commit()
        flash('Movement added successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movement_form.html', movement=None, action='Add', 
                         products=products, locations=locations)

@app.route('/movement/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    
    if request.method == 'POST':
        movement.from_location = request.form.get('from_location') or None
        movement.to_location = request.form.get('to_location') or None
        movement.product_id = request.form['product_id']
        movement.qty = int(request.form['qty'])
        
        if not movement.from_location and not movement.to_location:
            flash('At least one location (from or to) must be specified!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if movement.qty <= 0:
            flash('Quantity must be greater than 0!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        db.session.commit()
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movement_form.html', movement=movement, action='Edit',
                         products=products, locations=locations)

@app.route('/movement/delete/<int:movement_id>')
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

# Report Route
@app.route('/report')
def report():
    # Calculate balance for each product in each location (only positive balances)
    balances = db.session.query(
        Product.product_id,
        Product.name,
        Location.location_id,
        Location.name.label('location_name'),
        func.sum(
            db.case(
                (ProductMovement.to_location == Location.location_id, ProductMovement.qty),
                else_=0
            ) - db.case(
                (ProductMovement.from_location == Location.location_id, ProductMovement.qty),
                else_=0
            )
        ).label('balance')
    ).select_from(Product).join(
        ProductMovement, Product.product_id == ProductMovement.product_id
    ).join(
        Location, 
        db.or_(
            ProductMovement.to_location == Location.location_id,
            ProductMovement.from_location == Location.location_id
        )
    ).group_by(
        Product.product_id, Location.location_id
    ).having(
        func.sum(
            db.case(
                (ProductMovement.to_location == Location.location_id, ProductMovement.qty),
                else_=0
            ) - db.case(
                (ProductMovement.from_location == Location.location_id, ProductMovement.qty),
                else_=0
            )
        ) > 0  # Only show positive balances
    ).all()
    
    return render_template('report.html', balances=balances)

if __name__ == '__main__':
    app.run(debug=True)