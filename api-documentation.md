# Hospital Management System API Documentation

_Last updated: April 2025_

## Table of Contents
1. [Project Overview](#project-overview)
2. [Authentication](#authentication)
3. [User Roles & Access](#user-roles--access)
4. [Base URL & Common Headers](#base-url--common-headers)
5. [API Endpoints](#api-endpoints)
    - [Users](#users)
    - [Appointments](#appointments)
    - [Patient Records](#patient-records)
    - [Medications](#medications)
    - [Prescriptions](#prescriptions)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Notes](#notes)

---

## 1. Project Overview

This is a RESTful API for a Hospital Management System that allows different users—**Doctors, Patients, Pharmacists,** and **Admins**—to manage healthcare data. The system includes features for user registration and authentication, managing appointments, medical records (including diagnoses and lab results), medications, and prescriptions.

---

## 2. Authentication

- **Login Endpoint**: `POST /api/users/login/`  
  The API uses **Token-based Authentication**. After logging in, a token is generated that must be included in the `Authorization` header for subsequent requests.

- **Header Format**:  
  ```
  Authorization: Token <your_token_here>
  ```

- **Registration Endpoint**: `POST /api/users/register/`  
  _Note: Registration does not require authentication._

---

## 3. User Roles & Access

- **Doctor**  
  - Can create and update appointments, medical records, diagnoses, and prescriptions.  
  - Cannot update prescription status.

- **Patient**  
  - Can create appointments and view their own medical records, appointments, diagnoses, and lab results.

- **Pharmacist**  
  - Can update the status field of prescriptions and manage medications.

- **Admin**  
  - Has full access to all endpoints.

---

## 4. Base URL & Common Headers

- **General Base URL**: `/api/`
- **Users Base URL**: `/api/users/` (for authentication and profile endpoints)
- **Content-Type**: All request bodies should be sent as JSON.

---

## 5. API Endpoints

### Users (Endpoints under `/api/users/`)

| Method | Endpoint       | Description                                                        | Access        |
| ------ | -------------  | ------------------------------------------------------------------ | ------------- |
| POST   | `/register/`   | Register a new user (Doctor, Patient, Pharmacist, or Admin).       | Public        |
| POST   | `/login/`      | Log in a user and receive an authentication token.                 | Public        |
| POST   | `/logout/`     | Log out the current user (token deletion).                         | Authenticated |
| GET    | `/me/`         | Retrieve or update the authenticated user’s profile.               | Authenticated |
| GET    | `/all/`        | List all users (Admin only).                                       | Admin         |
| *Profile CRUD* | See related endpoints below for Patient, Doctor, Pharmacist profiles. |               |

**User Profile Endpoints**  
- **Patient Profile**: `/api/users/patient-profile/`  
- **Doctor Profile**: `/api/users/doctor-profile/`  
- **Pharmacist Profile**: `/api/users/pharmacist-profile/`

---

### Appointments (Endpoints under `/api/`)

| Method | Endpoint                                    | Description                                                                | Access         |
| ------ | ------------------------------------------- | -------------------------------------------------------------------------- | -------------- |
| POST   | `/appointments/create/`                     | Create a new appointment. The logged-in patient is auto-assigned.          | Patient        |
| GET    | `/my/appointments/`                         | Retrieve the appointments for the logged-in user.                          | Doctor/Patient |
| PATCH  | `/my/appointments/<id>/update-status/`      | Doctors update the status of an appointment.                              | Doctor         |
| DELETE | `/my/appointments/<id>/delete/`             | Patients delete their own appointments.                                    | Patient        |

**Note:**  
- When creating an appointment, the `patient` field is automatically set to the currently authenticated patient.
- Only doctors can update the status field.

---

### Patient Records (Managed under `/api/`)

Patient records include **Medical Records, Diagnoses,** and **Lab Results**.

#### Medical Records

| Method | Endpoint                              | Description                                                         | Access         |
| ------ | ------------------------------------- | ------------------------------------------------------------------- | -------------- |
| POST   | `/medical-records/create/`            | Create a new medical record (doctors only).                         | Doctor         |
| GET    | `/medical-records/`                   | List all medical records (doctors) or the record of the patient.      | Doctor/Patient |
| GET    | `/medical-records/<id>/detail/`        | Retrieve details of a specific medical record.                      | Doctor         |
| PUT    | `/medical-records/<id>/update/`        | Update an existing medical record (doctors only).                   | Doctor         |

#### Diagnoses

| Method | Endpoint                              | Description                                                         | Access         |
| ------ | ------------------------------------- | ------------------------------------------------------------------- | -------------- |
| POST   | `/diagnoses/create/`                  | Create a new diagnosis (doctors only).                              | Doctor         |
| GET    | `/diagnoses/`                        | List all diagnoses or those for the current patient.                | Doctor/Patient |
| GET    | `/diagnoses/<id>/detail/`             | Retrieve details of a diagnosis.                                    | Doctor/Patient |
| PUT    | `/diagnoses/<id>/update/`             | Update an existing diagnosis (doctors only).                        | Doctor         |

#### Lab Results

| Method | Endpoint                              | Description                                                         | Access         |
| ------ | ------------------------------------- | ------------------------------------------------------------------- | -------------- |
| POST   | `/lab-results/create/`                | Create new lab results (doctors only).                              | Doctor         |
| GET    | `/lab-results/`                       | List lab results (all for doctors, or own for patients).              | Doctor/Patient |
| GET    | `/lab-results/<id>/detail/`            | Retrieve a specific lab result.                                     | Doctor/Patient |
| PUT    | `/lab-results/<id>/update/`            | Update lab results (doctors only).                                  | Doctor         |

---

### Medications (Managed under `/api/`)

Medications are handled via a ViewSet.

| Method    | Endpoint             | Description                                         | Access                                |
| --------- | -------------------- | --------------------------------------------------- | ------------------------------------- |
| GET       | `/medications/`      | List all medications.                               | All (Read-only for patients/doctors)  |
| POST      | `/medications/`      | Create a new medication.                            | Pharmacist (or Admin)                 |
| GET       | `/medications/<id>/` | Retrieve details of a medication.                  | All                                   |
| PUT/PATCH | `/medications/<id>/` | Update a medication.                                | Pharmacist (or Admin)                 |
| DELETE    | `/medications/<id>/` | Delete a medication.                                | Pharmacist (or Admin)                 |

---

### Prescriptions (Managed under `/api/`)

Prescriptions link to medical records and medications. **Note:** Medications are associated via a reverse relationship (i.e., each Medication has a `prescription` ForeignKey).

| Method | Endpoint                    | Description                                                                 | Access                                                    |
| ------ | --------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------- |
| GET    | `/prescriptions/`           | List all prescriptions (filtered based on user role).                     | Doctors, Pharmacists, Patients (only own records)         |
| POST   | `/prescriptions/`           | Create a new prescription. **Requires at least one medication ID.**          | Doctors create; Pharmacists may update status later.      |
| GET    | `/prescriptions/<id>/`      | Retrieve details of a specific prescription, including medications.          | Accessible based on role                                  |
| PUT    | `/prescriptions/<id>/`      | Update a prescription (restrictions apply based on role).                    | Doctors and Pharmacists (with field restrictions)         |
| DELETE | `/prescriptions/<id>/`      | Delete a prescription.                                                       | Doctors (or Admin)                                        |

#### Prescription Details:
- **Input Field**: `medication_ids` – A write-only field to accept a list of medication IDs.
- **Output Field**: `medications` – A read-only field that displays detailed medication information.
- **Validation**: The prescription creation validates that the patient in the prescription matches the patient in the linked medical record.

---

## 6. Error Handling

The API returns standard HTTP status codes:

- **200 OK** – Successful GET, PUT, or DELETE operations.
- **201 Created** – Successful POST operations.
- **400 Bad Request** – Validation errors, missing fields (e.g., no medication IDs provided when required).
- **401 Unauthorized** – Authentication is missing or invalid.
- **403 Forbidden** – The user does not have permission to perform the action.
- **404 Not Found** – The requested resource does not exist.

**Example Error Response:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

or

```json
{
  "medication_ids": [
    "At least one medication is required."
  ]
}
```

---

## 7. Examples

### Example 1: User Registration

**Request:**

```http
POST /api/users/register/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "role": "Patient"
}
```

**Response:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "role": "Patient"
}
```

---

### Example 2: User Login

**Request:**

```http
POST /api/users/login/
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securePassword123"
}
```

**Response:**

```json
{
  "token": "9c5e54f7e346f3b..."
}
```

---

### Example 3: Get Current User Profile

**Request:**

```http
GET /api/users/me/
Authorization: Token 9c5e54f7e346f3b...
```

**Response:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "role": "Patient"
}
```

---

### Example 4: Creating an Appointment

**Request:**

```http
POST /api/appointments/create/
Content-Type: application/json
Authorization: Token <patient_token>

{
  "date_time": "2025-04-10T10:00:00Z"
}
```

**Response:**

```json
{
  "id": 4,
  "date_time": "2025-04-10T10:00:00Z",
  "status": "Pending",
  "doctor": null,
  "patient": {
    "user": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "role": "Patient"
    }
  }
}
```

---

### Example 5: Listing Appointments

**Request:**

```http
GET /api/my/appointments/
Authorization: Token <user_token>
```

**Response (for a patient):**

```json
[
  {
    "id": 4,
    "date_time": "2025-04-10T10:00:00Z",
    "status": "Pending",
    "doctor": null,
    "patient": {
      "user": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "role": "Patient"
      }
    }
  }
]
```

---

### Example 6: Updating Appointment Status (Doctor)

**Request:**

```http
PATCH /api/my/appointments/3/update-status/
Content-Type: application/json
Authorization: Token <doctor_token>

{
  "status": "Approved"
}
```

**Response:**

```json
{
  "id": 3,
  "date_time": "2025-04-06T09:00:00Z",
  "status": "Approved",
  "doctor": {
    "user": {
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice@example.com",
      "role": "Doctor"
    },
    "license_number": "DOC12345",
    "specialization": "Cardiology",
    "years_of_experience": 10,
    "certifications": "Board Certified"
  },
  "patient": {
    "user": {
      "first_name": "Bob",
      "last_name": "Jones",
      "email": "bob@example.com",
      "role": "Patient"
    },
    "date_of_birth": "1990-01-01",
    "sex": "Male",
    "address": "123 Main St",
    "phone_number": "5551234567",
    "full_name": "Bob Jones",
    "age": 35
  }
}
```

---

### Example 7: Creating a Medical Record

**Request:**

```http
POST /api/medical-records/create/
Content-Type: application/json
Authorization: Token <doctor_token>

{
  "patient": 3,
  "surgeries": "Appendectomy in 2010",
  "allergies": "Penicillin",
  "family_history": "Diabetes",
  "social_history": "Non-smoker"
}
```

**Response:**

```json
{
  "patient": 3,
  "surgeries": "Appendectomy in 2010",
  "allergies": "Penicillin",
  "family_history": "Diabetes",
  "social_history": "Non-smoker",
  "date_created": "2025-04-05T13:00:00Z",
  "last_updated": "2025-04-05T13:00:00Z",
  "diagnoses": [],
  "lab_results": [],
  "prescriptions": []
}
```

---

### Example 8: Creating a Diagnosis

**Request:**

```http
POST /api/diagnoses/create/
Content-Type: application/json
Authorization: Token <doctor_token>

{
  "patient": 3,
  "medical_record": 5,
  "condition": "Hypertension",
  "added_notes": "Blood pressure consistently high."
}
```

**Response:**

```json
{
  "id": 2,
  "patient": 3,
  "medical_record": 5,
  "condition": "Hypertension",
  "added_notes": "Blood pressure consistently high.",
  "date_created": "2025-04-05T14:00:00Z",
  "last_updated": "2025-04-05T14:00:00Z"
}
```

---

### Example 9: Creating Lab Results

**Request:**

```http
POST /api/lab-results/create/
Content-Type: multipart/form-data
Authorization: Token <doctor_token>

--boundary
Content-Disposition: form-data; name="patient"

3
--boundary
Content-Disposition: form-data; name="medical_record"

5
--boundary
Content-Disposition: form-data; name="xray"; filename="xray.jpg"
Content-Type: image/jpeg

<binary data>
--boundary--
```

**Response:**

```json
{
  "id": 4,
  "patient": 3,
  "medical_record": 5,
  "xray": "/media/xrays/xray.jpg",
  "vitalsigns": null,
  "blood_test_results": null,
  "urinalysis_results": null,
  "date_created": "2025-04-05",
  "notes": null
}
```

---

### Example 10: Creating a Prescription

**Request:**

```http
POST /api/prescriptions/
Content-Type: application/json
Authorization: Token <your_token_here>

{
  "doctor": 2,
  "medical_record": 5,
  "patient": 3,
  "frequency": "Twice a day",
  "quantity": 10,
  "duration": 7,
  "instructions": "Take after meals",
  "status": "Pending",
  "medication_ids": [12, 15]
}
```

**Response:**

```json
{
  "id": 7,
  "doctor": 2,
  "medical_record": 5,
  "patient": 3,
  "frequency": "Twice a day",
  "quantity": 10,
  "duration": 7,
  "instructions": "Take after meals",
  "prescribed_at": "2025-04-05T14:30:00Z",
  "status": "Pending",
  "medications": [
    {
      "id": 12,
      "generic_name": "Paracetamol",
      "brand_name": "Panadol",
      "dosage_form": "Tablet",
      "strength": "500.00",
      "unit": "mg"
    },
    {
      "id": 15,
      "generic_name": "Amoxicillin",
      "brand_name": "Amoxil",
      "dosage_form": "Capsule",
      "strength": "250.00",
      "unit": "mg"
    }
  ]
}
```

---

### Example 11: Updating a Prescription (Pharmacist Updating Status)

**Request:**

```http
PUT /api/prescriptions/7/
Content-Type: application/json
Authorization: Token <pharmacist_token>

{
  "status": "Dispensed"
}
```

**Response:**

```json
{
  "id": 7,
  "doctor": 2,
  "medical_record": 5,
  "patient": 3,
  "frequency": "Twice a day",
  "quantity": 10,
  "duration": 7,
  "instructions": "Take after meals",
  "prescribed_at": "2025-04-05T14:30:00Z",
  "status": "Dispensed",
  "medications": [
    {
      "id": 12,
      "generic_name": "Paracetamol",
      "brand_name": "Panadol",
      "dosage_form": "Tablet",
      "strength": "500.00",
      "unit": "mg"
    },
    {
      "id": 15,
      "generic_name": "Amoxicillin",
      "brand_name": "Amoxil",
      "dosage_form": "Capsule",
      "strength": "250.00",
      "unit": "mg"
    }
  ]
}
```

---

## 8. Notes

- **Authorization**: Except for `/register/` and `/login/`, every endpoint requires a valid token.
- **Role-based Access**: Endpoints enforce role-based permissions (e.g., only patients can create appointments, only doctors can create diagnoses).
- **Data Consistency**: When creating prescriptions, the API validates that the patient provided matches the patient in the associated medical record.
- **File Uploads**: Lab results support file uploads (e.g., for X-rays) under `/lab-results/create/` – ensure your requests are sent as multipart/form-data if uploading files.
- **Pagination**: List endpoints may return paginated responses. Look for `next`, `previous`, and `results` keys in the JSON response.
- **Testing**: Use tools like Postman to interact with these endpoints and verify the responses.

---

_End of Documentation_
```