from app import db
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class AcademicYear(db.Model):
    """Model for academic years (e.g., أولى ابتدائي، ثانية ابتدائي)"""
    __tablename__ = 'academic_years'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationship with subjects
    subjects = relationship('Subject', backref='academic_year', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AcademicYear {self.name}>'

class Subject(db.Model):
    """Model for subjects within academic years (e.g., عربي، رياضيات، علوم)"""
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)
    
    # Relationship with books
    books = relationship('Book', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Book(db.Model):
    """Model for books within subjects"""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    page_count = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.name} ({self.page_count} pages)>'

class PrintingPrice(db.Model):
    """Model for printing prices and types"""
    __tablename__ = 'printing_prices'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # e.g., "وش أسود", "وش وظهر أسود"
    price_per_unit = Column(Float, nullable=False)
    pages_per_unit = Column(Integer, nullable=False)  # How many pages per unit (2 for single-sided, 4 for double-sided)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<PrintingPrice {self.name}: {self.price_per_unit} per unit>'

class AddOn(db.Model):
    """Model for fixed add-ons like covers, binding, etc."""
    __tablename__ = 'addons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<AddOn {self.name}: {self.price}>'
