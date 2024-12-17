import os
from datetime import datetime
from sqlalchemy import desc
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, current_app, send_from_directory
from flask import Response
from werkzeug.utils import secure_filename
from flask_login import login_required
from pension import db, logger
from pension.models import Diary, FileMetadata
from pension.diary.forms import DiaryForm, AddRefs
from pension.main.utils import last3, change_file_name, validate_file


diaries = Blueprint('diaries', __name__)

@diaries.route("/childrecords/<int:id>", methods=["GET"])
@login_required
def childrecords(id:int) -> Response:
    """" This function should return records related to each row just like child record."""
    # data = Diary.query.order_by(desc(Diary.diary_date)).all()
    children = Diary.query.get_or_404(id)
    return redirect(url_for("diaries.new"))


@diaries.route("/diary/new", methods=["GET", "POST"])
@login_required
def new() -> Response:
    data = Diary.query.order_by(desc(Diary.diary_date)).all()
    form = DiaryForm()
    ref_form = AddRefs()
    if not request.method=="POST":
        return render_template("diary.html", title ='Diary',form=form, data = data, ref_form=ref_form) 
    if not form.validate_on_submit():
        logger.error(form.errors)
        error_messages = "\n".join(
        f" {error}"
        for error_list in form.errors.values()
        for error in error_list                
        )
        flash(error_messages, "danger")
        return redirect(url_for("diaries.new"))
    formref = form.reference.data.upper()
    ref_date = form.ref_date.data
    ref_no = formref if last3(formref) else f'{formref}/{ref_date.year % 100}'
    subject = form.subject.data.upper()
    diary_id = form.diary_id.data
    db_ref = Diary.query.filter_by(reference_no=ref_no).first()
    if db_ref:
        flash("Diary Number already exists in Database", "danger")
        return redirect(url_for("diaries.new"))
    try:
        # Lock the session (work in progress).
        diary = Diary(reference_no=ref_no, reference_date= ref_date, subject=subject, diary_id= diary_id)
        db.session.add(diary)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        flash(f"e", "danger")
        abort(500)

    return redirect(url_for('diaries.new'))
    

@diaries.route('/diaries/update_diary', methods=["POST"])       
@login_required
def update_diary() -> Response:
    form = AddRefs()  
    if not form.validate_on_submit():
        # needs some changing here not working currently.
        logger.error(form.errors)
        error_messages = "\n".join(
        f" {error}"
        for error_list in form.errors.values()
        for error in error_list
            
        )
        flash(error_messages, "danger")
        return redirect(url_for('diaries.new'))
    item_id = request.form['ref_id']
    ref = Diary.query.get_or_404(item_id)
    reference_date = request.form['ref_date']
    try:
        reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
    except ValueError:
        flash("Date Format is incorrect or Empty. Please try Again")
        return redirect(url_for('issues.new'))
    ref.reference_date = reference_date
    ref.reference_no = request.form['reference']
    ref.subject = request.form["subject"].upper()
    db.session.commit()
    flash("The reference has been updated successfully", "info")
    return redirect(url_for("diaries.new"))
    

@diaries.route('/diaries/add_refs', methods=["POST"])       
@login_required
def add_diary_refs() -> Response:
    form = AddRefs()
    if not form.validate_on_submit():
        logger.error(form.errors)
        error_messages = "\n".join(
        f" {error}"
        for error_list in form.errors.values()
        for error in error_list
        )
        flash(error_messages, "danger")
        return redirect(url_for('diaries.new'))
    ref_id = request.form.get('ref_id')
    ref = Diary.query.get_or_404(ref_id)
    ref_date = request.form['ref_date']
    try:
        ref_date= datetime.strptime(ref_date, '%Y-%m-%d').date()
    except ValueError:
        flash("Date Format is incorrect or Empty. Please try Again")
        return redirect(url_for('issues.new'))
    subject = request.form['subject']
    formref = request.form['reference']
    if last3(formref):
        ref_no = formref
    else:
        ref_no = f"{formref}/{ref_date.year % 100}"
    db_ref = Diary.query.filter_by(reference_no=ref_no).first()
    if db_ref:
        flash("Diary Number already exists in Database", "danger")
        return redirect(url_for("diaries.new"))
    new_diary = Diary(reference_no=ref_no, reference_date= ref_date, subject=subject, diary_id = ref_id)
    db.session.add(new_diary)
    db.session.commit()
    flash("The reference has been updated successfully", "info")
    return redirect(url_for('diaries.new'))


@diaries.route('/diaries/delete', methods=['POST'])
@login_required
def delete_item() -> Response:
    item_id = request.form['item_id']
    ref = Diary.query.get_or_404(item_id)    
    if not ref.file_ref:
        db.session.delete(ref)
        db.session.commit()
        flash(f'Diary No. {item_id} deleted successfully', 'success')
        return redirect(url_for('diaries.new'))
    file_reference = ref.file_ref.file_name
    base_dir = os.getcwd()
    relative_path = os.getenv('UPLOAD_FOLDER')
    full_path = os.path.join(base_dir,relative_path,file_reference)
    if file_reference and not os.path.exists(full_path):
        db.session.delete(ref)
        db.session.commit()
        flash(f'Diary No. {item_id} deleted successfully, but the file was not found', 'warning')
        return redirect(url_for('diaries.new'))
    # If file reference exists and file is found on the filesystem
    elif file_reference and os.path.exists(full_path):
        import traceback
        try:
            db.session.delete(ref)
            db.session.commit()
            os.remove(full_path)
            flash(f'Reference Number {item_id} alongwith file deleted successfully', 'success')
        except Exception as e:
            logger.error(f"Expection occured: {e}\n {traceback.format_exc()}")
            flash(f"{e}", "danger")
            return redirect(url_for('diaries.new'))
    return redirect(url_for('diaries.new'))


@diaries.route('/diaries/upload', methods=['POST'])
@login_required
def upload() -> Response:
    if not request.method == 'POST':
        return redirect(url_for('diaries.new'))
    file = request.files['file']
    if not validate_file(file, current_app.config["ALLOWED_EXTENSIONS"],current_app.config["MAX_FILE_SIZE"]):
        return redirect(url_for('diaries.new'))        
    base_dir = os.getcwd()
    relative_path = os.getenv('UPLOAD_FOLDER')

    # Join paths
    full_path = os.path.join(base_dir, relative_path)

    if not os.path.exists(full_path):
        os.makedirs(full_path)
    ref_no = Diary.query.filter_by(id=request.form['uploadid']).first().reference_no
    file.save(os.path.join(full_path, file.filename))

    file_data = FileMetadata(item_id = request.form['uploadid'], file_name = file.filename)
    try:
        db.session.add(file_data)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        flash(f"{e}", "danger")
        return redirect(url_for('diaries.new'))
    flash("FILE SAVED SUCCESSFULLY.", "info")
    return redirect(url_for('diaries.new'))


@diaries.route('/diaries/view_file', methods=['GET'])
@login_required
def view_file() -> Response:
    relative_path = os.getenv('UPLOAD_FOLDER')
    # Join paths
    filename = request.args.get('name')
    if filename:
        file_metadata = FileMetadata.query.filter_by(file_name=filename).first()
        file_path = os.path.join(relative_path, filename)
        if os.path.exists(file_path):
            return send_from_directory(relative_path, filename, as_attachment= True)
        else:
            # Delete file reference if not found.
            if file_metadata:
                db.session.delete(file_metadata)
                db.session.commit()
            flash('😿 Oops, File Not Found!<br> &nbsp; &nbsp; &nbsp; It looks like this file has been delted, moved or renamed . <br> 😱 Sorry, but you will need to upload the file again.', 'danger')
            return redirect(url_for('diaries.new'))
    else:
        flash('😿 Oops, The required file name was not supplied!  <br>Don\'t worry, just try again. 🕳️', 'error')
        return redirect(url_for('diaries.new'))

