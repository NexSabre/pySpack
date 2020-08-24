import unittest
from build.lib.pySpack import pyspack

from pySpack.pyspack import PySpack


class Test_TestPySpack(unittest.TestCase):
    def setUp(self):
        self.pyspack = PySpack()

    def test_install(self):
        self.assertTrue(self.pyspack.install('py-json5'), "py-json5 should be installed")

    def test_is_installable(self):
        self.assertTrue(self.pyspack.is_installable('py-json5'), "py-json5 should be installable")

    def test_find(self):
        self.pyspack.install('py-json5')
        self.assertTrue(self.pyspack.find('py-json5'), "py-json5 should be on the list of installed packages")

    def test_not_found(self):
        self.pyspack.uninstall('py-json5')
        self.assertFalse(self.pyspack.find('py-json5'), "py-json5 should not be found after uninstallation")

    def test_uninstall(self):
        self.pyspack.install('py-json5')
        self.assertTrue(self.pyspack.uninstall('py-json5'), "py-json5 should be uninstalled correctly")

    def test_load(self):
        self.pyspack.install('py-json5')
        load_output = self.pyspack.load('py-json5')
        self.assertTrue(self.find_python_path(load_output, 'py-json5'), "py-json5 should be available at PYTHONPATH string returned by the Spack")

    def test_negative_load(self):
        package_which_not_exists = 'py-random-package-which-does-not-exists'
        load_output = self.pyspack.load(package_which_not_exists)
        self.assertFalse(self.find_python_path(load_output, package_which_not_exists))

    @staticmethod
    def find_python_path(decoded_output: str, package_to_find: str) -> bool:
        exports_list = [x for x in str(decoded_output).split(';') if 'PYTHONPATH' in x]
        for element in exports_list: 
            if package_to_find in element:
                break
        else:
            return False        
        return True
