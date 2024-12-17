
from flask import redirect, render_template, request, session, flash
from functools import wraps
import re
from pension import db, logger
from datetime import date
from pension.models import FileMetadata
# Redis client for distributed locking
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

  # Max file size in bytes (16 MB)
def allowed_file(filename:str, allowedExtension:list) -> str:
    return '.' in filename and \
           '.' + filename.rsplit('.', 1)[1].lower() in allowedExtension

def validate_file(file, files_allowed, max_file_size) -> bool:
    """"
    THIS FUNCTION CHECKS THE FILE SIZE AND ALLOWED FILE TYPES FOR UPLOADING.
    """
    if file is None or 'file' not in request.files:
        flash('No file part', 'danger')
        return False

    if file.filename == '':
        flash('No selected file', 'danger')
        return False

    if not allowed_file(file.filename, files_allowed):
        flash("File Type Not Allowed", 'danger')
        return False

    if len(file.read()) > int(max_file_size):
        flash("File is too large", 'danger')
        return False

    return True

def last3(s):
    currentdate = date.today().year % 100
    if s[-3:] == f'/{currentdate}':
        return True


def check_file_name(file:str, allowedEstension):
    if any(file.endswith(ext) for ext in allowedEstension):        
        data = FileMetadata.query.filter_by(file_name=file).first()
    return data

def change_file_name(file, new_name):
    file_extension = file.rsplit('.', 1)[1].lower()
    new_name = escape(new_name)
    new_filename = f"{new_name}.{file_extension}"
    return new_filename



# Define a function for
# for validating an Email
def check(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False


# print(check("adsf@gmail.gamil.cilm"))
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def escape(s):
    """
    Escape special characters.

    https://github.com/jacebrowning/memegen#special-characters
    """
    for old, new in [
        ("-", "--"),
        (" ", "-"),
        ("_", "__"),
        ("?", "~q"),
        ("%", "~p"),
        ("#", "~h"),
        ("/", "~s"),
        ('"', "''"),
    ]:
        s = s.replace(old, new)
    return s


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ("\\", "~s"),
            ('"', "''"),
            ("'", "''"),
            ("'", "''"),


        ]:
            s = s.replace(old, new)
        return s

def escape_reverse(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ("\\", "~s"),
            ('"', "''"),
            ("'", "''"),
            ("'", "''"),


        ]:
            s = s.replace(new, old)
        return s

