# CSV Processor

Обработчик CSV-файлов с поддержкой фильтрации, агрегации и сортировки данных.

## Возможности

- Фильтрация данных с операторами `=`, `>`, `<`
- Агрегация данных (avg, min, max)
- Сортировка данных по колонке (asc/desc)
- Красивый вывод в виде таблицы

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/ninja152play/TestworkCSV.git
cd TestworkCSV
```
2. Установите зависимости
```
pip install -r requirements.txt
```
# Использование
```
python csv_processor.py --file <путь_к_csv> [опции]
```
Опции:
Опция	    Описание	                    Пример

--file	    Путь к CSV файлу (обязательный)	--file data.csv

--where	    Условие фильтрации	            --where "price>1000"

--aggregate	Агрегация данных	            --aggregate "avg=price"

--orderby   Сортировка данных	            --orderby "price=desc"

# Требования

Python 3.7+

Зависимости:

tabulate (для красивого вывода таблиц)

pytest (для тестов)

# Запуск тестов

```
pytest .
```

# Формат CSV файла
Файл должен содержать первую строку с заголовками (именами колонок). Пример:

name,brand,price,rating

iphone,apple,999,4.9

galaxy,samsung,1199,4.8

# Особенности реализации

Для числовых сравнений автоматически конвертирует строки в числа

Поддерживает сравнение строк (лексикографическое)

Выводит понятные сообщения об ошибках

Код покрыт тестами и имеет аннотации типов

# Примеры запуска!
![Снимок экрана_20250709_161525.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_20250709_161525.png)

![Снимок экрана_20250709_161807.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_20250709_161807.png)