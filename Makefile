run:
	docker run --publish 5000:5000 --env-file apiInfo.env chris-satterfield-ivr
build:
	docker build -t chris-satterfield-ivr .