# Task 3

Модуль для подсчёта одновременного пребывания ученика и учителя на уроке по интервалам в формате Unix Timestamp.

## API
### Формат
**Endpoint:** '/appearance'

Ожидается POST-запрос, содержащий в теле JSON-данные в формате:
```js
{
  "lesson": [...],
  "pupil": [...],
  "tutor": [...]
}

```
В случае успеха возвращает JSON:
```js
{"appearance": результат_в_секундах}
```
HTTP статус: 200

Если входные данные некорректные:
```js
{"error": "Input data is invalid."}
```
HTTP статус: 422

### Запуск в Docker

```shell
$ docker build -t presence_calculator .
$ docker run --publish 5000:5000 presence_calculator
```

### Пирмер

#### Запрос
```bash
curl --location --request POST 'localhost:5000/appearance' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lesson": [
        1594663200,
        1594666800
    ],
    "pupil": [
        1594663340,
        1594663389,
        1594663390,
        1594663395,
        1594663396,
        1594666472
    ],
    "tutor": [
        1594663290,
        1594663430,
        1594663443,
        1594666473
    ]
}'
```

#### Ответ
```js
{"appearance":3117}
```
