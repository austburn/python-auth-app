default: build launch

build:
	docker build -f ./app.docker --tag python-auth-app .

launch:
	./launch.sh
