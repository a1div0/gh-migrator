# gh-migrator

Утилита для сохранения Issue со всеми вложениями и комментариями в файлы
на диске.

Использовать так.
1. Нужно создать Github API token с правами на чтение из репозиториев.
   Прописать его в переменную окружения `GITHUB_API_TOKEN`.
2. Нужно из браузера, из кукисов достать user session. Прописать значение в
   `GITHUB_USER_SESSION`.

Далее вызов:
```shell
python3 main.py <папка_куда_складывать> <repo_owner> <repo_name>
```

Пример вызова:
```shell
GITHUB_API_TOKEN=too GITHUB_USER_SESSION=foo \
    python3 main.py database/tarantooldb/ tarantool tarantooldb
```
