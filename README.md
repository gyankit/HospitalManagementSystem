# HospitalManagementSystem

Initialization

The website for this hospital management system was built using python-flask. Please read through the steps below to get the website working.

Requirements : 
1) Make sure you have python installed (python 3.8 or above recommended)
2) Have the virtual environment package pipenv installed
Command to install : pip install pipenv

Steps :
1) Create a virtual environment and activate it.
Command : py - m venv venv
To activate : venv\Scripts\activate

2) Use the Requirements file to install other necessary packages in the venv.
Command : pip install -r requirements.txt
In case a package does not get installed, try downloading its .whl file from 	websites like pypi.org, etc. and install it using pip install some-package.whl

3) Run the admin.py file using, python admin.py 
   If it throws an error you already have the default user created. 
Note : default username : admin,  password : admin
To create another user change the credentials inside the admin.py file and execute it.

4) Once all the above steps are done, execute the command : flask run.
5) In your browser go to - localhost:5000 to visit the website and you should be able to see the login page.
Note : To run flask in development mode make sure FLASK_ENV=development is not commented in the .env file and vice versa.

The website was built and tested using Python 3.8.x and the packages as mentioned in the requirements.txt file. Any packages not installed may cause errors. The website was tested in Google chrome, Mozilla Firefox and Microsoft Edge. There may be errors if using Internet explorer because it may not support the bootstrap version used.



USER LOGIN

Login using the default username(admin) and password(admin). Other login credentials can be created as mentioned in step 3 of initialization.


OPTIONS IN HEADER - PATIENT 

NEW PATIENT REGISTRATION

Go to ‘NEW REGISTRATION’ under the ‘PATIENT’ option in the header to open the patient registration page. The SSN Id (unique 9 digit serially ordered number) of the patient is generated automatically to help keep track of the total number of patients at a quick glance. Fill in the other details and click on Submit to register the patient.
Upon successful patient registration an unique random 9 digit ‘Patient Id’ is generated which is displayed with a success message. This patient id is the key factor for performing all patient related tasks. To view the patient id later refer to the ALL RECORDS section.

SINGLE RECORD

To search for a particular patient using his/her unique ‘Patient Id’. Patients already discharged cannot be viewed from this section.

UPDATE RECORD

To update the details of a particular patient after searching with his/her ‘Patient Id’. Details of patients already discharged cannot be updated.

DELETE RECORD

To delete the records of a patient who is discharged. If an attempt is made to delete the records of a patient who is not discharged, the page will be redirected to the BILLING DETAILS of that patient so that he/she can be discharged and then his/her records can be deleted.



BILLING DETAILS

To generate the bill of a patient with the option of downloading the bill in a pdf format. 
Note : Once Confirm & Proceed is selected in the Confirmation pop up, the patient will be discharged. This is irreversible. Selecting Cancel on the pop up, or redirecting to another page before Confirming will not discharge the patient.

ALL DETAILS

To view the details of all the patients admitted, both available and discharged, the status being clearly mentioned for each patient. The ‘Patient Id’ parameter can be viewed and copied from here for other tasks related to a specific patient.


OPTIONS IN HEADER - TREATMENT

PHARMACIST

To view previously issued medicines and to issue new ones to a specific patient. To issue new medicines click on ‘Issue Medicines’. Then select the medicine and the quantity to be issued to the patient. Multiple medicines can be issued at once. When all medicines and their respective quantities are added, click on ‘Update’ to finalize the medicines issued. Once updated, this is irreversible.
Note : Medicines that are out of stock cannot be issued.

DIAGNOSTIC

To view previously issued tests and to issue new tests to a specific patient. To issue new tests click on ‘Issue Tests’. Then select the test to be issued. Multiple tests can be issued at once. To finally confirm the selection of tests and issue them click on ‘Update’. Once updated, this is irreversible.



OPTIONS IN HEADER - STORE

ADD MEDICINES

To add a completely new medicine to the medicine store. Specify the name, quantity to add and its rate, then click on ‘Add Medicine’ to add it to the store. Once added the medicine can be issued to patients.

AVAILABLE MEDICINES

To view a list of all the medicines, their quantity left in stock and rate, in the store. Also medicines that have 0 quantity, I.e., they are out of stock can, be restocked using the ‘Update’ option of the corresponding medicine. ‘Update’ can also be used to modify the quantity and the rates of a medicine. Similarly, to completely remove a medicine from the stock, use the corresponding ‘Delete’ option.

ADD DIAGNOSTIC

To add a completely new medical test to the diagnostic store. Specify the name, and its rate, then click on ‘Add Test’ to add it to the store. Once added the Test can be issued to patients.

AVAILABLE DIAGNOSTICS

To view a list of all the available tests, and their rates. The ‘Update’ option can be used to modify the rates of the corresponding test. To completely remove a test from the store, use the corresponding ‘Delete’ option.


OPTIONS IN HEADER - LOGOUT

To logout from the current session and return to the login page.

