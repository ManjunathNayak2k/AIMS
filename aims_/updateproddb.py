from aims_ import db
from aims_.models import Product, Inventory,Company

def update_products(table_data,company_id,invoice_id):
    for item in table_data:
        prod = Product.query.filter_by(name=item[0].lower()).first()
        if prod==None:
            addprod = Product(name=item[0].lower(),price=item[1])
            db.session.add(addprod)
            db.session.commit()
    company = Company.query.filter_by(id=company_id).first()
    if company!=None:
        found = {}
        inventory_items = company.products
        for invitem in inventory_items:
            found[invitem.product_id]=invitem
        for item in table_data:
            checkprod = Product.query.filter_by(name=item[0].lower()).first()
            if checkprod.id in found:
                found[checkprod.id].quantity += item[2]
                db.session.commit()
            else:
                prod = Product.query.filter_by(name=item[0].lower()).first()
                checkinv = Inventory.query.filter_by(company_id=company_id,product_id=prod.id).first()
                if checkinv==None:
                    additem = Inventory(company_id=company_id,quantity=item[2],product_id=prod.id)
                    db.session.add(additem)
                    db.session.commit()
                else:
                    checkinv.quantity+=item[2]
                    db.session.commit()
        return True
    return False


        
