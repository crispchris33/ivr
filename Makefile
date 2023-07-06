run:
	docker run --publish 5000:5000 --env-file apiInfo.env name-of-ivr
build:
	docker build -t name-of-ivr .
