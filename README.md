
## **Restaurant Manager System**



## **Installation**

First should install requirement.txt. Then create new database and add yoour database. create your own database.


```bash
pip install psycopg2-binary
pip install SQLAlchemy
pip install python-dotenv
pip install fastapi
pip install alembic
pip install JWT
pip install bcrypt
```
### from source
```bash
git clone https://github.com/hossein601/restaurant_fastapi.git
cd restaurant
pip install -e
```
## Usage
First install database and create new database with your specific username and password,add it to file 'base_model'
```bash
sudo -u postgres psql
sudo -u postgres createdb <dbname>
```
Create '.env' file wirte 
```bash
DATABASE_URL=postgresql+psycopg2://postgres:<password>@localhost/<dbname>
```
## CLI
```bash
>uvicorn main:app --reload

usage:http://127.0.0.1:8000/docs
options:
auth,
user,
staff,
item,
category,
category_item,
basket,
order

```
## auth
```bash
auth
POST/v1/sigin
Request body:requierd
{
  "phone_number": "string",
  "password": "string"
}
response
access token

```
```bash
auth
POST/v1/login
Request body:requierd
{
  "phone_number": "string",
  "password": "string"
}
response
access token
```
## user
```bash
user
GET/v1/users
response
{
  "name": "string",
  "address": "string",
  "phone_number": "string",
  "wallet": 0
}
```
```bash
user
PUT/v1/users
rquest
{
  "name": "string",
  "address": "string"
}
response
{
  "name": "string",
  "address": "string",
  "phone_number": "string",
  "wallet": 0
}
```


