# Test task
This is an application for parsing movies on http://kinogo-net.org. It includes a parser and django app to display information from the database. Images are saved in separate folders. An absolute path is used to access images. To run the script requires an argument of the number of pages

# Instructions
- Install Python 3.6+ and pip
- Install required libraries:
```$xslt
pip install -r requirements.txt
```
- Make migrate:
```$xslt
python manage.py makemigrations kinogo
python manage.py migrate
```
- Start parser:
```$xslt
python kinogo_parser.py 30
```
- Start server:
```$xslt
python manage.py runserver
```

