# Todos Service API

### Настройка окружения
#### В .*shrc (.bashrc; .zshrc) файле укажите:
`export MYSQL_USER=`<br>
`export MYSQL_PASSWORD=`<br>
`export MYSQL_HOST=`<br>
`export MYSQL_PORT=`<br>
`export MYSQL_DB=`<br>
`export API_SERVER_HOST=`<br>
`export API_SERVER_PORT=`

##### Как пример:
`export MYSQL_USER=exampleuser`<br>
`export MYSQL_PASSWORD=examplepass`<br>
`export MYSQL_HOST=localhost`<br>
`export MYSQL_PORT=3306`<br>
`export MYSQL_DB=exampledb`<br>
`export API_SERVER_HOST=localhost`<br>
`export API_SERVER_PORT=8080`

##### Установка как сервис:
`./scripts/install_service.sh`

##### Запуск без установки:
`./scripts/run.sh`
