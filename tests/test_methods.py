""" ********************************************************

Project: nita-yaml-to-excel

Copyright (c) Juniper Networks, Inc., 2021. All rights reserved.

Notice and Disclaimer: This code is licensed to you under the Apache 2.0 License (the "License"). You may not use this code except in compliance with the License. This code is not an official Juniper product. You can obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.html

SPDX-License-Identifier: Apache-2.0

Third-Party Code: This code may depend on other components under separate copyright notice and license terms. Your use of the source code for those components is subject to the terms and conditions of the respective license as noted in the Third-Party source code file.

******************************************************** """

import unittest
from collections import OrderedDict

from ddt import ddt, data

from yamltoexcel import yaml2xls


@ddt
class ParserMethodsTestCase(unittest.TestCase):
    """Unit tests for yaml2xls parser helper methods."""

    @data(5, False, '12.12.12.12', "Test")
    def testParseCellValue(self, value):
        """parse_cell_value converts bools to str and passes ints through unchanged."""
        if isinstance(value, bool):
            temp_value = str(value)
        elif isinstance(value, int):
            temp_value = value
        else:
            temp_value = str(value)
        yaml2excel = yaml2xls.YamlToExcel("yaml_file")
        self.assertEqual(yaml2excel.parse_cell_value(value), temp_value)

    def testBuildListData(self):
        """build_list_data returns only the list-valued keys from the input dict."""
        input_data = OrderedDict({"boot_server": "10.1.10.134",
                                  "radius_server": "10.1.10.135",
                                  "servers": [
                                      "10.99.0.134",
                                      "10.0.2.5",
                                      "10.10.72.184"
                                  ]
                                  })
        expected_result_data = {"servers": [
            "10.99.0.134", "10.0.2.5", "10.10.72.184"]}
        yaml2excel = yaml2xls.YamlToExcel("yaml_file")
        self.assertEqual(yaml2excel.build_list_data(
            input_data), expected_result_data)

    def testBuildDictData(self):
        """build_dict_data flattens nested dicts and handles prefixes and unique identifiers."""

        input_data = OrderedDict({"boot_server": "10.1.10.134",
                                  "radius_server": "10.1.10.135",
                                  "servers": [
                                      "10.99.0.134",
                                  ]
                                  })
        expected_result_data = {
            "boot_server": "10.1.10.134", "radius_server": "10.1.10.135"}

        yaml2excel = yaml2xls.YamlToExcel("yaml_file")
        self.assertEqual(yaml2excel.build_dict_data(
            input_data), expected_result_data)

        old_data = OrderedDict({"Old_data": "Test"})
        expected_result_data.update(old_data)
        self.assertEqual(yaml2excel.build_dict_data(
            input_data, old_data), expected_result_data)

        expected_result_data = OrderedDict(
            {"ntp.boot_server": "10.1.10.134", "ntp.radius_server": "10.1.10.135"})
        self.assertEqual(yaml2excel.build_dict_data(
            input_data, {}, "ntp"), expected_result_data)

        input_data = OrderedDict({"name": "SKCpolling",
                                  "clients": [
                                      "192.168.0.0/16",
                                      "10.1.0.53/32",
                                      "10.10.7.2/32"
                                  ]
                                  })
        expected_result_data = {'@name': 'SKCpolling'}
        self.assertEqual(yaml2excel.build_dict_data(
            input_data, {}, "", True), expected_result_data)


def runTests():
    suite = unittest.makeSuite(ParserMethodsTestCase, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    runTests()
