python3.6 -m pip install PyGithub

export COMMIT_MESSAGE=$(git reflog -1 | sed 's/^.*: //')
python3.6 teamcity/verify_release_tags.py
    
python3.6 -m pip install twine;
python3.6 setup.py sdist;
twine upload dist/*;