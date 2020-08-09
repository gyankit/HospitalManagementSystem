from HMS import db
from HMS.pharmacist import pharmacist
from flask import render_template, redirect, request, url_for, flash, abort, jsonify
from flask_login import login_required
from HMS.pharmacist.forms import MedicineStoreForm, MedicineSubmitForm, MedicineDeleteForm, MedicineUpdateForm
from HMS.models import MedicineMaster, Medicines, Patient
from HMS.patient.routes import checkPid


#Patient Details Routes
@pharmacist.route('/pharmacist', methods=['GET', 'POST'])
@login_required
def details():
    pid = request.args.get('pid')
    if pid is None:
        return redirect(url_for('main.search', next='pharmacist.details'))
    patient = checkPid(pid, True)
    title = 'Namaste Hospitals | Pharmacist'
    if request.method == 'POST':
        id = request.form.get('submitId')
        qty = request.form.get('submitQty')
        id =list(id.split(",")) 
        qty =list(qty.split(",")) 
        for i in range(len(id)):
            medDetail = MedicineMaster.query.filter_by(medicineId=id[i]).first()
            if int(medDetail.quantity) >= abs(int(qty[i])):
                medDetail.quantity = int(medDetail.quantity) - abs(int(qty[i]))
                medicine = Medicines(patientId=pid, medicineId=id[i], quantity=qty[i])
                db.session.add(medicine)
            else:
                pass
        db.session.commit()
        flash(f'New Medicines Issue to Patient ID : {pid}', 'success')
        return redirect(url_for('pharmacist.details', pid=pid))
    form = MedicineSubmitForm()
    medicines = MedicineMaster.query.all();
    issues = Medicines.query.filter_by(patientId=pid).all();
    issuemedicines = []
    for issue in issues:
        issueData = {}
        issueData['quantity'] = issue.quantity
        medDetail = MedicineMaster.query.filter_by(medicineId=issue.medicineId).first()
        issueData['name'] = medDetail.medicineName
        issueData['rate'] = medDetail.rate
        issuemedicines.append(issueData)
    return render_template('pharmacist/medicine.html', title=title, form=form, pid=pid, medicines=medicines, patient=patient, issuemedicines=issuemedicines)



@pharmacist.route('/medicineDetails', methods=['POST'])
@login_required
def medicineDetails():
        medicine = MedicineMaster.query.get(int(request.form.get('id')))
        if medicine:
            data = {
                "id": medicine.medicineId,
                "name": medicine.medicineName,
                "rate": medicine.rate
            }
            return jsonify(data)
        else:
            abort(404)

@pharmacist.route('/medicineQuantity', methods=['POST'])
@login_required
def medicineQuantity():
        medicine = MedicineMaster.query.get(int(request.form.get('id')))
        if medicine:
            return str(medicine.quantity)



@pharmacist.route('/medicineStore', methods=['GET', 'POST'])
@login_required
def medicine():
    title = 'Namaste Hospitals | Add Medicine'
    form = MedicineStoreForm()
    if request.method == 'POST' and form.validate_on_submit():
        medicine = MedicineMaster(medicineName=form.medicineName.data, quantity=form.quantity.data, rate=form.rate.data)
        db.session.add(medicine)
        db.session.commit()
        flash('New Medicine Successfully Added', 'success')
    return render_template('pharmacist/addmedicine.html', title=title, form=form)



@pharmacist.route('/allMedicineDetails', methods=['GET', 'POST'])
@login_required
def allmedicines():
    title = 'Namaste Hospitals | Medicines | Status'
    medicines = MedicineMaster.query.all()
    return render_template('pharmacist/allmedicinedetails.html', medicines=medicines)


@pharmacist.route('/medicineDelete', methods=['GET', 'POST'])
@login_required
def medicinedelete():
    title = 'Namaste Hospitals | Medicines | Delete'
    med = request.args.get('med')
    form = MedicineDeleteForm()
    medicine = MedicineMaster.query.filter_by(medicineName=med).first()
    if request.method == 'POST':
        MedicineMaster.query.filter_by(medicineName=med).delete()
        db.session.commit()
        flash(f'Medicine Removed from Store successfully', 'success')
        return redirect(url_for('pharmacist.allmedicines'))
    return render_template('pharmacist/deletemedicine.html', form=form, medicine=medicine)


@pharmacist.route('/medicineUpdate', methods=['GET', 'POST'])
@login_required
def medicineupdate():
    title = 'Namaste Hospitals | Medicines | Update'
    med = request.args.get('med')
    medicine = MedicineMaster.query.filter_by(medicineName=med).first()
    form = MedicineUpdateForm()
    form.medicineName.data = medicine.medicineName
    form.quantity.data = medicine.quantity
    form.rate.data = medicine.rate
    if request.method == 'POST':
        print(request.form)
        quantity = request.form.get('quantity')
        rate = request.form.get('rate')
        if quantity:
            medicine.quantity = quantity
        if rate:
            medicine.rate = rate
        db.session.commit()
        flash(f'Medicine Update Successful', 'success')
        return redirect(url_for('pharmacist.allmedicines'))
    return render_template('pharmacist/updatemedicine.html', form=form)

