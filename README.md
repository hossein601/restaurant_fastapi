
## **Restaurant Manager System**


## **Installation**

First should install requirement.txt.Then create new database and add your database. Create your own database.

### From source
```bash
git clone https://github.com/hossein601/restaurant_fastapi.git
cd restaurant
pip install -r requirements.txt
```
## Usage
First install database and create new database with your specific username and password
```bash
sudo -u postgres psql
sudo -u postgres createdb <dbname>
```
Create '.env' file write 
```bash
DATABASE_URL=postgresql+psycopg2://postgres:<password>@localhost/<dbname>
```
## Executing
#### You can run one of the following commands for execution:

```bash
$ uvicorn main:app

```
## Swagger
#### You can run one of the following commands for accessing apis:
```bash
http://127.0.0.1<port_number>/docs
```
## Testing

``` bash
$ pytest
Launching pytest with arguments /home/hossien/PycharmProjects/restaurant_fastapi/test --no-header --no-summary -q in /home/hossien/PycharmProjects/restaurant_fastapi/test

============================= test session starts ==============================
collecting ... collected 69 items

test_basket.py::test_create_basket PASSED                                [  1%]
test_basket.py::test_create_basket_basket_item_exist PASSED              [  2%]
test_basket.py::test_create_basket_not_exist_basket PASSED               [  4%]
test_basket.py::test_create_basket_not_item PASSED                       [  5%]
test_basket.py::test_add_basket PASSED                                   [  7%]
test_basket.py::test_add_basket_not_exist_basket PASSED                  [  8%]
test_basket.py::test_remove_from_basket PASSED                           [ 10%]
test_basket.py::test_remove_from_basket_not_exist_bakset PASSED          [ 11%]
test_basket.py::test_remove_from_basket_not_exist_item PASSED            [ 13%]
test_basket.py::test_get_basket PASSED                                   [ 14%]
test_basket.py::test_delete_item_from_basket PASSED                      [ 15%]
test_basket.py::test_delete_item_from_basket_not_basket_item PASSED      [ 17%]
test_basket.py::test_delete_all_items_from_basket PASSED                 [ 18%]
test_basket.py::test_delete_basket_not_found PASSED                      [ 20%]
test_basket.py::test_item_not_found_in_basket PASSED                     [ 21%]
test_category.py::test_create_category PASSED                            [ 23%]
test_category.py::test_create_category_exist PASSED                      [ 24%]
test_category.py::test_update_category PASSED                            [ 26%]
test_category.py::test_update_category_not_exsiting PASSED               [ 27%]
test_category.py::test_delete_category PASSED                            [ 28%]
test_category.py::test_delete_category_not_exist PASSED                  [ 30%]
test_category.py::test_search_categories_by_name PASSED                  [ 31%]
test_category.py::test_search_categories_descriptions PASSED             [ 33%]
test_category.py::test_search_categories_get_all PASSED                  [ 34%]
test_category_item.py::test_assign_item_to_category PASSED               [ 36%]
test_category_item.py::test_assign_item_to_category_not_found_item PASSED [ 37%]
test_category_item.py::test_assign_item_to_category_exist_category_item PASSED [ 39%]
test_category_item.py::test_assign_item_to_category_not_found_cateory PASSED [ 40%]
test_category_item.py::test_update_item_categories_not_exist_item PASSED [ 42%]
test_category_item.py::test_update_item_categories_not_found_item PASSED [ 43%]
test_category_item.py::test_update_item_categories_not_found_category PASSED [ 44%]
test_category_item.py::test_update_item_categories_invalid_id PASSED     [ 46%]
test_category_item.py::test_get_category_items PASSED                    [ 47%]
test_category_item.py::test_get_category_items__not_exist_category_items PASSED [ 49%]
test_category_item.py::test_delete_category_items PASSED                 [ 50%]
test_items.py::test_create_item PASSED                                   [ 52%]
test_items.py::test_update_item PASSED                                   [ 53%]
test_items.py::test_update_item_not_exsist PASSED                        [ 55%]
test_items.py::test_delete_item PASSED                                   [ 56%]
test_items.py::test_filter_item_id PASSED                                [ 57%]
test_items.py::test_filter_item_price PASSED                             [ 59%]
test_items.py::test_filter_item_description PASSED                       [ 60%]
test_items.py::test_filter_item_category_id PASSED                       [ 62%]
test_items.py::test_filter_item_category_name PASSED                     [ 63%]
test_items.py::test_filter_item_category_no_filter PASSED                [ 65%]
test_order.py::test_create_order_basket_empty PASSED                     [ 66%]
test_order.py::test_create_order_missing_address PASSED                  [ 68%]
test_order.py::test_create_order PASSED                                  [ 69%]
test_order.py::test_create_order_not_enough__stock PASSED                [ 71%]
test_order.py::test_get_orders PASSED                                    [ 72%]
test_staff.py::test_create_staff PASSED                                  [ 73%]
test_staff.py::test_update_staff PASSED                                  [ 75%]
test_staff.py::test_update_not_exsisting_staff PASSED                    [ 76%]
test_staff.py::test_delete_staff PASSED                                  [ 78%]
test_staff.py::test_delete_staff_not_staff PASSED                        [ 79%]
test_user.py::test_get_users_profile PASSED                              [ 81%]
test_user.py::test_increase_wallet PASSED                                [ 82%]
test_user.py::test_decrease_wallet PASSED                                [ 84%]
test_user.py::test_decrease_wallet_get_error PASSED                      [ 85%]
test_user.py::test_signin_with_valid_data PASSED                         [ 86%]
test_user.py::test_login_with_valid_data PASSED                          [ 88%]
test_user.py::test_login_with_invalid_data PASSED                        [ 89%]
test_user.py::test_signin_existing_phone_number PASSED                   [ 91%]
test_user.py::test_signin_with_invalid_password PASSED                   [ 92%]
test_user.py::test_signin_with_invalid_phone_number PASSED               [ 94%]
test_user.py::test_login_with_invalid_phone_number PASSED                [ 95%]
test_user.py::test_delete_user PASSED                                    [ 97%]
test_user.py::test_validation_type_name PASSED                           [ 98%]
test_user.py::test_validation_type_address PASSED                        [100%]

====================== 69 passed, 486 warnings in 23.12s =======================
Wrote XML report to /home/hossien/.cache/JetBrains/PyCharm2024.2/coverage/restaurant_fastapi$.xml

```

## Accessing variables

```

Settings.DATABASE_URL
Settings.algorithm
Settings.access_token_expire_minutes
Settings["db"]["uri"]

```