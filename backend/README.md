# Backend Repo


## Installation
Install the requirements
```
pip install -r requirements.txt
```

## Configurations
All configs located in config.json, feel free to change

## Running Backend Server
Export flask variable
```
export FLASK_APP="main.py"
```
Running flask. By default it will run on port 5000
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
| verified     | ***Boolean*** | Condition whether the message verified or not     |
| error_msg   | ***String*** | (optional) Any error message occured during verifying |

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

### 3. /api/encrypt
**Available method**: POST

**Request payload**: Form

| Attribute   | Type         | Description             |
| ----------- |:------------:| ------------------------|
| message     | ***String*** | Message to be encrypted |
| key         | ***String*** | Key for encryption      |

**Response**: JSON object 

| Attribute     | Type         | Description           |
| ------------- |:------------:| ----------------------|
| encrypted     | ***String*** | Encrypted message     |

### 4. /api/decrypt
**Available method**: POST

**Request payload**: Form

| Attribute   | Type         | Description             |
| ----------- |:------------:| ------------------------|
| message     | ***String*** | Message to be decrypted |
| key         | ***String*** | Key for decryption      |

**Response**: JSON object 

| Attribute     | Type         | Description           |
| ------------- |:------------:| ----------------------|
| decrypted     | ***String*** | Decrypted message     |

### 5. /api/inbox/```<email>```
*Example*: ```/api/inbox/my_mail@gmail.com```

**Available method**: GET, POST, DELETE

### GET METHOD
Retrieve inboxes of an ```email```

**Response**: JSON List of object 

Where each object defined as below

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| id     | ***Integer*** | Identifier of a mail    |
| subject   | ***String*** | Subject of a mail |
| sender_mail   | ***String*** | Sender email |
| receiver_mail   | ***String*** | Receiver email (in this case equals to ```email```) |
| content   | ***String*** | Content of a mail |

### POST METHOD
Insert new inbox mail, with receiver = ```email```

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| subject   | ***String*** | Subject of a mail |
| sender_mail   | ***String*** | Sender email |
| content   | ***String*** | Content of a mail |

**Response**: String, message indicating a mail was inserted successfully to the database

### DELETE METHOD
Delete a mail with specific Identifier provided

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| mail_id   | ***Integer*** | ID of a mail to be deleted |

**Response**: String, message indicating a mail was deleted successfully from the database

### 6. /api/sent_mail/```<email>```
*Example*: ```/api/sent_mail/my_mail@gmail.com```

**Available method**: GET, POST, DELETE

### GET METHOD
Retrieve sent mails of an ```email```

**Response**: JSON List of object 

Where each object defined as below

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| id     | ***Integer*** | Identifier of a mail    |
| subject   | ***String*** | Subject of a mail |
| sender_mail   | ***String*** | Sender email (in this case equals to ```email```) |
| receiver_mail   | ***String*** | Receiver email  |
| content   | ***String*** | Content of a mail |

### POST METHOD
Insert new sent mail, with receiver = ```email```

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| subject   | ***String*** | Subject of a mail |
| receiver_mail   | ***String*** | Receiver email |
| content   | ***String*** | Content of a mail |

**Response**: String, message indicating a mail was inserted successfully to the database

### DELETE METHOD
Delete a mail with specific Identifier provided

**Request payload**: Form

| Attribute   | Type         | Description          |
| ----------- |:------------:| ---------------------|
| mail_id   | ***Integer*** | ID of a mail to be deleted |

**Response**: String, message indicating a mail was deleted successfully from the database