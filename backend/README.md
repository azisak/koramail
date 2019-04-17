# Backend Repo


## Installation
Install the requirements
```
pip install -r requirements.txt
```

## Running Backend
Export flask variable
```
export FLASK_APP="main.py"
```
Running flask
```
flask run
```


## API Endpoints

### 1. /api/sign
**Available method**: POST

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| -------------------- |
| message     | ***String*** | Message to be signed |

**Response**: JSON object 

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| message     | ***String*** | Original message     |
| signature   | ***String*** | Signature of message |

### 2. /api/verify
**Available method**: POST

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| -------------------- |
| message     | ***String*** | Message to be verified |
| signature     | ***String*** | Signature to be verified |

**Response**: JSON object 

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| verified     | ***Boolean*** | Condition whether the message signed or not     |
| error_msg   | ***String*** | (optional) Any error message occured during signing |
