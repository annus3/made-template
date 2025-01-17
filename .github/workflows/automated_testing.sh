name: Automated_Testing_CI
run-name: ${{ github.actor }} is testing out GitHub Actions 🚀

on:   
  push:
    branches:
    - main

env:
  KAGGLE_USERNAME: $KAGGLE_USERNAME
  KAGGLE_KEY: $KAGGLE_KEY

jobs:
  Automated_Testing_CI:
    runs-on: ubuntu-latest
    steps:

    - name: Checkout
      uses: actions/checkout@v3


    - name: Set up Node
      uses: actions/setup-node@v3
      with:
        node-version: 'lts/*'
      
    # Install python
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
        
    # Install dependencies
    - name: Install dependecies
      run: |
        python -m pip install --upgrade pip
        pip install pandas
        pip install requests
        pip install sqlalchemy
        
    # Run Code Format check

    - name: Set execute permissions
      run: 
        chmod +x ./project/tests.sh

    # Run tests 
    - name: Run Shell Script and tests
      run: |
        ./project/tests.sh