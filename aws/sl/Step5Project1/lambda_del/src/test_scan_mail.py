# pylint: disable=unused-argument

import unittest
import lambda_function


class TestScanMail(unittest.TestCase):

    def test_scan_mail(self):


        with open('./lambda_del/sample-data/mail_body.txt', 'r') as file:
            content = file.read()

        filename = lambda_function.scan_mail(content)
        print(filename)



if __name__ == '__main__':
    unittest.main()