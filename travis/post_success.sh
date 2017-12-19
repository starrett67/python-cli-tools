pip install PyGithub
python travis/verify_release_tags.py
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    pip install twine;
    python setup.py sdist;
    twine upload dist/*;
fi