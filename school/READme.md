SIGNING UP 
curl localhost:8000/user/sign_up/ -H "Content-Type: application/json" -d '{"username": "bon", "password": "firefox123"}'

LOGIN USER
curl localhost:8000/user/login/ -H "Content-Type: application/json" -d '{"username": "bon", "password": "firefox123"}'

CREATE A SCHOOL
curl localhost:8000/user/create-school/ -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek" -d '{"name": "Busia Township"}'


CREATE A TERM FEE FOR ALL STUDENTS
curl localhost:8000/finance/create-term-fees/ -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek" -d '{"schoolTerm": "Term 3 2024", "fees": "12344", "startDate": "2024-12-02", "endDate": "2025-03-05"}'


REGISTER A PARENT
curl localhost:8000/user/register-parent/ -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek" -d '{"fullName": "Bion Solo", "phoneNumber": "0701036054"
, "email": "bionsol25@gmail", "related": "father"}'


CREATING PAYMENT
curl localhost:8000/finance/make-payment/ -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek" -d '{"studentId": "8f0f9726-6271-47bb-b4ec-0038777c2f3f", "amount": "50", "paymentMethod": "mpesa"}'


ADMIT A STUDENT
curl localhost:8000/user/admit-student/ -H "Content
-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -
H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek" -d '{"parentId": "8b633b36-d178-4cec-9a75-2c43bb70686e", "fullName": "bion nova", "grade": "3"}'

VIEW SCHOOL FEE PAID OF THE LATEST TERM
curl localhost:8000/finance/view-feepaid/?studentId=8f0f9726-6271-47bb-b4ec-0038777c2f3f -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek"

VIEW ALL SCHOOL FEE PAID IN ALL TERMS
curl localhost:8000/finance/view-all-feepaid/?studentId=8f0f9726-6271-47bb-b4ec-0038777c2f3f -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek"

VIEW ALL PAYMENT FOR A SPECIFIC STUDENT FOR THE LAST 3 MONTHS
curl localhost:8000/finance/view-all-payments/?studentId=8f0f9726-6271-47bb-b4ec-0038777c2f3f -H "Content-Type: application/json" -H "X-CSRFToken: 9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp" -H "Cookie: csrftoken=9o36Mp7i9CXFW4PPFjllyJieyEiCqJqp; sessionid=lulcbv73bfphwb2rex622ftf44ltr9ek"