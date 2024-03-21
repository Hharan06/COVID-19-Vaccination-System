from pyexpat.errors import messages
from django.db import connection
from django.shortcuts import render,redirect
from .models import HealthCareInformation,Patients,Vaccine

# Create your views here.
def create_tables():
    with connection.cursor() as cursor:
        # Define SQL queries for creating tables
        create_healthcare_table_query = """
            CREATE TABLE IF NOT EXISTS healthcareinformation (
                name VARCHAR(255) PRIMARY KEY,
                doctor VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20),
                city VARCHAR(255),
                location VARCHAR(255)
            );
        """

        create_login_table_query = """
            CREATE TABLE IF NOT EXISTS login (
                username VARCHAR(255) PRIMARY KEY,
                email VARCHAR(255),
                password VARCHAR(255)
            );
        """

        create_vaccine_table_query = """
            CREATE TABLE IF NOT EXISTS vaccine (
                name VARCHAR(255),
                vaccine_id VARCHAR(255),
                type VARCHAR(255),
                doses INT,
                start_date DATE,
                end_date DATE,
                PRIMARY KEY(vaccine_id),
                FOREIGN KEY(name) REFERENCES healthcareinformation(name) ON DELETE CASCADE
            );
        """

        create_patients_table_query = """
            CREATE TABLE IF NOT EXISTS patients (
                healthcare VARCHAR(255),
                name VARCHAR(255),
                age INT,
                aadhar VARCHAR(255),
                phone VARCHAR(20),
                vaccine_id VARCHAR(50),
                dose INT,
                date_selected VARCHAR(100),
                PRIMARY KEY(address),
                FOREIGN KEY(healthcare) REFERENCES healthcareinformation(name) ON DELETE CASCADE,
                FOREIGN KEY(vaccine_id) REFERENCES vaccine(vaccine_id) ON DELETE CASCADE
            );
        """

create_tables()

def home(request):
    with connection.cursor() as cursor:
        cursor.execute('''
                    SELECT h.city,COUNT(p.name) AS Total,
                    CAST(SUM(CASE WHEN p.dose = 1 THEN 1 ELSE 0 END) AS SIGNED) AS Dose1,
                    CAST(SUM(CASE WHEN p.dose = 2 THEN 1 ELSE 0 END) AS SIGNED) AS Dose2
                    FROM patients p
                    JOIN healthcareinformation h ON h.name = p.healthcare
                    GROUP BY h.city
                    ORDER BY Total DESC; 
                    ''')
        data=cursor.fetchall()
        result=[]
        for data in data:
            result.append(data)
    return render(request,'home.html',{'overall':result})

def login(request):
    return render(request,'login.html')

def enroll(request):
    if request.method == 'POST':
        name = request.POST.get('providerName')
        contact = request.POST.get('contactPerson')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        location = request.POST.get('location')

        raw_sql_query = """
            INSERT INTO healthcareinformation
            (name, contact, email, phone, city, location) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = [name, contact, email, phone, city, location]

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)

        return render(request, 'create_account.html')

    return render(request, 'enroll.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        raw_sql_query = "INSERT INTO login (username, email, password) VALUES (%s, %s, %s)"
        params = [username, email, password]

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)

        return render(request, 'login.html')


def login_authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        healthcare = request.POST.get('healthcare')
        password = request.POST.get('password')

        raw_sql_query = """
            SELECT * 
            FROM login 
            WHERE username = %s AND password = %s
        """
        params = [username, password]

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)
            obj = cursor.fetchone()

        if obj:
            request.session['healthcarename'] = healthcare
            request.session['health'] = healthcare
            return render(request, 'dashboard.html')

    # Handle invalid login or other cases
    return render(request, 'login.html')

def vaccine_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        vaccine_id = request.POST.get('id')
        vaccine_type = request.POST.get('vaccineType')
        available_doses = request.POST.get('availableDoses')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        raw_sql_query = """
            INSERT INTO vaccine 
            (name, vaccine_id, type, doses, start_date, end_date) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = [name, vaccine_id, vaccine_type, available_doses, start_date, end_date]

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)

        return render(request, 'dashboard.html')

    return render(request, 'vaccine_appointment.html')

def patient_dashboard(request):
    city_search = request.GET.get('citySearch')
    raw_sql_query="""
            SELECT * FROM healthcareinformation
            WHERE TRIM(city)=%s
            """
    param=[city_search]
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query,param)
        data=cursor.fetchall()
        result=[]
        for data in data:
            result.append(data)

    return render(request, 'patients_dashboard.html', {'datas': result})


def patients(request):
    return render(request,'patients_dashboard.html')

def vaccine_display(request, name):
    # Retrieve data using raw SQL query
    raw_sql_query_select = """
        SELECT * 
        FROM vaccine 
        WHERE name = %s
    """
    params_select = [name]
    datas=Vaccine.objects.filter(name=name)

    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query_select, params_select)
        data = cursor.fetchall()
        result=[]
        for data in data:
            result.append(data)

    if request.method == 'POST':
        # Insert data using raw SQL query
        healthcare = request.POST.get('healthcare')
        patient_name = request.POST.get('patientName')
        patient_age = request.POST.get('patientAge')
        patient_address = request.POST.get('patientAddress')
        vaccine_id = request.POST.get('vaccine_id')
        patient_dose = request.POST.get('patientDose')
        patient_phone = request.POST.get('patientPhone')
        patient_date = request.POST.get('patientDate')

        raw_sql_query_insert = """
            INSERT INTO patients 
            (healthcare, name, age, address, vaccine_id, phone, dose, date_selected) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params_insert = [healthcare, patient_name, patient_age, patient_address, vaccine_id, patient_phone, patient_dose, patient_date]

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query_insert, params_insert)

        return redirect("home")

    return render(request, 'patients.html', {'vaccines': result})
  

def patient_information(request):
    name = request.session.get('healthcarename')
    if name:
        raw_sql_query = """
            SELECT p.healthcare,p.name,p.age,p.address,p.phone,p.vaccine_id,p.dose,p.date_selected,v.type 
            FROM patients p
            JOIN vaccine v on v.vaccine_id=p.vaccine_id
            WHERE healthcare = %s
            ORDER BY name
        """
        params = [name]
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)
            data = cursor.fetchall()
            result=[]
            for data in data:
                result.append(data)

        return render(request, 'patient_information.html', {'patients': result})
    else:
        return render(request, 'patient_information.html', {'patients': []})

def vaccine_information(request):
    # Retrieve the name from the session
    name = request.session.get('healthcarename')
    
    if name:
        raw_sql_query = """
            SELECT * 
            FROM vaccine 
            WHERE name = %s
        """
        params = [name]
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)
            data = cursor.fetchall()
            result=[]
            for data in data:
                result.append(data)

        return render(request, 'vaccine_information.html', {'vaccines': result})
    else:
        return render(request, 'vaccine_information.html', {'vaccines': []})

def aadhar(request):
    if request.method == 'POST':
        aadhar_number = request.POST.get('aadharNumber')

        raw_sql_query = """
            SELECT * 
            FROM patients 
            WHERE address = %s
        """
        params = [aadhar_number]
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, params)
            data = cursor.fetchall()
            result=[]
            for data in data:
                result.append(data)

        return render(request, 'certificate.html', {'patients': result})

    return render(request, 'get_aadhar.html')

def delete_patient(request, aadhar):
    raw_sql_query = """
        DELETE FROM patients 
        WHERE address = %s
    """
    params = [aadhar]

    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query, params)

    return redirect("patient_information")

def delete_vaccine(request, vaccine_id):
    raw_sql_query = """
        DELETE FROM vaccine 
        WHERE vaccine_id = %s
    """
    params = [vaccine_id]

    with connection.cursor() as cursor:
        cursor.execute(raw_sql_query, params)

    return redirect("vaccine_information")

def update_patients(request, aadhar):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        dose = request.POST.get('dose')
        date = request.POST.get('date')

        raw_sql_query = """
            UPDATE patients
            SET name=%s, age=%s, address=%s, phone=%s, dose=%s, date_selected=%s
            WHERE TRIM(address)=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, [name, age, address, phone, dose, date, address])

        return redirect('patient_information')

    raw_sql = """
        SELECT * FROM patients
        WHERE address = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(raw_sql, [aadhar])
        data = cursor.fetchall()

    result = []
    for row in data:
        result.append(row)

    return render(request, 'update_patient.html', {'patients': result})

def update_vaccines(request, vaccine_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        vaccine_id = request.POST.get('vaccine_id')
        type = request.POST.get('type')
        doses = request.POST.get('doses')

        raw_sql_query = """
            UPDATE vaccine
            SET name=%s, vaccine_id=%s, type=%s, doses=%s
            WHERE TRIM(vaccine_id)=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query, [name, vaccine_id, type, doses, vaccine_id])

        return redirect('vaccine_information')

    raw_sql = """
        SELECT * FROM vaccine
        WHERE vaccine_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(raw_sql, [vaccine_id])
        data = cursor.fetchall()

    result = []
    for row in data:
        result.append(row)

    return render(request, 'update_vaccine.html', {'vaccines': result})