python3.6 -m pip install PyGithub

echo "-- Creating git release draft --"
export COMMIT_MESSAGE=$(git reflog -1 | sed 's/^.*: //')
python3.6 teamcity/verify_release_tags.py
  
python3.6 -m pip install twine;

echo "-- Packaging module --"
python3.6 setup.py sdist;
echo "-- Uploading package --"
twine upload dist/*;