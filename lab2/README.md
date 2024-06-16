### Лабораторная работа №2

Скрипт `mtu.py` позволяет найти значение `MTU` до заданного хоста.

Пример запуска:

```
python3 mtu.py --host=ya.ru
```

Или, используя докер:

```
docker build -t mtu_script . 
docker run -it --rm mtu_script --host=ya.ru
```
