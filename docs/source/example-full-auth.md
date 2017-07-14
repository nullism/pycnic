[[
title: Full authentication example
timestamp: 2015-11-08 21:00
tags: [examples]
]]

[TOC]

# Full Authentication Example

This example handles the following operations: 

1. Create a database in memory with `users` and `user_sessions` tables.
2. Provides a `/login` handler which sets up a session.
3. Provides a `/home` handler which checks for a session.
4. Provides a `/logout` handler which deletes a session.

## Running the example

This example uses SQLAlchemy, but the principles are the same with most ORMs. 
To run this specific example you will need SQLAlchemy installed, which
can be done with `pip(3) install sqlalchemy`

1. Place `app.py` and `models.py` in the same directory.
2. Run `app.py` with your `python` command (2.7/3 should work). 
3. Use a JSON API tool, such as Advanced Rest for Chrome, to perform the following calls:
    1. `POST /login` with a payload of `{ "username":"foo", "password":"foo" }`.
    2. `GET or POST /home`. You should see a message of "Hello, foo".
    3. `POST /logout`
    4. `GET or POST /home`. You should now see a 401 error.

## app.py

    :::python
    #!/usr/bin/env python3
    from functools import wraps
    from pycnic.core import WSGI, Handler
    from pycnic.errors import HTTP_401, HTTP_400
    # Import our SQLAlchemy stuff
    from models import User, UserSession, Session, Base, engine

    # Start the :memory: sqlite session
    db = Session()

    def get_user(request):
        """ Lookup a user session or return None if one doesn't exist """

        sess_id = request.cookies.get("session_id")
        if not sess_id:
            return None
        sess = db.query(UserSession).filter(
            UserSession.session_id == sess_id).first()
        if not sess:
            return None
        if not sess.user:
            return None
        return { "username": sess.user.username }

    def requires_login():
        """ Wrapper for methods that require login """

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if not get_user(args[0].request):
                    raise HTTP_401("I can't let you do that")
                return f(*args, **kwargs)
            return wrapped
        return wrapper

    class Home(Handler):
        """ Handler for a message with the user's name """    

        @requires_login()
        def get(self):
            user = get_user(self.request)
            return { "message":"Hello, %s"%(user.get("username")) }

        @requires_login()
        def post(self):
            return self.get()

    class Login(Handler):
        """ Create a session for a user """    

        def post(self):

            username = self.request.data.get("username")
            password = self.request.data.get("password")
            
            if not username or not password:
                raise HTTP_400("Please specify username and password")

            # See if a user exists with those params
            user = db.query(User).filter(
                User.username==username, 
                User.password==password).first()
            if not user:
                raise HTTP_401("Invalid username or password")
           
            # Create a new session 
            sess = UserSession(
                user_id=user.id)
            db.add(sess)
            self.response.set_cookie("session_id", sess.session_id) 
            return { "message":"Logged in", "session_id":sess.session_id }

    class Logout(Handler):
        """ Clears a user's session """    

        def post(self):
            
            sess_id = self.request.cookies.get("session_id")
            if sess_id:
                # query to user sessions table
                sess = db.query(UserSession).filter(
                    UserSession.session_id==sess_id).first()
                if sess:
                    db.delete(sess)
                self.response.delete_cookie("session_id")
                return { "message":"logged out" } 
            return { "message":"Not logged in" }

    class app(WSGI):
        routes = [ 
            ('/home', Home()),
            ('/login', Login()),
            ('/logout', Logout())
        ]

    if __name__ == "__main__":

        print("DB: Creating users table in memory...")    
        Base.metadata.create_all(engine)

        print("DB: Adding users...")
        db.add_all([
            User(username="foo", password="foo")
        ])

        from wsgiref.simple_server import make_server
        try:
            print("Serving on 0.0.0.0:8080...")
            make_server('0.0.0.0', 8080, app).serve_forever()
        except KeyboardInterrupt:
            pass
        print("Done")

## models.py

This file contains the SQLAlchemy database models as well
as a method to generate session ids in SHA1 format.

    :::python
    from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, backref
    import hashlib
    import time

    engine = create_engine('sqlite:///:memory:', echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)

    def get_new_session_id():
        """ Generates a sha1 session id """

        to_hash = "%s_SECRET"%(time.time())
        return hashlib.sha1(to_hash.encode('utf-8')).hexdigest()    
        
    class UserSession(Base):

        __tablename__ = "user_sessions"
        id = Column(Integer, primary_key=True)
        session_id = Column(String, 
            default=get_new_session_id, onupdate=get_new_session_id)
        user_id = Column(Integer, ForeignKey('users.id'))
        user = relationship("User", backref=backref("sessions"), order_by=id)

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)

