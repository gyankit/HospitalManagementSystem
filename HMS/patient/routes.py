from HMS import db, bcrypt
from HMS.patient import patient
from flask import render_template, redirect, request, url_for, flash, jsonify, abort
from flask_login import login_required
from HMS.patient.forms import PatientRegistrationForm, PatientUpdateForm, PatientDischarge, PatientDelete
from HMS.cities import getstates, getcities
from HMS.models import Patient, Medicines, Diagnostics, MedicineMaster, DiagnosticMaster
from random import randint
import json
from datetime import datetime


def random_num():
    start = 10**8
    end = (10**9)-1
    return randint(start, end)

def checkPid(pid, status=None):
    if status is None:
        patient = Patient.query.filter_by(patientId=pid).first_or_404()
    else:
        patient = Patient.query.filter_by(patientId=pid, status=status).first_or_404()
    if patient:
        return patient


# City Route
@patient.route('/city/<selectState>')
@login_required
def city(selectState):
    states = getstates()
    for i, state in enumerate(states):
        if state == selectState:
            n = i
            break
    cities = getcities()[int(n)]
    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[1]
        cityArray.append(cityObj)
    return jsonify({'cities': cityArray})


# Patient Route
@patient.route('/register', methods=['GET', 'POST'])
@login_required
def register(): 
    title = 'Namaste Hospitals | Patient Registration'
    form = PatientRegistrationForm()
    form.ssnid.data = int(Patient.query.count()) + 100000001
    if request.method == 'POST' and form.validate_on_submit():
        doa = request.form.get('dateOfAdmission')
        id=0
        while True:
            id = random_num()
            if not Patient.query.filter_by(patientId=id).first():
                break
        newPatient = Patient(
            ssnid=form.ssnid.data,
            patientId=id,
            name=request.form.get('patientName'),
            age=request.form.get('age'),
            dateOfJoining = datetime.strptime(doa, '%Y-%m-%d %H:%M:%S'),
            roomType=request.form.get('roomType'),
            address=request.form.get('patientaddress'),
            city=request.form.get('city'),
            state=request.form.get('state')
            )
        db.session.add(newPatient)
        db.session.commit()
        flash(f'Patient Registration initiated successfully! Patient Id : {id}', 'success')
        return redirect(url_for('patient.register'))
    return render_template('patient/register.html', title=title, form=form, cdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Update Patient
@patient.route('/update', methods=['GET','POST'])
@login_required
def update():
    pid = request.args.get('pid')
    if pid is None:
        return redirect(url_for('main.search', next='patient.update'))
    p = checkPid(pid, True)
    title = 'Namaste Hospitals | Patient Update'
    form = PatientUpdateForm()
    form.patientId.data = p.patientId
    form.name.data = p.name
    form.age.data = p.age
    form.address.data = p.address
    form.state.data = p.state
    form.city.data = p.city
    if request.method == 'POST' and form.validate_on_submit():
        p.name = request.form.get('name')
        p.age = request.form.get('age')
        p.address = request.form.get('address')
        p.state = request.form.get('state')
        if request.form.get('city'):
            p.city = request.form.get('city')
        db.session.commit()
        flash(f'Patient Updation initiated successfully! Patient Id : {pid}','success')
        return redirect(url_for('patient.details', pid=pid))
    return render_template('patient/update.html', form=form, title=title, patient=p)
        

    
#delete Patient
@patient.route('/delete', methods=['GET','POST'])
@login_required
def delete():
    pid = request.args.get('pid')
    if pid is None:
        return redirect(url_for('main.search', next='patient.delete'))
    p = checkPid(pid)
    title = 'Namaste Hospitals | Patient Delete'
    form = PatientDelete()
    form.pid.data = pid
    if request.method == 'POST' and form.validate():
        id = request.form.get('pid')
        if p.status:
            flash(f'Awaiting Payment for Patient. Redirecting to Billing page...', 'danger')
            return redirect(url_for('patient.billing', next='patient.delete', pid=id))
        else:
            Medicines.query.filter_by(patientId=id).delete()
            Diagnostics.query.filter_by(patientId=id).delete()
            Patient.query.filter_by(patientId=id).delete()
        db.session.commit()
        flash(f'Patient Deletion initiated successfully! Patient Id: {id}','success')
        return redirect(url_for('main.home'))
    return render_template('patient/delete.html', p=p, form=form)


# Patient Details Route
@patient.route('/details-single', methods=['GET', 'POST'])
@login_required
def details():
    pid = request.args.get('pid')
    if pid is None:
        return redirect(url_for('main.search', next='patient.details'))
    title = 'Namaste Hospitals | Patient | Details'
    p = checkPid(pid)
    if p.status is False:
        flash(f'Patient with id : {pid} is discharged. To check details go to All Records.', 'danger')
        return redirect(url_for('patient.details'))
    return render_template('patient/patientDetails.html', p=p, pid=pid)


# Patients Status Route
@patient.route('/details-all', methods=['GET', 'POST'])
@login_required
def status():
    title = 'Namaste Hospitals | Patient | Status'
    patient = Patient.query.all()
    return render_template('patient/allPatientsDetails.html', patient=patient)


# Patient Billing Route
@patient.route('/billing')
@login_required
def billing():
    pid = request.args.get('pid')
    nexturl = request.args.get('next')
    if pid is None:
        return redirect(url_for('main.search', next='patient.billing'))
    patient = checkPid(pid)
    title = 'Namaste Hospitals | Patient Billing'
    form = PatientDischarge()
    form.pid.data = pid
    form.nexturl.data = nexturl
    btn = True
    if patient.dateOfDischarge:
        dod = patient.dateOfDischarge
        flash(f'Patient with id : {pid} is already discharge', 'info')
        btn = False
    else:
        dod = datetime.now().replace(microsecond=0)
    personal = [patient.name, patient.age, f'{patient.address}, {patient.city}, {patient.state}']
    dates = [patient.dateOfJoining, dod ]
    if patient.roomType == 'General' :
        roomtype = 'General ward'
        roomrent = 2000
    elif patient.roomType == 'Sharing':
        roomtype = 'Semi sharing'
        roomrent = 4000
    else:
        roomtype = 'Single room'
        roomrent = 8000
    datediff = dates[1]-dates[0]
    dateHr = datediff.total_seconds() // 3600
    daycount = f'{int(dateHr // 24)} Days {int(dateHr % 24)} hours'
    money = round(((roomrent*(dateHr // 24))+((roomrent / 24)*(dateHr % 24))), 2)
    rents = [roomtype, daycount, roomrent, money]
    mamount = tamount = 0
    medicines = []
    mids = Medicines.query.filter_by(patientId=pid).all()
    for i in range(len(mids)):
        med = {}
        medicine = MedicineMaster.query.filter_by(medicineId=mids[i].medicineId).first()
        med['count'] = i+1;
        med['name'] = medicine.medicineName
        med['qty'] = mids[i].quantity
        med['rate'] = medicine.rate
        med['amount'] = mids[i].quantity*medicine.rate
        medicines.append(med)
        mamount += mids[i].quantity*medicine.rate
    tests = []
    dids = Diagnostics.query.filter_by(patientId=pid).all()
    for i in range(len(dids)):
        tt = {}
        test = DiagnosticMaster.query.filter_by(testId=dids[i].testId).first()
        tt['count'] = i+1;
        tt['name'] = test.testName
        tt['rate'] = test.rate
        tests.append(tt)
        tamount += test.rate
    totalamount = [mamount, tamount]
    return render_template('patient/billing.html', title=title, medicines=medicines, tests=tests, personal=personal, dates=dates, rents=rents, totalamount=totalamount, pid=pid, btn=btn, form=form)


# Generate PDF Route
@patient.route('/genratePDF', methods=['POST'])
@login_required
def genPDF():
    pid = request.form.get('pid')
    nexturl = request.form.get('nexturl')
    if pid is None:
        abort(404)
    checkPid(pid, True)
    data = {
        "pid" : pid,
        "next" : nexturl,
        "dod" : request.form.get('dateOfDischarge'),
        "key" : bcrypt.generate_password_hash(pid).decode('utf-8'),
        "formData" : request.form.get('formData')
    }
    return render_template('patient/genratePdf.html', title=f'Billing Details | {pid}', data=data)


# Patient Discharge Route
@patient.route('/patientDischarge')
@login_required
def discharge():
    pid = request.args.get('pid')
    nexturl = request.args.get('next')
    dod = request.args.get('dod')
    key = request.args.get('key')
    if pid and bcrypt.check_password_hash(key, pid):
        p = checkPid(pid, True)
        print(p)
        p.dateOfDischarge = datetime.strptime(dod, '%Y-%m-%d %H:%M:%S')
        p.status = False
        db.session.commit()
        return redirect(url_for(nexturl or 'patient.billing', pid=pid))
    else:
        abort(404)
