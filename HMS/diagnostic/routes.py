from HMS import db
from HMS.diagnostic import diagnostic
from flask import render_template, redirect, request, url_for, flash, abort, jsonify
from flask_login import login_required
from HMS.diagnostic.forms import *
from HMS.models import DiagnosticMaster, Patient, Diagnostics
from HMS.patient.routes import checkPid


#Patient Details Routes
@diagnostic.route('/diagnostic', methods=['GET', 'POST'])
@login_required
def details():
    pid = request.args.get('pid')
    if pid is None:
        return redirect(url_for('main.search', next='diagnostic.details'))
    patient = checkPid(pid, True)
    title = 'Namaste Hospitals | Diagnostics'
    if request.method == 'POST':
        display = True
        id = request.form.get('submitId')
        id = list(id.split(","))  
        for i in range(len(id)):
            test = Diagnostics(patientId=pid, testId=id[i])
            db.session.add(test)
        db.session.commit()
        flash(f'New Tests issued to Patiend Id : {pid}', 'success')
        return redirect(url_for('diagnostic.details', pid=pid))
    issuetests = []
    form = DiagnosticSubmitForm()
    tests = DiagnosticMaster.query.all();
    issues = Diagnostics.query.filter_by(patientId=pid).all();
    for issue in issues:
        issueData = {}
        testDetail = DiagnosticMaster.query.filter_by(testId=issue.testId).first()
        issueData['name'] = testDetail.testName
        issueData['rate'] = testDetail.rate
        issuetests.append(issueData)
    return render_template('diagnostic/patienttests.html', title=title, form=form, pid=pid, tests=tests, patient=patient, issuetests=issuetests)



@diagnostic.route('/testDetails', methods=['POST'])
@login_required
def testDetails():
        test = DiagnosticMaster.query.get(int(request.form.get('testId')))
        if test:
            data = {
                "id": test.testId,
                "name": test.testName,
                "rate": test.rate
            }
            return jsonify(data)
        else:
            abort(404)


@diagnostic.route('/addtest', methods=['GET', 'POST'])
@login_required
def addtest():
    title = 'Namaste Hospitals | Add Test'
    form = AddTestForm()
    if request.method == 'POST' and form.validate_on_submit():
        test = DiagnosticMaster(testName=form.testName.data, rate=form.rate.data)
        db.session.add(test)
        db.session.commit()
        flash('New Test Successfully Added', 'success')
    return render_template('diagnostic/addtest.html', title=title, form=form)


@diagnostic.route('/allTestDetails', methods=['GET', 'POST'])
@login_required
def alltests():
    title = 'Namaste Hospitals | Diagnostics | Status'
    tests = DiagnosticMaster.query.all()
    return render_template('diagnostic/alltestdetails.html', tests=tests)


@diagnostic.route('/testDelete', methods=['GET', 'POST'])
@login_required
def testdelete():
    title = 'Namaste Hospitals | Diagnostics | Delete'
    t = request.args.get('test')
    form = TestDeleteForm()
    test = DiagnosticMaster.query.filter_by(testName=t).first()
    if request.method == 'POST':
        DiagnosticMaster.query.filter_by(testName=t).delete()
        db.session.commit()
        return redirect(url_for('diagnostic.alltests'))
    return render_template('diagnostic/deletetest.html', form=form, test=test)


@diagnostic.route('/testUpdate', methods=['GET', 'POST'])
@login_required
def testupdate():
    title = 'Namaste Hospitals | Diagnostics | Update'
    t = request.args.get('test')
    test = DiagnosticMaster.query.filter_by(testName=t).first()
    form = TestUpdateForm()
    form.testName.data = test.testName
    form.rate.data = test.rate
    if request.method == 'POST':
        rate = request.form.get('rate')
        if rate:
            test.rate = rate
        db.session.commit()
        flash(f'Diagnostic Update Successful', 'success')
        return redirect(url_for('diagnostic.alltests'))
    return render_template('diagnostic/updatetest.html', form=form)

