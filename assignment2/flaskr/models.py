import os
import json
import bcrypt
import uuid

from .db import getDB, queryDB, insertDB

def registerUser(username, password):
    isSuccess = False

    # Check input lengths
    if len(username) == 0 or len(password) == 0:
        return (isSuccess, 'Invalid username or password length')

    # Check username uniqueness
    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)
    if res is not None:
        # User already exists inside the database
        return (isSuccess, 'The supplied username is already in use')
    else:
        # Registration successful
        insertDB('INSERT INTO users (username, passhash) values (?, ?)', (username, password))
        isSuccess = True
    return (isSuccess, 'Registration successful')

# Returns tuple of (success, session)
# Session is the username in this case.
def validateUser(username, password):
    isSuccess = False

    if len(username) == 0 or len(password) == 0:
        return (isSuccess, None)

    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)

    if res is not None:
        if res[2] == password:
            # Login succeeded
            isSuccess = True
            return (isSuccess, username)
        return (isSuccess, username)

    return (isSuccess, None)

def isUserAdmin(username):
    isSuccess = False

    if not username:
        return (isSuccess, False)

    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)

    if res is not None:
        if res[3] == 1:
            isSuccess = True
            return (isSuccess, True)
        return (isSuccess, False)

    return (isSuccess, False)

def getUserCreds(username):
    isSuccess = False

    if not username:
        return (isSuccess, False)

    res = queryDB('SELECT name, address, email, phonenum, funds FROM creds JOIN users ON users.uid=creds.uid WHERE username = ?', [username], one=True)

    if res is not None:
        isSuccess = True
        return (isSuccess, res)

    return (isSuccess, False)