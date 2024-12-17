import os
import time
from datetime import datetime
from pathlib import Path
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, current_app, send_from_directory
from flask_login import login_required
from pension import db, logger
from pension.models import Despatch, FileMetadata
from pension.issue.forms import IssueForm, ReminderForm
from pension.main.utils import validate_file, change_file_name
from pension.main.utils import escape, escape_reverse

from werkzeug.utils import secure_filename
# from html import escape # to sanitize the input from the forms

issues = Blueprint('issues', __name__)

@issues.route("/issues/new", methods=["GET", "POST"])
@login_required
def new():
    form = IssueForm()
    ref_form = ReminderForm()
    num_fields = len(ref_form._fields)
    data = Despatch.query.all()
    if not request.method=="POST":
        return render_template("issue_new.html",form=form, title ='Issue-New', data = data, ref_form=ref_form, num_fields=num_fields) 

    if not form.validate_on_submit():
        logger.error(form.errors)
        error_messages = "\n".join(
        f" {error}"
        for error_list in form.errors.values()
        for error in error_list                
        )
        flash(error_messages, "danger")
        return redirect(url_for("issues.new"))
    issue_date = request.form['issue_date']
    try:
        issue_date = datetime.strptime(issue_date, '%Y-%m-%d').date()
    except ValueError:
        flash("Date Format is incorrect or Empty. Please try Again")
        return redirect(url_for('issues.new'))
    branch_ref = escape(request.form['branch'])
    subject = request.form['subject']
    issue_ref = request.form['diary_id']

    new_issue = Despatch(branch_prefix = branch_ref, despatch_date=issue_date,subject= subject, diary_id=issue_ref)
    try:
        db.session.add(new_issue)
        db.session.commit()
    except Exception as e:
        flash(e, "Danger")
        logger.error(e)
        abort(500)

    flash("New record entered", "success")
    return redirect(url_for('issues.new'))


@issues.route('/issues/delete', methods=['POST'])
@login_required
def delete():
    item_id = request.form['item_id']
    ref = Despatch.query.get_or_404(item_id)    
    if not ref.despatch_file_ref:
        db.session.delete(ref)
        db.session.commit()
        flash(f'Despatch No. {item_id} deleted successfully', 'success')
        return redirect(url_for('issues.new'))
    file_reference = ref.despatch_file_ref.file_name
    base_dir = os.getcwd()
    relative_path = os.getenv('UPLOAD_FOLDER')
    full_path = os.path.join(base_dir,relative_path,'ISSUE',file_reference)
    if file_reference and not os.path.exists(full_path):
        db.session.delete(ref)
        db.session.commit() 
        flash(f'Despatch No. {item_id} deleted successfully, but the file was not found', 'warning')
        return redirect(url_for('issues.new'))
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
            return redirect(url_for('issues.new'))
    return redirect(url_for('issues.new'))

@issues.route('/issues/update', methods=["POST"])       
@login_required
def update():
    if request.method == "POST":
        id = request.form['item_id']
        ref = Despatch.query.get_or_404(id)
        if not ref:
            flash("Unable to locate the required record, please try again")
            return redirect(url_for('issues.new'))

        request_despatch_date = request.form['issue_date']
        try:
            issue_date = datetime.strptime(request_despatch_date, '%Y-%m-%d').date()
        except ValueError:
            flash("Date Format is incorrect or Empty. Please try Again")
            return redirect(url_for('issues.new'))
    
        ref.despatch_date = issue_date
        ref.branch_prefix = request.form['branch']
        ref.subject = request.form['subject']
        ref.diary_id = request.form['diary_id']
        db.session.commit()
        flash("Record Updated Successfully", "success")
        return redirect(url_for('issues.new'))
    else:
        flash("Method not allowed")
        return redirect(url_for('issues.new'))
    

@issues.route('/issues/upload', methods=['POST'])
@login_required
def upload():
    if not request.method == 'POST':
        return redirect(url_for('issues.new'))

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    file = request.files['file']
    # print(upload_file)
    if not validate_file(file, current_app.config["ALLOWED_EXTENSIONS"],int(current_app.config["MAX_FILE_SIZE"])):
        logger.error("File Upload Failed")
        flash("File Validation Failed", "info")
        return redirect(url_for('issues.new'))        
    base_dir = os.getcwd()
    relative_path = os.getenv('UPLOAD_FOLDER')
    print(base_dir, relative_path)
    # Join paths
    full_path = Path(relative_path) / "ISSUE"

    # Ensure the directory exists
    full_path.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    """Change the following code according to Despatch model"""


    ref_no = Despatch.query.filter_by(id=request.form['uploadid']).first().branch_prefix
    ref_no = request.form['uploadid']+ref_no
    file_name = secure_filename(file.filename)
    try:
        # Sanitize and save the file
        filename = full_path / file_name
        file.save(filename)
        time.sleep(20)
        # filename = os.path.join(full_path, secure_filename(file.filename))
        # file.save(filename)
    except PermissionError:
        return 'Permission denied: Unable to upload file to the folder.'
    except Exception as e:
        return f'An error occurred: {e}'
    file_data = FileMetadata(despatch_id = request.form['uploadid'], file_name = file_name)
    try:
        db.session.add(file_data)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        m = str(e)
        flash(m.split(":")[0], "danger")
        return redirect(url_for('issues.new'))
    flash("FILE SAVED SUCCESSFULLY.", "info")
    return redirect(url_for('issues.new'))



@issues.route('/issues/view_file', methods=['GET'])
@login_required
def view_file():
    relative_path = os.getenv('UPLOAD_FOLDER')
    relative_path = os.path.join(relative_path, "ISSUE")    
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
            return redirect(url_for('issues.new'))
    else:
        flash('😿 Oops, The required file name was not supplied!  <br>Don\'t worry, just try again. 🕳️', 'error')
        return redirect(url_for('issues.new'))


@issues.route('/issues/add_refs', methods=["POST"])       
@login_required
def add_diary_refs():
    form = ReminderForm()
    if not form.validate_on_submit():
        logger.error(form.errors)
        error_messages = "\n".join(
        f" {error}"
        for error_list in form.errors.values()
        for error in error_list    
        )
        flash(error_messages, "danger")
        return redirect(url_for('issues.new'))
    ref_id = request.form.get('diary_id')
    ref = Despatch.query.get_or_404(ref_id)
    ref_date = request.form['issue_date']
    try:
        ref_date= datetime.strptime(ref_date, '%Y-%m-%d').date()
    except ValueError:
        flash("Date Format is incorrect or Empty. Please try Again")
        return redirect(url_for('issues.new'))
    subject = request.form['subject']
    branch = request.form['branch']
    new_diary = Despatch(branch_prefix=branch, despatch_date= ref_date, subject=subject, diary_id = ref_id)
    db.session.add(new_diary)
    db.session.commit()
    flash("The reference has been updated successfully", "info")
    return redirect(url_for('issues.new'))




