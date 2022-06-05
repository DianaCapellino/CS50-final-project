# GOLDEN DOT GAMES WEBSITE
#### Video Demo:  https://youtu.be/hwDpyCyBkhw
#### Description:

This is a web application for a fantasy company named Golden DOT Games.
The original idea came up as I wanted to build a website for uploading the games I would like to develop in the future. The games proposed in the website are real ideas about future projects that I would like to implement and upload. I thought that making the first step and build the website functionality would work for the final project and also be useful for the future.

I had many ideas but some of them were left for the future as they would imply so much more time that I have planed for the final project in CS50. However, most of them were implemented, leaving behind just the game developments and the game specifications that have its place in the database but the content is not yet prepared.

The website has the following pages saved in the templates folder:

- index.html: 
    You access this page through the golden dot image or when you enter the website.
    It has just a welcome message.

- games.html: 
    It is acceded by clicking "GAMES" button in the menu.
    In this page you can see all the games to be realased by Golden DOT Games and you can click on "Add to favourites" to add the games in your list, but only if you have logged in.
    The information of the games is in the database saved in goldendot.db (SQLite).

- news.html: 
    You can access this site by clicking "NEWS" button in the menu.
    This page is a list of articles that are read from a News API. It brings the most relevant videogames news in the last 7 days.

- yourgames.html: 
    This page is acceded by clicking "YOUR GAMES" button in the menu. It is restricted for logged in users.
    It brings the list of the games the user has added to favourites with a picture of the game, the name, and the alternative to remove from favourites.

- contactus.html: 
    It is acceded by clicking "CONTACT US" button in the menu.
    For leaving a message any person could leave a name, message and e-mail. If an e-mail is not provided then a page error would appear but the message will be sent to the company e-mail address anyway.

- register.html: 
    The register page is access when clicking "Register" in the menu. It is hidden when user has already logged in.
    It is compulsory to give a username and a password, repeat it, and giving an e-mail. The password that the user repeats should be the same and the e-mail should be valid as the company send and e-mail with the validation link with a token.
    The username cannot be repeated.

- login.html: 
    This page can be acceded by clicking "Log in" in the menu. If the user has already logged in, the option is not shown.
    If a user has just registered and tries to log in, it will return an error page if the user's e-mail hasn't been authenticated by clicking the link within 5 minutes received the token.
    The user should provide the username and password.

- error.html: 
    It is page that can be returned when there is an error, always with the same image but different messages.

- layout.html: 
    It contains the layout for the nav menu and footer.

The web application works with Python with Flask and the database has been made with SQLite. The files used for all of this are:

- app.py: 
    It contains the core of the application with the connection to the database, the sessions, the templates and all the details to make the website works.

- helpers.py: 
    It has 3 functions: "error" to manage the logic when an error ocurrs; "login_required" to decorate the functions where the user should be logged in; and "get_news" that contains the information and steps to connect with the news API.

- config.cfg: 
    It has all the configuration for sending e-mails from the Golden DOT Games e-mail account.

- goldendot.db: 
    It is the database with SQLite built in 3 tables: "users" that contains the essential information of the users with a unique ID; "favourites" with the information of the games saved per user_id; and "games" that has all the information about the games including the link to the images, descriptions, etc.

In the static folder is saved all the images and the styles.css where all the style is implemented.
