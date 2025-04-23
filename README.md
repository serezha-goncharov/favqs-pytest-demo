# favqs-pytest-demo
This repository represents basic API tests built with pytest and Allure of FavQs project that allows you to collect, discover, and share your favorite quotes.

https://favqs.com/api


Disclaimer: The tests do not cover all the endpoints and all test-cases.
It is designed to develop and improve automation testing skills with Pytest and Allure


Install
```commandline
pip install
```

Run tests
```commandline
pytest tests/ --base-url "https://favqs.com/api"
```

Generate HTML report
```commandline
allure generate reports/json -o reports/html --clean
```

Open HTML report
```commandline
allure open reports/html
```