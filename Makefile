install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py

lint:
	# pylint --disable=R,C --ignore-patterns=__*__.py --disable=W0511,E1101 *.py

test:
	# python -m pytest -vv --cov=Code_10 --cov=main test_*.py
	python -m pytest -vv --cov=main main/tests/test_*.py

build:
	docker build -t cloud_bodes .

run:
	docker run -it --rm -p 8080:8080 cloud_bodes
	# docker run -dp 8080:8080 cloud_bodes
	# docker run --rm -i hadolint/hadolint < Dockerfile


run-local:
	streamlit app run app.py

run-local-docker: build run 

deploy-aws:
#   Placeholder 
	ls 
# 	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 667719398048.dkr.ecr.us-east-1.amazonaws.com	
# 	docker build -t awscloudbodes .
# 	docker tag awscloudbodes:latest 667719398048.dkr.ecr.us-east-1.amazonaws.com/awscloudbodes:latest
# 	docker push 667719398048.dkr.ecr.us-east-1.amazonaws.com/awscloudbodes:latest

all: install format lint deploy # test 
