# *A comprehensive Hospital Management System API built with Django REST Framework.*
> Manage users, appointments, prescriptions, medications, and patient records with role-based access for doctors, patients, pharmacists, and admins.

---

## 🔗 Live API

The API is deployed on PythonAnywhere for assessment and demonstration.

👉 **[View Live API](https://tsewayo.pythonanywhere.com/)**

---

## 📁 Project Structure

```
hospital_management/
├── api-documentation.md
├── manage.py
├── users/
├── prescriptions/
├── appointments/
├── medications/
├── patient_records/
└── hospital_api/
```

---

## 👥 User Roles

The system supports the following roles, each with specific access and functionality:

- **Admin**
- **Doctor**
- **Patient**
- **Pharmacist**

---

## 🔐 Authentication

- Token-based authentication
- Users log in to receive an authentication token
- Include the token in the header for all authenticated requests:

```
Authorization: Token your_token_here
```

---

## 🧩 Core Features

### ✅ User Management (`/api/users/`)
- Registration and login
- Role-based profile creation (Doctor, Patient, Pharmacist)
- Token authentication

### 💊 Prescriptions (`/api/prescriptions/`)
- Doctors can create prescriptions
- Pharmacists can view all prescriptions
- Patients can view their own prescriptions

### 📋 Patient Records (`/api/patient-records/`)
- Medical records, lab results, and diagnosis
- Only doctors can create/edit
- Patients can view their own records

### 🗓️ Appointments (`/api/appointments/`)
- Patients can book appointments
- Doctors can view and update appointment statuses

### 💉 Medications (`/api/medications/`)
- CRUD operations for medications
- Managed primarily by pharmacists

---

## ⚙️ API Endpoints

A full list of endpoints and request/response examples can be found in the [API Documentation](api-documentation.md).

---

## 📦 Setup Instructions

1. **Clone the project**

```bash
git clone https://github.com/your-username/hospital-management-api.git
cd hospital-management-api
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**

```bash
python manage.py createsuperuser
```

6. **Run the server**

```bash
python manage.py runserver
```

---

## 📄 API Testing

You can test the endpoints using tools like:

- **Postman**
- **cURL**
- **Python requests**
- **DRF’s built-in API browser**

---

## 🧪 Example Usage

```bash
# Register a user
POST /api/users/register/
{
  "username": "john_doe",
  "password": "securepass123",
  "role": "doctor"
}

# Login
POST /api/users/login/
{
  "username": "john_doe",
  "password": "securepass123"
}

# Create a prescription
POST /api/prescriptions/
Headers: Authorization: Token your_token_here
{
  "patient": 2,
  "medication_name": "Amoxicillin",
  "dosage": "500mg twice daily"
}
```

---

## ✅ Requirements

- Python 3.8+
- Django 4.x
- Django REST Framework

---

## 🚀 Deployment

Deployed via PythonAnywhere. Follow the [PythonAnywhere Django guide](https://help.pythonanywhere.com/pages/DeployingDjango/) for setup.

---

## 📚 License

This project is licensed for educational purposes as part of a capstone project at ALX.

---

## 🙋🏾‍♀️ Author

**Gifty Dede Tsewayo**
Back-end Engineering Student @ ALX Africa & Pharmacy Student
GitHub: [@dev-dede](https://github.com/dev-dede/)`

---