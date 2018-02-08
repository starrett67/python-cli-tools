cat > ~/.pypirc << EOL
[distutils]
index-servers =
  pypi

[pypi]
username=${PYPI_USER}
password=${PYPI_PASSWORD}
EOL