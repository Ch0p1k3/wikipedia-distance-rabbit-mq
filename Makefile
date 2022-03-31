client:
	PYTHONPATH=. python3.9 src/client

install_python3.9:
	apt-get update
	apt-get install -y python3.9 python3.9-dev python-dev

requirements:
	python3.9 -m pip install .
