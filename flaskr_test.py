import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    # Testing deleting an entry by adding an entry then deleting it
    def test_delete_message(self):
        rv = self.app.post('/add', data=dict(
            title='Test Entry',
            text='This is a test entry.',
            category='Test Category'
        ), follow_redirects=True)

        # Get the ID of the test entry
        rv = self.app.get('/')
        entry_id = rv.data.split(b'value="')[1].split(b'"')[0].decode('utf-8')

        # Delete the entry
        rv = self.app.post('/delete', data=dict(
            entry_id=entry_id
        ), follow_redirects=True)
        assert b'New entry was successfully posted' not in rv.data

    def test_edit_message(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)

        # Get the ID of the test entry
        rv = self.app.get('/')
        entry_id = rv.data.split(b'value="')[1].split(b'"')[0].decode('utf-8')


        rv = self.app.post('/update', data=dict(
            entry_id = entry_id,
            title = "Updated Entry",
            text = "Updated",
            category = "Updated Category"
        ))

        assert b'Updated Entry' in rv.data
        assert b'Updated' in rv.data
        assert b'Updated Category' in rv.data



if __name__ == '__main__':
    unittest.main()