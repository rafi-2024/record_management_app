from flask import Blueprint, render_template
from flask_login import login_required
from pension import db
from pension.models import Diary, Despatch
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

dash = Blueprint('dashboard', __name__)

def refine_db_results(results: list, column_names:list, counting_col:str) -> dict:
    data_dicts = [r.__dict__ for r in results]
    # Remove the SQLAlchemy internal '__mapper__' and '_sa_instance_state' columns if present
    for d in data_dicts:
        d.pop('_sa_instance_state', None)
        d.pop('__mapper__', None)
    # Convert to pandas DataFrame
    df = pd.DataFrame(data_dicts)
    # If the DataFrame has more columns, and you only want to rename a subset
    df.rename(columns=dict(zip(df.columns[:len(column_names)], column_names)), inplace=True)
    df.columns = column_names
    df.replace('', pd.NA, inplace=True)    

    total_diary = len(df)
    true_count_references = df[counting_col].notna().value_counts().get(True,0)
    false_count_references = df[counting_col].notna().value_counts().get(False,0)

    return {'total_diary': str(total_diary), 'true_count_references': str(true_count_references), 'false_count_references': str(false_count_references)}

@dash.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    diary_results = db.session.query(Diary).all()
    despatch_results = db.session.query(Despatch).all()
    column_names = ["Diary No","Reference No", "Subject", "Receipt Date", "Receiving Date", "Link Ref No"]
    despatch_col_names = ["Issue Date","Issuing branch", "Reference No", "Link Ref No", "Subject"]
    counting_col = "Link Ref No"
    # Convert the SQLAlchemy model instances to dictionaries
    diary_results = refine_db_results(diary_results, column_names=column_names, counting_col=counting_col)
    despatch_results = refine_db_results(despatch_results,column_names=despatch_col_names, counting_col=counting_col)
    return render_template("dashboard.html", diaries = diary_results, despatch = despatch_results)
