from flask import Flask, render_template, url_for, redirect, session, request, jsonify, flash, g
from datetime import datetime, timedelta
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract, or_, distinct, create_engine, MetaData, Table, text, asc
import os
import threading
import schedule
import time
from jinja2 import Environment
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.globals import current_app  # Import current_app correctly

parameters = {}
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123_!Atellp#@34.131.21.184/masters"
app.config['SQLALCHEMY_BINDS'] = {
    'operation_master': 'mysql://root:123_!Atellp#@34.131.21.184/operation_master',
    'ht_dp_mdo': 'mysql://root:123_!Atellp#@34.131.21.184/ht_dp_mdo',
}
app.secret_key = "any-string-you-want-just-keep-it-secret"
db = SQLAlchemy(app)

# Userview table
class Userview(db.Model):
    uid = db.Column(db.BigInteger, primary_key=True,nullable=False)
    ln_id = db.Column(db.Text,nullable=True)
    priority = db.Column(db.Text,nullable=False)
    employee_name = db.Column(db.Text,nullable=False)
    module_display_name = db.Column(db.Text,nullable=False)
    process_display_name = db.Column(db.Text,nullable=False)
    project_display_name = db.Column(db.Text,nullable=False)
    task_display_name = db.Column(db.Text,nullable=False)
    descr = db.Column(db.Text,nullable=False)
    role = db.Column(db.Text,nullable=False)
    how = db.Column(db.Text,nullable=False)
    tat = db.Column(db.Text,nullable=False)
    tatunit = db.Column(db.Text,nullable=False)
    planned = db.Column(db.DateTime,nullable=False)
    actual = db.Column(db.DateTime,nullable=False)
    task_information = db.Column(db.Text,nullable=False)
    last_task_input = db.Column(db.Text,nullable=False)
    task_id = db.Column(db.Text,nullable=False)
    input_display_name = db.Column(db.Text,nullable=False)
    ln_status = db.Column(db.Text,nullable=False)

# inputmaster table
class Inputmaster(db.Model):
    uid = db.Column(db.BigInteger, primary_key=True, nullable=False)
    module_id = db.Column(db.Text,nullable=True)
    process_id = db.Column(db.Text,nullable=True)
    task_id = db.Column(db.Text,nullable=True)
    input_id = db.Column(db.Text,nullable=True)
    input_type = db.Column(db.Text,nullable=True)
    input_display_name = db.Column(db.Text,nullable=True)
    input_variables = db.Column(db.Text,nullable=True)
    data_call_table_name = db.Column(db.Text,nullable=True)
    affected_input = db.Column(db.Text,nullable=True)
    input_display_id = db.Column(db.Text,nullable=False)
    input_number = db.Column(db.Integer, nullable=False)

# Doermaster table
class Doermaster(db.Model):
    uid = db.Column(db.BigInteger,primary_key=True,nullable=False)
    task_id = db.Column(db.Text,nullable=True)
    task_doer_group = db.Column(db.Text,nullable=True)
    input = db.Column(db.Text,nullable=True)
    doer_identifier = db.Column(db.Text,nullable=True)
    doer_id = db.Column(db.Text,nullable=True)
    doer = db.Column(db.Text,nullable=True)

# Modulemaster table
class Modulemaster(db.Model):
    uid = db.Column(db.BigInteger, primary_key=True,nullable=False)
    fms_type = db.Column(db.Text,nullable=True)
    module_id = db.Column(db.Text,nullable=True)
    module_display_name = db.Column(db.Text,nullable=True)
    module_owner_id = db.Column(db.Text,nullable=True)
    module_owner = db.Column(db.Text,nullable=True)
    pc_code = db.Column(db.Text,nullable=True)
    dme_id = db.Column(db.Text,nullable=True)
    dme_code = db.Column(db.Text,nullable=True)
    dme_name = db.Column(db.Text,nullable=True)

# Outputmaster table
class Outputmaster(db.Model):
    uid = db.Column(db.BigInteger,primary_key=True,nullable=False)
    module_id = db.Column(db.Text,nullable=True)
    process_id = db.Column(db.Text,nullable=True)
    task_id = db.Column(db.Text,nullable=True)
    ln_id = db.Column(db.Text,nullable=True)
    input_id = db.Column(db.Text,nullable=True)
    output_id = db.Column(db.Text,nullable=True)
    values = db.Column(db.Text,nullable=True)
    email_id = db.Column(db.Text,nullable=True)
    employee_id = db.Column(db.Text,nullable=True)
    mob_number = db.Column(db.Text,nullable=True)

# Processmaster table
class Processmaster(db.Model):
    uid = db.Column(db.BigInteger,primary_key=True,nullable=False)
    module_id = db.Column(db.Text,nullable=True)
    process_id = db.Column(db.Text,nullable=True)
    process_display_name = db.Column(db.Text,nullable=True)
    dashboard_tab = db.Column(db.Text,nullable=True)
    process_owner_id = db.Column(db.Text,nullable=True)
    process_owner_name = db.Column(db.Text,nullable=True)
    db_name = db.Column(db.Text,nullable=False)
    table_name = db.Column(db.Text,nullable=False)

# Taskmaster table
class Taskmaster(db.Model):
    uid = db.Column(db.BigInteger,primary_key=True,nullable=False)
    module_id = db.Column(db.Text,nullable=True)
    process_id = db.Column(db.Text,nullable=True)
    task_id = db.Column(db.Text,nullable=True)
    task_display_name = db.Column(db.Text,nullable=True)
    descr = db.Column(db.Text,nullable=True)
    role = db.Column(db.Text,nullable=True)
    how = db.Column(db.Text,nullable=True)
    tat = db.Column(db.Text,nullable=True)
    tat_unit = db.Column(db.Text,nullable=True)
    predecessor = db.Column(db.Text,nullable=True)
    successor = db.Column(db.Text,nullable=True)

# Employee Master
class Employeemaster(db.Model):
    __bind_key__ = 'operation_master'  # This line specifies that this model is associated with the 'operation_master' connection
    uid = db.Column(db.BigInteger, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=True)
    employee_code = db.Column(db.Text, nullable=True)
    designation = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)
    contact = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True)
    dob = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)
    combo = db.Column(db.Text, nullable=True)

# Project Master
class Projectmaster(db.Model):
    __bind_key__ = 'operation_master'
    uid = db.Column(db.BigInteger, primary_key=True, nullable=False)
    location = db.Column(db.Text, nullable=True)

# MDO Doer Change
class Mdo(db.Model):
    __bind_key__ = 'ht_dp_mdo'
    sno = db.Column(db.BigInteger, primary_key=True, nullable=False)
    task_id = db.Column(db.Text, nullable=True)
    ln_id = db.Column(db.Text, nullable=True)
    project = db.Column(db.Text, nullable=True)
    module = db.Column(db.Text, nullable=True)
    processes = db.Column(db.Text, nullable=True)
    tasks = db.Column(db.Text, nullable=True)
    existing_doer = db.Column(db.Text, nullable=True)
    new_doer = db.Column(db.Text, nullable=True)
    new_doer_mobile = db.Column(db.Text, nullable=True)
    process_owner = db.Column(db.Text, nullable=True)
    kind_of_request = db.Column(db.Text, nullable=True)
    reason_of_request = db.Column(db.Text, nullable=True)
    planned = db.Column(db.Text, nullable=True)
    actual = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True)
    tat = db.Column(db.Text, nullable=True)
    tat_unit = db.Column(db.Text, nullable=True)
    nexttaskid = db.Column(db.Text, nullable=True)
    nexttaskplanneddate = db.Column(db.Text, nullable=True)
    uid = db.Column(db.BigInteger, nullable=True)

def split_string(value, delimiter):
    return value.split(delimiter)

app.jinja_env.filters['split'] = split_string

with app.app_context():
    db.create_all()

Session = sessionmaker()
session = Session()
@app.before_request
def before_request():
    g.db_session = Session(bind=current_app.config['SQLALCHEMY_DATABASE_URI'])

@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'db_session'):
        g.db_session.close()

@app.route('/')
def taskform():
    
    parameters = {}
    for key, value in request.args.items():
        parameters[key]=value

    join = ', '.join(parameters)
    uview = Userview.query.filter_by(ln_id=parameters.get('lnid', '')).first()
    tasks = Taskmaster.query.filter_by(task_id=uview.task_id).first()
    inputs = Inputmaster.query.filter_by(task_id=tasks.task_id).all()
    locations = db.session.query(distinct(Projectmaster.location)).all()
    # print(tasks.task_id)
    # for i in locations:
    #     print(i.location)

    return render_template('taskform.html',current_year=get_current_year(), tasks=tasks, parameters=parameters, inputs=inputs)

@app.route('/index', methods=['GET','POST'])
def index():    
    for key, value in request.args.items():
        parameters[key]=value
    join = ', '.join(parameters)
    # Database calls,
    uview = Userview.query.filter_by(ln_id=parameters.get('lnid', '')).first()
    tasks = Taskmaster.query.filter_by(task_id=uview.task_id).first()
    inputs = Inputmaster.query.filter_by(task_id=tasks.task_id).all()
    inputs_first = Inputmaster.query.filter_by(task_id=tasks.task_id).first()
    # Database table data to be returned to JS,
    inputs_json = []
    # Inputs for the current tasks.
    for input_item in inputs:
        input_dict = {
            'uid': input_item.uid,
            'module_id': input_item.module_id,
            'process_id': input_item.process_id,
            'task_id': input_item.task_id,
            'input_id': input_item.input_id,
            'input_type': input_item.input_type,
            'input_display_name': input_item.input_display_name,
            'input_variables': input_item.input_variables,
            'data_call_table_name': input_item.data_call_table_name,
        }
        inputs_json.append(input_dict)
    
    processes = Processmaster.query.all()
    process_arr = []
    proc_attr = Processmaster.__table__.columns.keys()
    proc_row = []
    for process in processes:
        # Extract specific attributes from the process object and add them to the current_row
        for attr_name in proc_attr:
            attr_value = getattr(process, attr_name)
            proc_row.append(attr_value)

        if len(proc_row) == len(proc_attr):
            process_arr.append(proc_row)
            proc_row = []  # Reset the current_row

    # Add any remaining data if it doesn't fill a complete row
    if proc_row:
        process_arr.append(proc_row)
        
    # print(process_arr)
    task = Taskmaster.query.all()
    task_attr = Taskmaster.__table__.columns.keys()
    task_arr = []
    task_row = []
    for ts in task:
        for attr_task in task_attr:
            attr_value = getattr(ts, attr_task)
            task_row.append(attr_value)

        if len(task_row) == len(task_attr):
            task_arr.append(task_row)
            task_row = []
    
    if task_row:
        task_arr.append(task_row)

    js_data = {
        "current_year": get_current_year(),
        "parameters": parameters,
        "inputs": inputs_json,
        "inputs_first": inputs_first,
        "processes": process_arr,
        "tasks": task_arr
    }

    return render_template('index.html',current_year=get_current_year(),parameters=parameters, inputs=inputs_json, inputs_first=inputs_first,processes=process_arr,tasks=task_arr,data=js_data)
    
@app.route('/input_partial', methods=['GET','POST'])
def input_partial():
    
    uview = Userview.query.filter_by(ln_id=parameters.get('lnid', '')).first()
    tasks = Taskmaster.query.filter_by(task_id=uview.task_id).first()
    inputs = Inputmaster.query.filter_by(task_id=tasks.task_id).order_by(asc(Inputmaster.input_number)).all()
    inputs_first = Inputmaster.query.filter_by(task_id=tasks.task_id).first()
    locations = Projectmaster.query.all()
    modules = Modulemaster.query.all()
    employees = Employeemaster.query.all()
    tasks = Taskmaster.query.all()
    processes = Processmaster.query.all()

    inputs_json = []
    
    for input_item in inputs:
        input_dict = {
            'uid': input_item.uid,
            'module_id': input_item.module_id,
            'process_id': input_item.process_id,
            'task_id': input_item.task_id,
            'input_id': input_item.input_id,
            'input_type': input_item.input_type,
            'input_display_name': input_item.input_display_name,
            'input_variables': input_item.input_variables,
            'data_call_table_name': input_item.data_call_table_name,
        }
        inputs_json.append(input_dict)

    

    clickCount = request.args.get('clickCount', 0)

    return render_template('_input_partial.html',inputs=inputs, inputs_first=inputs_first,parameters=parameters,clickCount = clickCount, locations = locations, modules = modules, employees = employees, tasks = tasks,processes=processes)

def get_current_year():
    return datetime.now().year

@app.route('/submit_data_to_python', methods=['POST'])
def submit_data():
    data = request.get_json()    
    # print(data)
    dbname = Processmaster.query.filter_by(process_display_name=data[0]['pro']).first_or_404().db_name
    tablename = Processmaster.query.filter_by(process_display_name=data[0]['pro']).first_or_404().table_name
    clickCount = data[0]['clickCount']
    # print(clickCount)
    ln_id = data[0]['lnid']
    # print(dbname, tablename, ln_id)
    # Udate Userview Table
    uView = Userview.query.filter_by(ln_id=data[0]['lnid']).first_or_404()
    taskid = uView.task_id
    tMaster = Taskmaster.query.filter_by(task_id = taskid).first()
    successor = tMaster.successor
    tat = tMaster.tat
    tunit = tMaster.tat_unit
    uView.actual=data[0]['date_0']
    uView.ln_status="Completed"
    db.session.commit()
    inputs = Inputmaster.query.filter_by(task_id=uView.task_id).all()
    # Update the Process Table
    
    engine = create_engine(app.config['SQLALCHEMY_BINDS'][dbname])
    metadata = MetaData()
    table = Table(tablename, metadata, autoload_with=engine)
    headers = table.columns.keys()
    
    print("Table Headers for", tablename, "in", dbname, "database:", headers)
    for j in inputs:
        parts = j.input_id.split('.')
        # print(j.input_id)
        for k in range(len(headers)):
            # print(headers[k])
            # print(j.input_display_id)                
            for i in range(clickCount):
                if int(clickCount) == 1:
                    if headers[k] == j.input_display_id:
                        new_value = data[i]['ts_'+str(i+1)+'_'+str(int(parts[-1]) - 1)]
                        column_name = headers[k]                        
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()
                    elif headers[k] == 'actual':
                        new_value = data[i]['date_0']
                        column_name = headers[k]
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()   
                    elif headers[k] == 'status':
                        new_value = "Completed"
                        column_name = headers[k]
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()
                    elif headers[k] == 'nexttaskid':
                        new_value = successor
                        column_name = headers[k]
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()
                    elif headers[k] == 'nexttaskplanneddate':
                        new_value = (datetime.strptime(data[i]['date_0'], '%d-%b-%Y %H:%M:%S') + timedelta(days=tat)).strftime('%y-%m-%d %H:%M:%S')
                        column_name = headers[k]
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()
                    elif headers[k] == 'uid':
                        new_value = str(int(round(time.time() * 1000)))+"_"+str(i+1)
                        column_name = headers[k]
                        with engine.connect() as connection:
                            # print(headers[k])
                            sql_query = text(f"UPDATE {tablename} SET {column_name} = :new_value WHERE ln_id = :ln_id")
                            connection.execute(sql_query, {'new_value': new_value, 'ln_id': ln_id})
                            connection.commit()
    return jsonify({"message": "Data submitted successfully"})

def create_directory_structure_file(root_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip the virtual environment folder
            if "venv" in dirnames:
                dirnames.remove("venv")

            depth = dirpath.count(os.sep) - root_dir.count(os.sep)
            indent = "  " * depth
            f.write(f"{indent}/{os.path.basename(dirpath)}/\n")

            for filename in filenames:
                f.write(f"{indent}  - {filename}\n")
            for dirname in dirnames:
                f.write(f"{indent}  + {dirname}/\n")




if __name__ == "__main__":
    project_root = "C:/Users/dme8/Desktop/gcp-files"  # Replace with your project's root directory
    output_filename = "project_structure.txt"

    create_directory_structure_file(project_root, output_filename)
    print(f"Directory structure saved to {output_filename}")

    # Run the Flask app
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
