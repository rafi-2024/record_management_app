import datetime
from datetime import date
from pension import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.contact}' )"
    

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empname = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    # pay = db.relationships("Pay", backref="emppay", lazy=True)
    def __repr__(self):
        return f"Employee('{self.empname}', '{self.email}','{self.contact}')"

class Pay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    basic = db.Column(db.Integer, nullable=False)
    ppay = db.Column(db.Integer, nullable=False)
    otherpay = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Basic Pay: {self.basic}, personal Pay: {self.ppay}, Other: {self.otherpay}"
    

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diary_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    reference_no = db.Column(db.String(25), unique=True, nullable=False)
    reference_date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diary.id'), nullable=True)
    diary_references = db.relationship('Diary', backref=db.backref('parent_diary', remote_side=[id]), lazy=True)
    despatch_references = db.relationship('Despatch', backref=db.backref('parent_despatch', remote_side=[id]), lazy=True)
    # file_ref = db.relationship("FileMetadata", backref=db.backref('parent_file_name', remote_side=[id], lazy=True, uselist=False))    
    
    # Define one-to-one relationship backpopulate is the name of field.
    # othertablename = db.relationship(othertablename, back_populates=othertable fieldname, uselist=False, cascade='all, delete-orphan')
    file_ref = db.relationship('FileMetadata', back_populates='diary', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"Diary_id={self.id}, reference_no={self.reference_no}, subject={self.subject}, fileRef={self.file_ref}"
    
    def as_dict(self):
        return {
            'id': self.id,
            'reference_no': self.reference_no,
            'subject': self.subject,
            'fileRef': self.file_ref,
            "diaries": self.diary_references,
            "issues": self.despatch_references
        }



class Despatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    despatch_date = db.Column(db.Date, default=datetime.date.today)
    branch_prefix = db.Column(db.String(60), nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diary.id'), nullable=True) 
    despatch_file_ref = db.relationship('FileMetadata', back_populates='despatch_rel', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"Despatch_Number: {self.id}, subject: {self.subject}"


class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), unique=True, nullable=False)
    # working relationship code for one-one relationship
    item_id = db.Column(db.Integer, db.ForeignKey('diary.id'), nullable = True)
    despatch_id = db.Column(db.Integer, db.ForeignKey('despatch.id'), nullable=True)
    diary = db.relationship("Diary", back_populates='file_ref')
    despatch_rel = db.relationship("Despatch", back_populates='despatch_file_ref')
    # Optionally, define relationships (if you need to access Table1 or Table2 directly)
    # despatch_rel = db.relationship('Despatch', backref='file_ref', foreign_keys=[despatch_id])

    def __init__(self, **kwargs):
        if kwargs.get("item_id") and kwargs.get("despatch_id"):
            raise ValueError('Item can only reference one table at a time')
        if not (kwargs.get("item_id") or kwargs.get("despatch_id")):
            raise ValueError('The argument (ID) must reference either Diary or Despatch')
        super().__init__(**kwargs)