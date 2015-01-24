# -*- coding: utf-8 -*-
__author__ = 'fgh'

import unittest
import mock

from mock import patch
from mock import Mock
from mock import call

from system import ensureExist

class UtilsSystemTestCase(unittest.TestCase):
    ################################################################################################
    ####### ensureExist(path)
    ################################################################################################
    def test_ensureExist_NonePath_EXCEPTION(self):
        try:
            ensureExist(None)
            self.assertFail()
        except Exception as inst:
            self.assertEqual(inst.message, "[utils.system.ensureExist ERROR] path param must not be None or empty!")

    def test_ensureExist_EmptyPath_EXCEPTION(self):
        try:
            ensureExist("")
            self.assertFail()
        except Exception as inst:
            self.assertEqual(inst.message, "[utils.system.ensureExist ERROR] path param must not be None or empty!")

    @mock.patch('os.path.exists')
    def test_ensureExist_OkPath_CallExist(self, mock_exists):
        mock_exists.return_value = True
        fake_path = 'fake/path'
        ensureExist(fake_path)
        mock_exists.assert_called_with(fake_path)

    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    def test_ensureExist_OkPath_OkCall(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        fake_path = 'fake/path'
        ensureExist(fake_path)
        mock_exists.assert_called_with(fake_path)
        mock_makedirs.assert_called_with(fake_path)


    # def test_emptyVar_OKValue_OKerror_None(self):
    #     self.assertEqual(isEmptyVar("TEST", "TEST"), None)
    # def test_emptyVar_NoneName_OKError_EXCEPTION(self):
    #     self.assertRaises(Exception, lambda: isEmptyVar(None, "TEST"))
    # def test_emptyVar_EmptyValue_OKError_EXCEPTION(self):
    #     self.assertRaises(Exception, lambda: isEmptyVar("", "TEST"))
    # def test_emptyVar_OkValue_NoneError_EXITERROR(self):
    #     self.assertRaises(Exception, lambda: isEmptyVar("TEST", None))
    # def test_emptyVar_OKValue_EmptyError_EXITERROR(self):
    #     self.assertRaises(Exception, lambda: isEmptyVar("TEST", ""))
    #
    #
    # ################################################################################################
    # ####### saveArrayInFile(inputArray, outputFile)
    # ################################################################################################
    # @patch('__builtin__.open')
    # def test_saveArrayInFile_NoneInputArray_OKoutputFile_writeCallsEmpty(self, open_mock):
    #     file = Mock()
    #     open_mock.return_value = file
    #     saveArrayInFile(None, "outputFile")
    #     file.write.assert_called_with("")
    #     file.close.assert_called_with()
    #
    # @patch('__builtin__.open')
    # def test_saveArrayInFile_emptyInputArray_OKoutputFile_writeCallsEmpty(self, open_mock):
    #     file = Mock()
    #     open_mock.return_value = file
    #     saveArrayInFile(list(), "outputFile")
    #     file.write.assert_called_with("")
    #     file.close.assert_called_with()
    #
    # @patch('__builtin__.open')
    # def test_saveArrayInFile_OneInputArray_OKoutputFile_WriteCallsWithArrayValue(self, open_mock):
    #     file = Mock()
    #     open_mock.return_value = file
    #     saveArrayInFile(["TEST"], "outputFile")
    #     file.write.assert_called_with("TEST")
    #     file.close.assert_called_with()
    #
    # @patch('__builtin__.open')
    # def test_saveArrayInFile_OneInputArray_OKoutputFile_WriteCallsTwiceWithArrayValue(self, open_mock):
    #     file = Mock()
    #     open_mock.return_value = file
    #     saveArrayInFile(["TEST1","TEST2"], "outputFile")
    #     calls = [call.write('TEST1'), call.write('TEST2'), call.close()]
    #     file.assert_has_calls(calls)
    #
    # def test_saveArrayInFile_OKInputArray_NoneOutputFile_Exception(self):
    #     try:
    #         saveArrayInFile(["test", "TEST"], None)
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "OutputFile must not be None or empty!")
    #
    # def test_saveArrayInFile_OKInputArray_EmptyOutputFile_Exception(self):
    #     try:
    #         saveArrayInFile(["test", "TEST"], "")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "OutputFile must not be None or empty!")
    #
    #
    # ################################################################################################
    # ####### createDictionaryFromSplitStrings(keys, values, splitCharKeys, splitCharValues)
    # ################################################################################################
    # def test_createDictionaryFromSplitStrings_NoneKeys_NoneValues_emptyDiccionary(self):
    #     result = createDictionaryFromSplitStrings(None, None, "splitCharKeys", "splitCharValues")
    #     self.assertFalse(bool(result))   #Empty dictionary passed to boolean is False
    #
    # def test_createDictionaryFromSplitStrings_emptyKeys_emptyValues_emptyDiccionary(self):
    #     result = createDictionaryFromSplitStrings("", "", "splitCharKeys", "splitCharValues")
    #     self.assertFalse(bool(result))   #Empty dictionary passed to boolean is False
    #
    # def test_createDictionaryFromSplitStrings_NoneKeys_emptyValues_emptyDiccionary(self):
    #     result = createDictionaryFromSplitStrings(None, "", "splitCharKeys", "splitCharValues")
    #     self.assertFalse(bool(result))   #Empty dictionary passed to boolean is False
    #
    # def test_createDictionaryFromSplitStrings_EmptyKeys_NoneValues_emptyDiccionary(self):
    #     result = createDictionaryFromSplitStrings("", None, "splitCharKeys", "splitCharValues")
    #     self.assertFalse(bool(result))   #Empty dictionary passed to boolean is False
    #
    # def test_createDictionaryFromSplitStrings_NoneKeys_NotEmptyOrNoneValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings(None, "TEST", "splitCharKeys", "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_EmptyKeys_NotEmptyOrNoneValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("", "TEST", "splitCharKeys", "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_NotEmptyOrNoneKeys_NoneValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("", None, "splitCharKeys", "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_NotEmptyOrNoneKeys_NoneValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "", "splitCharKeys", "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_NoneSplitCharKeys_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "TEST", None, "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "splitCharKeys is required!")
    #
    # def test_createDictionaryFromSplitStrings_EmptySplitCharKeys_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "TEST", "", "splitCharValues")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "splitCharKeys is required!")
    #
    # def test_createDictionaryFromSplitStrings_NoneSplitCharValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "TEST", "splitCharKeys", None)
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "splitCharValues is required!")
    #
    # def test_createDictionaryFromSplitStrings_EmptySplitCharValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "TEST", "splitCharKeys", "")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "splitCharValues is required!")
    #
    # def test_createDictionaryFromSplitStrings_oneValueWithoutSplit_diccionaryWithOneValue(self):
    #     result = createDictionaryFromSplitStrings("TEST", "TEST", "splitCharKeys", "splitCharValues")
    #     self.assertEqual(result["TEST"], "TEST")
    #
    # def test_createDictionaryFromSplitStrings_diferentNumberOfValues_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST", "TEST@TEST", "@", "@")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_diferentNumberOfKeys_EXCEPTION(self):
    #     try:
    #         createDictionaryFromSplitStrings("TEST@TEST", "TEST", "@", "@")
    #         self.assertFail()
    #     except Exception as inst:
    #         self.assertEqual(inst.message, "Keys have different number of elements than Values!")
    #
    # def test_createDictionaryFromSplitStrings_twoValues_diccionaryWithTwoValue(self):
    #     result = createDictionaryFromSplitStrings("TEST1@TEST2", "TEST1#TEST2", "@", "#")
    #     self.assertEqual(result["TEST1"], "TEST1")
    #     self.assertEqual(result["TEST2"], "TEST2")


def main():
    unittest.main()

if __name__ == '__main__':
    main()