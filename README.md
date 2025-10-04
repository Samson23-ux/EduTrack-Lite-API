# 🛠 Project Description

#### This system allows users to register for courses, track course completion, and manage course information. It supports CRUD operations and enforces simple validation and relationships between the entities.

## Functionalities

* Register for course
* Track Course Completion
* Get registered courses
* Get users enrolled for a course

![Static Badge](https://img.shields.io/badge/FastAPI-0.116.1-green?color=%23006400)
![Static Badge](https://img.shields.io/badge/Python-3.13-green?color=%23006400)

# 🧾 Steps to run and test endpoints

## 1. Clone repo

```shell
git clone https://github.com/Samson23-ux/EduTrack-Lite-API.git
```

## 2. Create enviroment

```shell
python -m venv venv
```

## 3. Activate enviroment

```shell
venv\Scripts\activate or source venv/bin/activate (for apple)
```

## 4. Install Dependencies

```shell
pip install -r requirements.txt
```

## 5. Run Server

```shell
uvicorn app.main:main --reload
```

## 6. Test Endpoints

```shell
run http://localhost:8000/docs on browser
```

