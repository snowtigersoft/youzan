#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 - kylinlingh@foxmail.com

import unittest

from src import apiprotocol


class ApiTest(unittest.TestCase):

    test_obj = apiprotocol.ApiProtocol()

    def test_sign(self):
        test_dict = {
        'method' : 'kdt.item.get',
        'timestamp' : '2013-05-06 13:52:03',
        'format' : 'json',
        'app_id' : 'test',
        'v' : 1.0,
        'sign_method' : 'md5',
        'num_iid' : 3838293428
        }
        app_sert = 'test'


        true_result = 'testapp_idtestformatjsonmethodkdt.item.getnum_iid3838293428sign_methodmd5timestamp2013-05-06 13:52:03v1.0test'
        test_result = self.test_obj.sign(app_sert, **test_dict)
        self.assertEqual(test_result, true_result)

    def test_hash(self):

        true_result = '74d4c18b9f077ed998feb10e96c58497'
        test_content = 'testapp_idtestformatjsonmethodkdt.item.getnum_iid3838293428sign_methodmd5timestamp2013-05-06 13:52:03v1.0test'

        test_result = self.test_obj.hash(test_content)
        self.assertEqual(test_result, true_result)


if __name__ == '__main__':
    unittest.main()