python3.6 -m pip install -r requirements.txt
python3.6 -m pip install coverage

coverage run -m unittest
coverage report -m