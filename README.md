
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
```bash
auth/v1/sigin
Request body:requierd
{
  "phone_number": "string",
  "password": "string"
}
response
access token

```
```bash
>python main.py order -h

positional arguments:
  {list,add,update,delete}
                        Order commands
    list                List all orders
    add                 Create a new order
    update              Update an existing order
    delete              Delete an order

options:
  -h, --help            show this help message and exit

```
```bash
>python main.py reserve -h

positional arguments:
  {list,add,update,delete}
                        Reserve commands
    list                List all reservations
    add                 Create a new reservation
    update              Update an existing reservation
    delete              Delete a reservation

options:
  -h, --help            show this help message and exit
      
```
```bash
>python main.py staff -h

positional arguments:
  {list,add,update,delete,filter}
                        Staff commands
    list                List all staff members
    add                 Add a new staff member
    update              Update an existing staff member
    delete              Delete a staff member
    filter              staff for each order

options:
  -h, --help            show this help message and exit

```

