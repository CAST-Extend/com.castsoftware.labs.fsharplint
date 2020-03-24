import unittest
from cast.application.test import run
from cast.application import create_postgres_engine
import logging

logging.root.setLevel(logging.DEBUG)

class TestIntegration(unittest.TestCase):

    def test2(self):
        
        run(kb_name='microsharp_local', application_name='qtest', engine=create_postgres_engine())
       

if __name__ == "__main__":
    unittest.main()
