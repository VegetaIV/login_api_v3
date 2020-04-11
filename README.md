# login_api

#1 Add api to postman from 

https://www.getpostman.com/collections/4d29af1b8d52cc9fbfd1

#2 Terminal1: Run redis-server

#3 Terminal2: Run server.py

#4 Test api trong postman

Bước 1. Api create_user: thay đổi username, email, password trong phần body rồi Send để tạo user mới

Bước 2. Api login: thay username và password trong body bằng thông tin vừa tạo ở Bước 1 rồi Send để đăng nhập, trong thông tin trả về có chứa trường id

Bước 3. Api cache_user: thay username, email và id trong body bằng thông tin đã đăng ký và id trả về ở Bước 2 rồi Send

Bước 4. Api user: thay id trong url bằng id trả về ở Bước 2 rồi Send
