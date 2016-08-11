default: build run

build:
	docker build -f ./app.docker --tag python-auth-app .

run:
	docker run -it python-auth-app
