python3.6 -m pip install -r requirements.txt
python3.6 -m pip install coverage
python3.6 -m pip install teamcity-messages

python3.6 -m coverage run -m teamcity.unittestpy
python3.6 -m coverage report -m