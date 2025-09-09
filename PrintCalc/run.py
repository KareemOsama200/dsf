#!/usr/bin/env python3
"""Main entry point for the PrintCalc application"""

from app import app, db

# Make the app available for gunicorn 
application = app

if __name__ == '__main__':
    with app.app_context():
        # Import models and routes after app context is established
        import models
        import routes
        
        # Create all tables
        db.create_all()
        
        # Initialize default settings if they don't exist
        from werkzeug.security import generate_password_hash
        
        # Initialize default data after models are imported
        if not models.PrintingPrice.query.first():
            default_prices = [
                models.PrintingPrice(name="وش أسود", price_per_unit=0.5, pages_per_unit=2),
                models.PrintingPrice(name="وش وظهر أسود", price_per_unit=0.8, pages_per_unit=4)
            ]
            for price in default_prices:
                db.session.add(price)
        
        # Create default add-ons if they don't exist
        if not models.AddOn.query.first():
            default_addons = [
                models.AddOn(name="غلاف", price=7.0, is_active=True),
                models.AddOn(name="تجليد", price=5.0, is_active=True)
            ]
            for addon in default_addons:
                db.session.add(addon)
        
        # Create default admin employee if no employees exist
        if not models.Employee.query.first():
            admin_employee = models.Employee(
                username="admin",
                password=generate_password_hash("admin123"),
                full_name="مدير النظام",
                phone="01000000000",
                is_active=True
            )
            db.session.add(admin_employee)
        
        db.session.commit()
    
    app.run(host='0.0.0.0', port=5000, debug=True)