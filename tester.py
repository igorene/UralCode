import os
import FSite
import unittest
import tempfile

class FsiteTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Fsite.app.config['DATABASE'] = tempfile.mkstemp()
        Fsite.app.config['TESTING'] = True
        self.app = Fsite.app.test_client()
        Fsite.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Fsite.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()