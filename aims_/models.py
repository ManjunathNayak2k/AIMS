from aims_ import db, login_manager
from flask_login import UserMixin
from aims_.routes import session

@login_manager.user_loader
def load_user(user_id):
    if 'account_type' in session:
        if session['account_type'] == 'broker':
            return Broker.query.get(int(user_id))
        elif session['account_type'] == 'admin':
            return Admin.query.get(int(user_id))
        elif session['account_type'] == 'company':
            return Company.query.get(int(user_id))
    return None

class Broker(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    invoices = db.relationship('Invoice', backref='processor', lazy=True)
    
    def __repr__(self):
        return f"Broker('{self.username}', '{self.email}', '{self.sex}')"

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}', '{self.sex}')"

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    commission = db.Column(db.Integer,nullable=False,default = 10)
    revenue_generated = db.Column(db.Integer,nullable=False,default = 0)
    street = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    invoices = db.relationship(
        'Invoice', backref='owner', cascade="all,delete", lazy=True)
    specializations = db.relationship('Specialization', backref='owners',cascade="all,delete", lazy=True)
    products = db.relationship(
        'Inventory', backref='product_owner', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f"Company('{self.username}', '{self.email}') Commission '{self.commission}', Revenue '{self.revenue_generated}'" 

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file =  db.Column(db.String(20), nullable=False)
    coors_file =  db.Column(db.String(20), nullable=False)
    processed = db.Column(db.Boolean, nullable=False,default= False)
    manual_processing = db.Column(db.Boolean, nullable=False, default=False)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.id'),nullable = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __repr__(self):
        return f"Invoice('{self.image_file}', Coordinate '{self.coors_file}', Owner '{self.owner_id}',Assigned to '{self.broker_id}',Processed '{self.processed}')" 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer,nullable=False)

    products = db.relationship(
        'Inventory', backref='which_product', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class Specialization(db.Model):
    name = db.Column(db.String(20), nullable=False, primary_key=True,autoincrement=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False,primary_key=True, autoincrement=False)

    def __repr__(self):
        return f"Specialization('{self.name}', '{self.company_id}')"

class Inventory(db.Model):
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False,primary_key=True,autoincrement=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True, autoincrement=False)
    quantity = db.Column(db.Integer, nullable=False,default=0)
    
    def __repr__(self):
        return f"Inventory(Company :'{self.company_id}', Product Number : '{self.product_id}', Quantity : '{self.quantity}')"


