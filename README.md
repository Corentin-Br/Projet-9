# LitrReview
A website using Django and Bootstrap frameworks to allow users to ask for and give opinions on books.

## Setup and execution:
This website can b einstalled and deployed locally following these steps:

### Setup
1. Clone the repository using`$git clone https://github.com/Corentin-Br/Projet-9.git` or downloading [the zip file](https://github.com/Corentin-Br/Projet-9/archive/refs/heads/master.zip).
2. Create the virtual environment with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
3. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
4. Install the dependencies with `$ pip install -r requirements.txt`.

### Execution
1. If that's not already the case, activate the virtual environment as you did during the setup.
2. Get in the folder LitrReview with `$ cd litrreview`
3. Deploy the website locally with `$ python manage.py run server`
4. Use your preferred browser and go to `127.0.0.1:8000`. If everything worked, you should be on the login page for the website. If it doesn't, make sure you have no other server deployed locally at the same address.


### Use
1. It's possible to create accounts to use the website.
2. In addition, three tests accounts are available : `test_user_1` with the password `password_test_1`, `test_user_2` with the password `password_test_2`, and `test_user_3` with the password `password_test_3`.
Those accounts already have some tickets and reviews and some of them follow each other to check various features.