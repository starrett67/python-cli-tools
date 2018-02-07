pip install PyGithub
python teamcity/verify_release_tags.py
    
pip install twine;
python setup.py sdist;
twine upload dist/*;