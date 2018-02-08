python3.6 -m pip install -r requirements.txt
python3.6 -m pip install coverage

python3.6 -m coverage run -m unittest
python3.6 -m coverage report -m