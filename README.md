# Content
* [Description](#description)
  * [Use Case](#use-case)
  * [Apps inside](#apps-inside)
* [Download and run](#download-and-run)

# Description
**Charity - Donation django web app**
This application was created solely as a way to extend my programming abilities.
Static files, templates and the idea for this application was delivered by Coderslab.

## Use Case
**The idea behind the app:**
**The purpose of this application is to connect people that wants to donate some items with Institutions that can help with passing them to those in need.
A registered user can donate items, selecting the Category, recipient, quantity, contact data, pickup time and place etc.

## Apps inside
* **accounts**
  * Changes functionality of the default Django User Authentication app

* **donations**
  * Handles all donation functions: adding, archiving, viewing

# Download and run
**To run this project on Your computer follow these steps**
* clone this repository
* create virtualenvironment (run `virtualenv venv`)
* activate virtualenvironment (run `source venv/bin/activate`)
* install requirements (run `pip install -r requirements.txt` inside project repository)
* change User model so it suits your needs,
* copy example_local_settings.py and change name to local_settings.py (conigure db and email backend if needed)
* change secret_key in local_settings.py
* run makemigrations from manage.py
* run migrate
