## Run project
#### `npm i`
Tải node_module
#### `npm start`
Chạy localhost frontend

#### `python -m rasa run actions`
Chạy endpoint cho file actions
#### `python -m rasa shell`
Test bot bằng cửa sổ dòng lệnh
#### `python -m rasa train`
Train bot
#### `python -m rasa run --enable-api --cors "*"`
Chạy api 

## Weather api: https://openweathermap.org/
#### `api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}`
Lấy thông tin dự báo thời tiết theo vĩ độ và kinh độ trong vòng 5 ngày
#### `api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}`
Lấy thông tin kinh độ và vĩ độ của thành phố hoặc quốc gia
#### `http://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}`
Lấy thông tin thời tiết hiện tại của 1 thành phố bất kì


