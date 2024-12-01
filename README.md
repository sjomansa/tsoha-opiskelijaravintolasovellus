Application shows the student-restaurants for in a list view. Each restaurant has a grade from (1-5), average que time and a restaurant owner. 

In each restaurant page, student users are able to chat about the restaurant in the comment section, see its menu for the day, rate and add que times for the restaurant, see information (opening times, adress) and add information about any specialities about the restaurant (Special made chili sauce, Special coffee availabe, funny staff member...)

  -Users can filter restaurants based on owner, rating and que time. (Coming) 🟨

  -Users can sort by owner, rating and que time on the restaurant list view. (Coming) 🟨
  
  -A user can sign in / register as a restaurant or a student. They can also sign out. 🟩

  -User can rate a restaurant and add a que time. Detail view will show the average of this rating / que time. (Coming) 🟨

  -User can write a comment about a restaurant in the comment section. They are able to see other comments about the restaurant. 🟩

  -Users can add a comment/note about a speciality in the restaurant. They can like other such notes so that the specialities are shown in order by most likes in the restaurants page. (Coming) 🟨

  -Restaurant owners can acess a special view where they can see all their restaurants. 🟩

  -Restaurant owner can add new restaurants. They can edit their own restaurants information (menu, opening time, location, city). They can also delete their own restaurants. (Everything except deletion is complete) 🟨

  -Looks need to be improved

  -Need to implement checking for session user (currently you are able to access certain views without being signed in)

  -Error messages need to be in finnish


INSTRUCTIONS FOR LOCAL TESTING:

Clone this repository into you device and change the current directory to its root directory. 
  
Create a .env file inside the directory and set up the following:

DATABASE_URL= the local address of your psql database

SECRET_KEY= your own secret key here 

Next activate the virtual environment and install dependencies listed on requirements.txt:

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt

IMPORTANT! Then add the SQL schemas AND the testdata. The testdata is dummydata that is located in testdata.sql.


This will showcase the app functionality better.

So do the following: 

First:

$ psql < schema.sql

Then:

$ psql < testdata.sql

Then you can run

$ flask run