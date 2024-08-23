SHELL := /bin/bash

migrate-factory-repos:
	python3 main.py database tarantool/tarantooldb
	python3 main.py database tarantool/k6-tarantool
	python3 main.py database tarantool/delivery
	python3 main.py database tarantool/crud
	python3 main.py database tarantool/crud-ee
	python3 main.py database tarantool/expirationd
	python3 main.py database tarantool/expirationd-ee
	python3 main.py database tarantool/migrations
	python3 main.py database tarantool/migrations-ee
	python3 main.py database tarantool/tt
	python3 main.py database tarantool/tt-ee
	python3 main.py database tarantool/dictionary
	python3 main.py database tarantool/halykbank
	python3 main.py database tarantool/spimex-server
	python3 main.py database tarantool/megafon-cdi
