"""Test eFEL io module"""

# pylint: disable=F0401

import os
import nose.tools as nt

testdata_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'testdata')

meanfrequency1_filename = os.path.join(testdata_dir,
                                       'basic',
                                       'mean_frequency_1.txt')
meanfrequency1_url = 'file://%s' % meanfrequency1_filename


def test_import():
    """io: Testing import"""

    # pylint: disable=W0611
    import efel.io  # NOQA
    # pylint: enable=W0611


def test_import_without_urlparse():
    """io: Testing import without urlparse"""

    # The only purpose of this test is to get the code coverage to 100% :-)

    import sys
    del sys.modules['efel.io']

    python_version = sys.version_info[0]

    if python_version < 3:
        import __builtin__
    else:
        import builtins as __builtin__
    realimport = __builtin__.__import__

    def myimport(name, *args):  # global_s, local, fromlist, level):
        """Override import"""
        if name == 'urlparse':
            raise ImportError
        return realimport(name, *args)  # global_s, local, fromlist, level)
    __builtin__.__import__ = myimport

    try:
        import urllib.parse  # NOQA
        urllibparse_import_fails = False
    except ImportError:
        urllibparse_import_fails = True

    if urllibparse_import_fails:
        nt.assert_raises(ImportError, __builtin__.__import__, 'efel.io')
    else:
        import efel.io  # NOQA

    __builtin__.__import__ = realimport


def test_load_fragment_column_txt1():
    """io: Test loading of one column from txt file"""

    import efel
    import numpy

    time_io = efel.io.load_fragment('%s#col=1' % meanfrequency1_url)

    time_numpy = numpy.loadtxt(meanfrequency1_filename, usecols=[0])

    numpy.testing.assert_array_equal(time_io, time_numpy)


def test_load_fragment_strange_mimetype():
    """io: Test loading file with unresolvable mime type"""

    import efel

    nt.assert_raises(
        TypeError,
        efel.io.load_fragment, 'file://strange.mimetype')


def test_load_fragment_wrong_fragment_format():
    """io: Test loading file wrong fragment format"""

    import efel

    nt.assert_raises(
        TypeError,
        efel.io.load_fragment,
        '%s#co=1' %
        meanfrequency1_url)


def test_load_fragment_wrong_mimetype():
    """io: Test loading fragment wrong mime type"""

    import efel

    nt.assert_raises(
        TypeError,
        efel.io.load_fragment,
        '%s#col=1' % meanfrequency1_url, mime_type='application/json')


def test_load_fragment_allcolumns():
    """io: Test loading fragment without specifying columns"""

    import efel
    import numpy

    time_io = efel.io.load_fragment('%s' % meanfrequency1_url)

    time_numpy = numpy.loadtxt(meanfrequency1_filename)

    numpy.testing.assert_array_equal(time_io, time_numpy)
