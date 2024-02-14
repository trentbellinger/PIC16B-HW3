from flask import Flask, render_template, request, g
import sqlite3
app = Flask(__name__)


def get_message_db():
    '''Handles the creation of a SQL database for the messages that are presented in the website.'''
    try:
        return g.message_db
    except:
        # if a database is not present, we create one
        g.message_db = sqlite3.connect("messages_db.db")
        
        # if a messages table does not exist, we create one with columns for handle and text
        cmd = 'CREATE TABLE IF NOT EXISTS messages (message TEXT, handle TEXT)'
        
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        
        return g.message_db
    
def insert_message(request):
    '''
    Extracts the message and handle from a request and inserts them into the messages database.
    Arguments:
        request: a request that the user inputs to the webpage
    Returns:
        the message and handle from the request
    '''
    message = request.form["message"]
    handle = request.form["handle"]
    
    db = get_message_db()
    cursor = db.cursor()
    
    # insert the handle and message into the database
    cursor.execute(f'INSERT INTO messages (message, handle) VALUES ("{message}", "{handle}")')
    # commit the changes and close the connection
    db.commit()
    db.close()
    
@app.route('/')
def index():
    '''Creates the opening page of the app, which is the submit.html page.'''
    return render_template('submit.html')

@app.route('/submit', methods = ['POST', 'GET'])
def render_submit_template():
    '''Renders the submit.html file in the app, accounting for POST and GET requests.'''
    if request.method == 'POST':
        # for a POST request, we insert the message into the database
        insert_message(request)
        
        msg = "Thanks for your submission!"
        # render submit.html with a thank you message
        return render_template('submit.html', msg = msg)
    else:
        # for a GET request, simply render submit.html
        return render_template('submit.html')

def random_messages(n):
    '''
    Returns a collection of n random messages that have been previously inputted into the app.
    Arguments:
        n (int): the number of random messages to return
    Returns:
        messages (list): a list containing the name and message for the n random messages
    '''
    # Get the database connection
    db = get_message_db()
    cursor = db.cursor()

    # select the handle and message for n random entries in the messages table
    cursor.execute(f"SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}")
    # save the message (output[0]) and the handle (output[1]) in a list
    messages = [[output[0], output[1]] for output in cursor.fetchall()]
    
    # close the db connection
    db.close()

    return messages

@app.route('/view')
def view_random_messages():
    '''
    Creates a /view page of the app that displays 4 random messages that have been previously 
    inputted along with the name/handle of the person who submitted them.
    '''
    # get 4 random messages
    messages = random_messages(4)
    # render view.html with the 4 random messages
    return render_template('view.html', messages = messages)
    
if __name__ == '__main__':
    '''How to run the app, I had to use port=4999 for it to run on my device (5000 was not working).'''
    app.run(host='0.0.0.0', port=4999, debug=True)