# Project 2

Web Programming with Python and JavaScript

Requirements:
    Display Name: When a user visits your web application for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
    --This is accomplished through local storage of 'user_name', stored after logging into a channel

    Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
    --This is accomplished by selecting "(other channels)" and then clicking "New channel" in the side nav bar.

    Channel List: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
    --This is accomplished by selecting "(other channels)" in the side nav bar. It will update dynamically by rooms added.

    Messages View: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
    --This is accomplished by creating a deque with a limit of 100.

    Sending Messages: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
    --This is accomplished in the chat room.

    Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes back to your web application, your application should remember what channel the user was on previously and take the user back to that channel.
    --This is accomplished in index.html that runs only some javascript to redirect the user.

    Personal Touch: Add at least one additional feature to your chat application of your choosing! Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting private messaging between two users.
    --Other features that were added are the following:

    (1) - User is able to logout
    (2) - Users receive a message if another user has left or joined a room. If that user is still viewing that room from multiple areas, such as tab/window, no message is broadcasted when they leave. Similarly no message is displayed when a user joins a room and they were already viewing it on another tab/window.
    (3) - Security feature: A user cannot inject html into the messages.
    (4) - Even with (3) a user can keep their return characters entered, allowing for some formatting.
    (5) - Users are able to view new rooms without refreshing
    (6) - Auto scroll to bottom of messages when a new message is entered
    (7) - Users must be unique and provide passwords
    (8) - Security feature: A user cannot inject html into the room names.
    (9) - User is able to enter a message by pressing 'Enter' or add a return line to the message by pressing 'Shift+Enter'.

Files:
    ..\project2
        application.py - Contains most logic for url redirect
        Channel.py - Contains Channel class to be used by application.py. Running it will perform test.
        Flacker.py - Contains Flacker (i.e. user) class to be used by application.py. Running it will perform test.
        README.md - information on project2
        requirements.txt - contains all requirements for project2

    ..\project2\templates
        channel_list.html - A file used to style the list of channels for the navbar
        chat.html - the main file for sending messages in the channels
        index.html - a file to run a redirect url
        layout.html - a main layout file for all main pages to extend
        login_error.html - displays error if user put information in login that was invalid
        login.html - area for user to enter credentials or register
        new_channel_error.html - displays an error if user put channel information that was invalid
        new_channel.html - allows user to create a new channel

    ..\project2\static\javascript
        chat.js - contains logic for chat.html.
        index.js - contains redirect logic for index.html to get the user to login or their last channel.
        login.js - contains logic for login.html.

    ..\project2\static\styles
        chat.scss - SCSS file for chat.css
        chat.css.map - map file between chat.css and chat.scss
        chat.scss - all styling for chat.html, including a navbar and message cards.
