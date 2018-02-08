pip install PyGithub

export COMMIT_MESSAGE=$(git reflog -1 | sed 's/^.*: //')
export TBS_CLI_VERSION=0.1.1
python teamcity/verify_release_tags.py
    
pip install twine;
python setup.py sdist;
twine upload dist/*;