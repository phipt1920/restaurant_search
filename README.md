#step dể chạy
##1: docker-compose up --build app
//Xoá index
##2:  curl -X DELETE "http://localhost:9200/restaurants" 
//Tạo index load file
##3: docker exec -it restaurant_search_app python load_data.py
##4:curl "http://localhost:5000/nearby?query=%E3%81%99%E3%81%97&lat=35.6762&lon=139.6503"
//or truy cập trình duyệt
