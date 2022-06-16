import os
from unittest import TestCase
from flask import session

from models import db, connect_db, Word, User, Users_Words

os.environ['DATABASE_URL'] = 'postgresql:///wordgame-test'

from app import app

db.create_all()

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config["WTF_CSRF_ENABLED"] = False


class UserTestCase(TestCase):
    """Test user views"""

    def setUp(self):
        User.query.delete()
        Word.query.delete()
        Users_Words.query.delete()

        new_user = User.signup(username="test_user", password="12345")

        word = Word(word="eternity", syllable_count="4", pos="noun", definition="a state of eternal existence believed in some religions to characterize the afterlife", synonyms='["timeless existence",timelessness]')

        db.session.add(new_user)
        db.session.add(word)
        db.session.commit() 

        word_list = Users_Words(user=new_user.id, word=word.id)
        db.session.add(word_list)
        db.session.commit()

        self.word = word
        self.user = new_user

    def tearDown(self):
        db.session.rollback()

    def test_signup(self):
        """Can user sign up with a username and password? If username already taken, is user given feedback to try again?"""
        with app.test_client() as client:

            res = client.post('/signup', data={'username': 'test_user2', 'password': '56789'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-2">How to Play</h1>', html)
            self.assertIn('You have created an account', html)
            
            res = client.post('/signup', data={'username': 'test_user', 'password': '56789'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Sorry, that username is already taken. Please try another one.", html)


    def test_authenticate_valid_user(self):
        """Is user allowed to log in when valid credentials are given?"""
        
        with app.test_client() as client:

            res = client.post('/login', data={'username': 'test_user', 'password': '12345'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You are logged in", html)
            self.assertIn('<h1 class="display-2">How to Play</h1>', html)


    def test_authenticate_not_valid_user(self):
        """Is user with invalid credentials prevented from logging in?"""

        with app.test_client() as client:

            res = client.post('/login', data={'username': 'non_user', 'password': '12345'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Username or password not valid. Please try again.", html)
            self.assertNotIn('<h1 class="display-2">How to Play</h1>', html)

            res = client.post('/login', data={'username': 'test_user', 'password': 'bad_pwd'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Username or password not valid. Please try again.", html)
            self.assertNotIn('<h1 class="display-2">How to Play</h1>', html)


    def test_see_word_list_valid_user(self):
        """Can logged in users view a list of their words?"""

        with app.test_client() as client:

            with client.session_transaction() as sess:            
                sess['user_id'] = self.user.id

            res = client.get('/user-words')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Your Words</h1>", html)


    def test_see_word_list_not_valid_user(self):
        """Are users who are not logged in redirected and given feedback when they attempt to view words?"""

        with app.test_client() as client:

            res = client.get('/user-words', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Sorry, you must have an account to see your words.", html)
            self.assertIn("Welcome to Werd Nerdz!", html)


    def test_delete_word_valid_user(self):
        """Can logged in users delete a word from their list?"""

        with app.test_client() as client:

            with client.session_transaction() as sess: 
                sess['user_id'] = self.user.id
                sess['word'] = self.word.word

            res = client.post(f"/word-info/{self.word.word}/delete", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You have deleted a word from your list.", html)


    def test_delete_word_not_valid_user(self):
        """Are users who are not logged in prevented from deleting words?"""
        
        with app.test_client() as client:

            res = client.post(f"/word-info/{self.word.word}/delete", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You are not authorized to delete words.", html)