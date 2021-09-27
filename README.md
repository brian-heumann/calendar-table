# calendar-table
A calendar table which makes the work with dates, holidays, weekends etc. easier.

## Virtual environment 
Use a virtual environment to manage project speoific python modules.

Create the virtual environment:
```bash
python3 -m venv .venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Install the required dependent modules:
````bash
pip install -r requirements.txt
````

After adding or updating the dependent modules, freeze the current dependent modules:
```bash
pip freeze > requirements.txt
```
