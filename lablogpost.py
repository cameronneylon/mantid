# LaBLogPost: A python library for interacting with the University
# of Southampton LaBLog System as an electronic lab notebook
#
# Public Domain Waiver:
# To the extent possible under law, Cameron Neylon has waived all 
# copyright and related or neighboring rights to lablogpost.py
# This work is published from United Kingdom.
#
# See http://creativecommons.org/publicdomain/zero/1.0/
#
# Dependencies: The application requires a range of modules from the
# Python 2.6 standard library. It also requires security access to a
# deployment of the LaBLog system. 
# 
# The LaBLog REST API is documented at: 
# http://chemtools.chem.soton.ac.uk/wiki/index.php?title=Blog:API_REST

import os.path
import base64
import unittest
import urllib2
import urllib
import socket
import logging
from xml.etree import ElementTree as ET

# Global Variables

MAX_MEM = 50000
DEFAULT_URL = 'http://biolab.isis.rl.ac.uk'
DEFAULT_UID = '' 
DEFAULT_USERNAME = ''

socket.setdefaulttimeout(10)

def set_proxy(boolean, proxy = 'ral'):
    """Method for setting up proxy arrangements

    Default proxy is currently for RAL which is one of the few
    places where this will actually be needed.
    """

    assert type(boolean) == bool, 'Allowed arguments are True and False'

    proxies = {'none': {},
               'ral' : {'http' : 'http://wwwcache.rl.ac.uk:8080'}
              }

    if boolean == True:
        # If the method is called to setup proxies
        # Setup proxy handler and then install an opener for use
        assert proxy in proxies, 'No information for that proxy'
        proxy_support = urllib2.ProxyHandler(proxies[proxy])
        urllib2.install_opener(urllib2.build_opener(proxy_support))

    elif boolean == False:
        # If the method is called to remove proxies 
        # Set up as empty
        proxy_support = urllib2.ProxyHandler(proxies['none'])
        urllib2.install_opener(urllib2.build_opener(proxy_support))
        
    try:
        f = urllib2.urlopen('http://google.com')
        assert f.read(21) == '<!doctype html><html>'
        return True

    except urllib2.URLError:
        return False

class LaBLogObject(dict):
    """A subclass of dictionary representing LaBLog Objects

    A generic class that holds common methods for the Data and Post objects. Will
    be able to add URL handling and common information here and inherit to both
    derivative classes.
    """

    def __init__(self, title = None):
        """Builder for LaBLogData objects"""

        self.title = title
        self.posted = False

    def set_title(self, title):
        if type(title) != str:
            raise TypeError('Title must be a string')
            return

        self.title = title
        

class LaBLogData(LaBLogObject):
    """LaBLogObject subclass with methods for setting up LaBLog Data objects

    The LaBLogData object represents a post to be made and subsequently the
    post that was made to a LaBLog. Making a data post requires a type 
    (inline, local, or url, generally local), 'main', the data itself,
    which is base64 encoded, and a title. These are wrapped as an XML
    object which is sent to the LaBLog API.

    Functions are provided to set the type, prepare the data, serialize
    the object as XML and to post to a LaBLog. Following posting the 
    internal variable self.posted is set to True and the data id and
    url returned by the LaBLog are available from self.data_id and 
    self.url respectively.

    The constructor can be called with no variables or with a dictionary
    of the required entities in the form of a dictionary or as arguments
    filename and title. Variables self.main defaults to '1' and self.type 
    defaults to 'local', which is the only method currently implemented.
    """

    def __init__(self, filename = None, title = None):
        LaBLogObject.__init__(self, title)
        self.type = None
        self.main = '1'
        self.data = None
        self.filename = filename
        self.url = None
        self.title = title
        self.etree = ET.ElementTree()
        self.postxml = None

    def set_type(self, locationtype):
        if type(locationtype) != str:
            raise TypeError('Locationtype must be a string')
            return

        if locationtype in ['inline', 'url', 'local']:
            self.type = locationtype
        else:
            raise ValueError('Type must be one "inline", "url", or "local"')


    def set_data(self, filename, dir=None, usefilename=True):

        # If filename looks like a full or relative path
        if os.path.split(filename) != filename:
            # Test that it really does point at something
            if os.path.exists(filename):
                pass
            else:
                raise OSError('Filename does not point to existing file?')
                return

            # Rename variables ready for getting name and extension
            fullpath = filename
            dir, file = os.path.split(filename)
            filename = file

        # If a directory is given    
        if dir != None:
            ###Add path to filename###
            fullpath = os.path.join(dir, filename)

            # Test that it really does point at something
            if os.path.exists(fullpath):
                pass
            else:
                raise OSError('Filename does not point to existing file?')
                return
        
        self.filename = filename
            
        # If a file extension appears to be present
        if '.' in filename:
            ext = filename.rsplit('.')[-1]
            self.ext = ext
        
        else:
            self.ext = None

        # Open and encode the file
        f = open(fullpath)
        # TODO:should possibly append file in chunks?
        # Add base64 encoded file to data object
        self.data = base64.standard_b64encode(f.read(MAX_MEM))

        # If usefilename = True then set title to be the filename
        if usefilename == True:
            self.set_title(filename.split('.')[0])


    def serialize(self):
        """Method for serializing the datapost object

        Adapted from what was originally a separate script file for
        generating the xml to be posted. This version simply brings
        that code in directly as an internal method. Future versions
        should perhaps have serialization methods for specific
        subelements and/or provide JSON or other formats.

        The LaBLog API requires an XML packet containing a range of information
        The init method takes a dictionary and returns the ElementTree object 
        ready for conversion to an XML file for posting.
        """
        # Test for presence of required elements in the data object
        assert self.postxml == None
        assert self.title != None and type(self.title) == str
        assert self.filename != None and type(self.filename) == str
        assert self.ext != None and type(self.ext) == str
        assert self.main == '1'
        assert self.data != None and type(self.data) == str

        # Create the <post> element as a subelement of the root
        dataset = ET.Element("dataset")
        ET.SubElement(dataset, "title").text = self.title
        data = ET.SubElement(dataset, "data")
        dataitem = ET.SubElement(data, "dataitem")

        # For inline file types populate the fields and values
        if self.type == 'inline':
            dataitem.set('type', 'inline')
            dataitem.set('filename', self.filename)
            dataitem.set('ext', self.ext)
            dataitem.set('main', self.main)
            # Assumes an incoming base64 encoded string
            dataitem.text = self.data

        # TODO: setup for online files

        self.etree._setroot(dataset)
        self.postxml = ET.tostring(dataset)
        

    def doPost(self, url=DEFAULT_URL, uid=DEFAULT_UID):
        """Method for posting the data object. Returns the post ID.

        doPost checks that required information is present and then
        posts the data object to the blog. The function returns the
        blog data ID object. The URL status code is posted to
        self.returned_post_status. XML is not generated until this 
        function is called as this is the first point where the 
        presence of all the required objects is explicitly tested.
        """

        # Check that self.posted is False
        assert self.posted == False

        # First check that the required elements are there
        assert self.title != None and type(self.title) == str
        assert self.type != None and type(self.type) == str

        if self.type == 'inline':
            assert self.data != None and type(self.data) == str

        if self.type == 'url': # TODO actually implement url method
            assert self.dataurl != None and type(self.dataurl) == str
            
        # Serialize the data object to generate the data post XML
        self.serialize()

        # Set up the Request object
        requesturl = url + '/api/rest/adddata/uid/' + uid
        request = urllib.urlencode({'request':self.postxml})
        post = urllib2.Request(requesturl, data=request)

        response = urllib2.urlopen(post)
              
        # Parse the response and get the status code
        parsedresponse = ET.parse(response)
        statuscode = parsedresponse.find('status_code').text
        success = parsedresponse.find('success').text
        self.post_status_code = statuscode
        self.post_response = response.read(100)

        # If statuscode is ok then return the post ID
        if success == 'true' and statuscode == '200':
            self.posted = True
            self.data_id = parsedresponse.find('data_id').text

            return self.data_id

        else:
            return False
        

class LaBLogPost(LaBLogObject):
    """A LaBLogObject subclass representing LaBLog Posts

    The LaBLogPost object represents a blog post that will be posted
    to and subsequently available at a LaBLog. Making a post requires
    a username, some text content, a blog_id (or blog short name) and
    a section. Optionally the post may include metadata elements as
    key value pairs or references to attached data that already have 
    a data_id in the LaBLog system. These elements are wrapped as an
    XML object to be sent to the LaBLog API.

    The constructor can be called with no variables or with a 
    dictionary of required elements. Default values for all internal
    elements are None except for the etree representation of the 
    XML serialization which is initialized to an empty 
    etree.ElementTree instance.

    The variables self.username, self.content, self.blog_id, 
    self.section, and self.blog_sname are all strings. The 
    self.metadata element is a dictionary and self.attached data
    is a list containing at least one member or is None. Following 
    posting self.posted is set to True, and the returned HTTP status
    code is stored at self.post_status_code. The main response is at
    self.post_response. The LaBLog post ID number is stored (as a 
    string) at self.post_id and the xml and html versions of the 
    generated post are in self.url_xml and self.url respectively.

    Methods are provided for setting all the appropriate internal
    variables, for serialization to XML and for posting. Serialization
    is only carried out as part of the posting process as this is the
    first time that the presence of all required elements is tested
    for. Methods are also provided for appending and overwriting the
    metadata."""

    def __init__(self, username = None, content = None, 
                 blog_id = None, section = None, blog_sname = None,
                 metadata = None, attached_data = [], title = None):

        LaBLogObject.__init__(self, title)
        self.username = username
        self.content = content
        self.blog_id = blog_id
        self.section = section
        self.blog_sname = blog_sname
        self.metadata = metadata
        self.attached_data = attached_data
        self.etree = ET.ElementTree()
        self.postxml = None
        
    def set_username(self, username):
        self.username = username

    def set_section(self, section):
        self.section = section

    def set_content(self, content):
        self.content = content

    def append_content(self, content):
        if not self.content:
            self.content = ''
        self.content += content

    def set_blog_id(self, blog_id):
        self.blog_id = blog_id

    def set_blog_sname(self, blog_sname):
        self.blog_sname = blog_sname

    def set_metadata(self, inputdictionary):
        self.metadata = inputdictionary

    def append_metadata(self, inputdictionary, overwrite=False):
        """Method for appending further metadata key-value pairs

        Provides a method for adding additional metadata elements
        to an empty or non-empty self.metadata. A safety is 
        provided for a key that is already present a ValueError
        is raised unless the overwrite = True option is invoked.
        """

        if not self.metadata:
            self.metadata = {}

        for key, value in inputdictionary.iteritems():
           if key not in self.metadata:
               self.metadata[key] = value

           elif key in self.metadata and overwrite==True:
               self.metadata[key] = value

           elif key in self.metadata and overwrite==False:
               raise ValueError("""Key already in metdata,
                       use overwrite=True option to overwrite if desired""")

           else:
               pass


    def set_attached_data(self, datalist):
        self.attached_data = datalist

    def append_attached_data(self, datalist, overwrite=False):
        for data_id in datalist:
           if (data_id in self.attached_data) and overwrite==False:
               raise ValueError("""Data ID already in attached data list.
                       Use overwrite=True option to overwrite if desired""")

           elif data_id in self.attached_data and overwrite==True:
               pass

           else:
               self.attached_data.append(data_id)

    def serialize(self):
        """Method for generating Post XML required for doPost

        This was adapted from a separate function. Currently only generates
        XML versions of the post as both ElementTree instance (self.etree)
        and an xml string (self.postxml). Future versions should probably offer
        the opportunity of serializing to JSON or to simply aggregate serializations
        of all the constituent objects.
        """
        # Test for presence of required elements in the post object
        assert self.title != None and type(self.title) == str
        assert self.section != None and type(self.section) == str
        assert self.username != None and type(self.username) == str
        assert self.content != None and type(self.content) == str        

        # Create the <post> element as a subelement of the root
        post = ET.Element("post")

        # Create and populate the required subelements of <post>
        ET.SubElement(post, "title").text = self.title
        ET.SubElement(post, "section").text = self.section
        author = ET.SubElement(post, "author")
        ET.SubElement(author, "username").text = self.username
        ET.SubElement(post, "content").text = self.content

        # Test for and create the optional elements of <post>
        if self.blog_id != None:
            assert type(self.blog_id) == str
            ET.SubElement(post, "blog_id").text = self.blog_id

        if self.blog_sname != None:
            assert type(self.blog_sname) == str
            ET.SubElement(post, "blog_sname").text = self.blog_sname

        if self.blog_id == None and self.blog_sname == None:
            raise ValueError("""Require one of blog_id or blog_sname""")

        if self.metadata != None:
            assert type(self.metadata) == dict
            metadata = ET.SubElement(post, "metadata")
            # Create and populate metadata elements
            for key, value in self.metadata.iteritems():
                ET.SubElement(metadata, key).text = value

        if self.attached_data != None:
            assert type(self.attached_data) == list
            attached_data = ET.SubElement(post, "attached_data")
            # Create and populate attached data elements
            for data in self.attached_data:
                data_item = ET.SubElement(attached_data, 'data')
                data_item.text = data
                data_item.set('type', 'local')

        # Clean up and put the ElementTree and XML post in the right places
        self.etree._setroot(post)
        self.postxml = ET.tostring(post)
        

    def doPost(self, url=DEFAULT_URL, uid=DEFAULT_UID):
        """Method for posting the Post object. Returns the post ID.

        doPost checks that required information is present and then
        posts the Post object to the blog. The URL status code is posted
        to self.returned_post_status. XML is not generated until this 
        function is called as this is the first point where the 
        presence of all the required objects is explicitly tested.
        """

        # Check that self.posted is False
        assert self.posted == False

        logging.debug(self.title)
        logging.debug(type(self.title))
        # First check that the required elements are there
        assert self.title != None and type(self.title) == str
        assert self.username != None and type (self.title) == str
        assert self.blog_id or self.blog_sname != None
        assert self.content != None and type(self.content) == str
        assert self.section != None and type(self.section) == str
            
        # Serialize the post to generate etree and XML string
        self.serialize()

        # Set up the Request object
        requesturl = url + '/api/rest/addpost/uid/' + uid
        request = urllib.urlencode({'request':self.postxml})
        logging.debug(request)
        post = urllib2.Request(requesturl, data=request)

        response = urllib2.urlopen(post)
               
        # Parse the response and get the status code
        parsedresponse = ET.parse(response)
        statuscode = parsedresponse.find('status_code').text
        success = parsedresponse.find('success').text
        self.post_status_code = statuscode
        self.post_response = response.read(100)

        # If statuscode is ok then return the data ID
        if success == 'true' and statuscode == '200':
            self.posted = True
            self.post_id = parsedresponse.find('post_id').text
            self.url_xml = parsedresponse.find('post_info').text
            self.url = self.url_xml[0:-3] + 'html'
            

            return self.post_id

        else:
            return None

class MultiDataFileUpload(object):
    """Class for creating multiple posts with single attached files"""

    def __init__(self, filelist = [], postnames = None, posttext = None,
                       metadata = None, server_url = None, blog_id = None,
                       username = None, section = None, uid = None,
                       blog_sname = None, usefilename = False):
        self.filelist = filelist
        self.postnames = postnames
        self.posttext = posttext
        self.metadata = metadata
        self.server_url = server_url
        self.blog_id = blog_id
        self.username = username
        self.section = ''
        self.uid = uid
        self.blog_sname = blog_sname
        self.usefilename = usefilename

    def addFile(self, path):
        """Add paths to the list of files for upload"""

        # Test that path exists and points at a file
        try:            
            assert os.path.exists(path), 'Path not found'
            assert os.path.isfile(path), 'Path not pointing at a file'

        except AssertionError, e:
            return str(e)

        # Append path to file to list
        self.filelist.append(path)

    def setPostNames(self, name):
        assert type(name) == str, 'Name must be a string'
        assert name != '', 'Must have a name'

        self.postnames = name

    def setPostText(self, text):
        assert type(text) == str, 'Post text must be a string'
        assert text != '', 'Must have some post text'

        self.posttext = text

    def doUpload(self):
        """Upload method for multiple posts with single files attached"""

        # Check for presence of required elements
        try:
            assert self.filelist != [], 'Filelist is empty'
            assert self.postnames or self.usefilename, \
                                      'No name given for post title'
            
        except AssertionError, e:
            return str(e)  

        # Sort the list into alphabetical/numeric order by filename
        self.filelist.sort()

        # Set up tracking variables for sequential upload
        i = 1
        data_fail = 0
        post_fail = 0

        # For each path in the filelist
        for path in self.filelist:
            data = LaBLogData() # Build data object
            data.set_type('inline')
            data.set_data(path)

            # Attempt to do the data object post
            if data.doPost(url = self.server_url, uid = self.uid) == None:
                data_fail = data_fail + 1

            # Only build and do the post if the data post succeeds
            else:
                # Build the post object
                post = LaBLogPost()
                
                # Set up the post name for the data post
                # If self.usefilename is set to True then get the filename
                if self.usefilename:
                    post.set_title = os.path.basename(path)
                # Otherwise use the postname that is set plus increment
                elif self.usefilename == False:
                    post.set_title(self.postnames + ' ' + str(i))

                post.set_username(self.username)
                post.set_section(self.section)
                post.set_content(self.posttext)
                if self.blog_id:
                    post.set_blog_id(self.blog_id)
                if self.blog_sname:
                    post.set_blog_sname(self.blog_sname)
                if self.metadata:
                    post.set_metadata(self.metadata)
                post.set_attached_data([data.data_id])
                i = i + 1

                # Attempt to do the blog post
                if post.doPost(url = self.server_url, uid = self.uid) == None:
                    post_fail = postfail + 1

                else:
                    pass
               
        return data_fail, post_fail, len(self.filelist)
                
                
                
class BlogTable(object):
    """A convenience class for creating and serializing tables for the blog

    The basic data model is a simple array (list of lists). Tables are 
    assumed to be ordered vertically so that additional samples/entires are 
    added by creating a new row.
    """

    def __init__(self, input = None):
        """Init method can take a set of lists and populate table"""

        self.content = None
        if input and self.checkInput(input):
            self.replaceContent(input)
        
    def checkInput(self, input):
        """Method for checking that input is ok for table creation"""

        # Check input is a list
        if type(input) != list:
            raise TypeError("Need a list for creation of table")
            return False

        # Check number of lists in input and that all rows are the same length
        # but only if the list contains lists
        if type(input[0]) == list:
            check = []
            for row in input:
                check.append(len(row))
                if len(check) > 1 and check[-1] != check[-2]:
                    raise ValueError("Rows are not the same length")
                    return False
        return True

    def replaceContent(self, input):
        """Replace the content of the table with values from input

        If input is a single list (and not a list if lists) then
        put it inside a list before setting the content to it.
        """

        if type(input[0] != list):
            input = [input]
        self.content = input

    def appendRow(self, input):
        if len(input) != self.numberOfColumns():
            raise ValueError("Row has wrong number of columns")
            return False

        self.content.append(input)
        return len(self.content)

    def numberOfRows(self):
        return len(self.content)

    def numberOfColumns(self):
        return len(self.content[0])

    def serialize(self):
        table = "[table]"
        for row in self.content:
            table += "[row]"
            for column in row:
                table += column + "[col]"
            table.rstrip("[col]")
            table += "[/row]\n"
        table += "[/table]\n"
        return table        
        


###############################################
#
# TESTS
#
###############################################

class TestDataObjectCreator(unittest.TestCase):

    def setUp(self):
        self.testemptydataobject = LaBLogData()
        self.title = 'Test title'
        self.faketitle = 'Not the test title'
        self.testint = 1
        self.testfloat = 5.4
        self.testfile = 'ai.gif'
        self.extension = 'gif'
        self.base64 = base64.standard_b64encode(
                                    open('ai.gif').read(3000))
        self.directory = '/Users/Cameron/Documents/Python/LaBLog/Testing/'
        self.fullpath = os.path.join(self.directory, self.testfile)

    def test_init_empty_object(self):
        self.assertTrue(self.testemptydataobject.title == None)
        self.assertTrue(self.testemptydataobject.type == None)
        self.assertEqual(self.testemptydataobject.main, '1')

    def test_set_title(self):
        self.testemptydataobject.set_title(self.title)
        self.assertEqual(self.testemptydataobject.title, self.title)
        self.assertNotEqual(self.testemptydataobject.title, self.faketitle)

    def test_set_title_Exceptions(self):
        self.assertRaises(TypeError, 
                            self.testemptydataobject.set_title, self.testint)
        self.assertRaises(TypeError, 
                            self.testemptydataobject.set_title, self.testfloat)

    def test_set_type_inline(self):
        self.testemptydataobject.set_type('inline')
        self.assertEqual(self.testemptydataobject.type, 'inline')

    def test_set_type_url(self):
        self.testemptydataobject.set_type('url')
        self.assertEqual(self.testemptydataobject.type, 'url')

    def test_set_type_local(self):
        self.testemptydataobject.set_type('local')
        self.assertEqual(self.testemptydataobject.type, 'local')

    def test_set_type_Exceptions(self):
        self.assertRaises(ValueError, 
                            self.testemptydataobject.set_type, self.title)
        self.assertRaises(TypeError, 
                            self.testemptydataobject.set_type, self.testint)
        self.assertRaises(TypeError, 
                            self.testemptydataobject.set_type, self.testfloat)

    def test_set_data_local_path(self):
        self.testemptydataobject.set_data(self.testfile)
        self.assertEqual(self.testemptydataobject.ext, self.extension)
        self.assertEqual(self.testemptydataobject.data, self.base64)
        self.assertEqual(self.testemptydataobject.title, 'ai')

    def test_set_data_full_path(self):
        self.testemptydataobject.set_data(self.fullpath)
        self.assertEqual(self.testemptydataobject.ext, self.extension)
        self.assertEqual(self.testemptydataobject.data, self.base64)

    def test_set_data_file_and_path(self):
        self.testemptydataobject.set_data(self.testfile, self.directory)
        self.assertEqual(self.testemptydataobject.ext, self.extension)
        self.assertEqual(self.testemptydataobject.data, self.base64)

    def test_set_data_no_filename(self):
        self.testemptydataobject.set_data(self.testfile, usefilename=False)
        self.assertEqual(self.testemptydataobject.title, None)

class TestDataPoster(unittest.TestCase):
    def setUp(self):
        self.testemptydataobject = LaBLogData()
        self.title = 'Test title'
        self.faketitle = 'Not the test title'
        self.testint = 1
        self.testfloat = 5.4
        self.testfile = 'ai.gif'
        self.extension = 'gif'
        self.base64 = base64.standard_b64encode(
                                    open('ai.gif').read(3000))
        self.directory = '/Users/Cameron/Documents/Python/LaBLog/Testing/'
        self.fullpath = os.path.join(self.directory, self.testfile)

    def testInlineDataPost(self):
        testdataobject = LaBLogData()
        testdataobject.set_title(self.title)
        testdataobject.set_type('inline')
        testdataobject.set_data(self.testfile)

        testdataobject.doPost()
        self.assertEqual(testdataobject.posted, True)
        self.assertEqual(testdataobject.post_status_code, '200')

class TestPostObjectCreator(unittest.TestCase):
    def setUp(self):
        self.testemptypostobject = LaBLogPost()
        self.title = 'Test title'
        self.faketitle = 'Not the test title'
        self.testint = 1
        self.testfloat = 10.6
        self.testusername = DEFAULT_USERNAME
        self.testblog_id = '16'
        self.testcontent = 'Blah blah blah'
        self.testblog_sname = 'testing_sandpit'
        self.testmetadata = {'key1':'value1', 'key2':'value2'}

    def test_init_empty_post(self):
        self.assertTrue(self.testemptypostobject.title == None)
        self.assertTrue(self.testemptypostobject.username == None)
        self.assertTrue(self.testemptypostobject.blog_id == None)
        
    def test_set_title(self):
        self.testemptypostobject.set_title(self.title)
        self.assertEqual(self.testemptypostobject.title, self.title)
        self.assertNotEqual(self.testemptypostobject.title, self.faketitle)

    def test_set_title_Exceptions(self):
        self.assertRaises(TypeError, 
                            self.testemptypostobject.set_title, self.testint)
        self.assertRaises(TypeError, 
                            self.testemptypostobject.set_title, self.testfloat)

    def test_set_metadata(self):
        self.testemptypostobject.set_metadata(self.testmetadata)
        self.assertEqual(self.testemptypostobject.metadata, self.testmetadata)

    def test_append_metadata(self):
        self.testemptypostobject.append_metadata(self.testmetadata)
        self.assertEqual(self.testemptypostobject.metadata, self.testmetadata)

        # Now try and add metadata again and should raise ValueError
        self.assertRaises(ValueError, 
                          self.testemptypostobject.append_metadata, {'key1':'value3'})

        # But the following should succeed using overwrite=True option
        self.testemptypostobject.append_metadata({'key1':'value3'}, overwrite = True)
        self.assertEqual(self.testemptypostobject.metadata, {'key1':'value3',
                                                             'key2':'value2'})


class TestXMLSerializors(unittest.TestCase):

    def setUp(self):
        self.testpost = LaBLogPost()
        self.testpost.title = 'title'
        self.testpost.username = DEFAULT_USERNAME
        self.testpost.section = 'API testing'
        self.testpost.content = 'test text content'
        self.testpost.blog_id = '16'
        self.testpost.blog_sname =  'testing_sandpit'
        self.testpost.metadata = {'key1':'value1',
                                  'key2':'value2',
                                  'key3':'value3'}
        self.testpost.attached_data = ['1', '2', '3']

        self.testxml = """<post><title>title</title><section>API testing</section><author><username>cameronneylon.net</username></author><content>test text content</content><blog_id>16</blog_id><blog_sname>testing_sandpit</blog_sname><metadata><key3>value3</key3><key2>value2</key2><key1>value1</key1></metadata><attached_data><data type="local">1</data><data type="local">2</data><data type="local">3</data></attached_data></post>""" 

        f = open('ai.gif')
        testbinary = f.read(3000)
        testbase64 = base64.standard_b64encode(testbinary)

        self.testdata = LaBLogData()
        self.testdata.title = 'title'
        self.testdata.type = 'inline'
        self.testdata.filename = 'filename.gif'
        self.testdata.ext = 'gif'
        self.testdata.main = '1'
        self.testdata.data =  testbase64

        self.testdataxml1 = """<dataset><title>title</title><data><dataitem ext="gif" filename="filename.gif" main="1" type="inline">R0lGODlhIAAgAOZmAP/elM6MY8Z7CEIxGOeUWv/OjHtKObVjENalUv/OY8aEMd57AP/vrTkhEOeMEKVrGNaUOeeMAK1jQmM5CM6EGL1rAJRSQpxaAIxjUlI5MbVzWq2lrd6UKe+lMeecGIRSEBAIAKWUjJx7Y71zGOecc7WtnHu11nNzezE5OSkYCJTG3tbGnM57Uv/erb21rUpKSsatpWtCMfeMECEICFpKQpyMe1JaWr2ljK2clKVrAIwICM7e50Jja73O1pR7c4RrQtaUlM6lc3taStbOxsa1tYyUnMbW3rWEc961pa17Ka21vfe9hEIpQhgYGHNjWs7GzqVjUoyMlN4pKSEYIXOMtWtSSs6tjP+1Ob21vYycrSkpKf+tKVIpGLVzSq1KMfe1c5RrMf+9UmsxIcZrOYRCKQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAGYALAAAAAAgACAAAAf/gGaCg4SFhoeIiYqEAQQri5CCLYJdCgoBkSEGYGBdAZ+EX2ZBYwSdj4kbGWJkXl5jCh0dCg+dYGRkY7pgN4IFX8DAYA0GZGLHZAdeD69jyrgHugShHRDWMWIDxwMDXBNc3dsTYhO4EwoIhGEcJiZCyAZiGZxcKTNczWBeuGJeCqiCwkAwEUXHh3JduhAIwwDBGDEzBuTS9QBXrUJfBhrIgWtMpYUAGDBIAAZEAy5cWEGDQGKSoC8cflz40E/XxzAhRcYo04BbMQMHwCxRR+HCBInNEi4UGTLBgAYqXR0AUSjMAhsoO8JSSCAAgi8hJZjkwm9CiqocuOgoN9FjFy9e/78CSGAgBatSB8pUFcDlgzZcubogCIOADBgJAQAgOAnmgYwOegkhqDCGjJZjmMeESUBmAAqvBRJkI/Ogw4LIgwgIYGGBSQZ+3QgACCCBBdhfw8REc4Ba0GROBl57jjcmAYDQBY5/8dLg1YEIvc0goHDCwI8xYAwYkNAvgXfvv76UzLXgdCEIFKhgwCAhgxdOrMKEWQhMfhcQZMtHh5AkiwgNVaCwiRdicEHAW2HUN58BTQxwgXmEQDCCFUeIgMEL82QHjhchhVZfFw1M8YEA0SkggAslBKABBjQIYUF2YiSEQAAkHBdGF0/lQGIhJiKhxCcarGjBiwVeIMUYYH1BgNEXKF1QQYkjPIHFBiGI8B8UFkjgygVjJAfAF12QgQ8FT/I4ggpobuDDCSIEQIMFXXCCAADHHQgGFzeEwVshHIzQQw9U4oBDDSc4wR5iBSSKAAEJ2MBDETLsSUifO+wAQwkluLDBCT58EgALXSSIEwAv8DBGBJIOIkAFQxhBxKVAABFCCEGQQEKCiRbAQA0NfOCFA9AVcoAADzxwwLAUOECBAMl6sMUV8sl3gLEHABtdBQJkK0B5EXTLLaoehOuBA9hmu8COhZSh7rrstutuu4QEAgA7</dataitem></data></dataset>"""

        self.emptydata = LaBLogData()
        self.emptypost = LaBLogPost()
        self.require_for_postxml = ['title', 'section', 'username', 'content']
        self.require_for_dataxml = ['title', 'filename', 'type', 'data']


    def testpostxmlserialization(self):
        self.testpost.serialize()
        self.assertEqual(ET.tostring(self.testpost.etree.getroot()), 
                                          self.testxml)
        self.assertEqual(self.testpost.postxml, self.testxml)

    def testdataxmlserialization(self):
        self.testdata.serialize()
        self.assertEqual(ET.tostring(self.testdata.etree.getroot()), 
                                          self.testdataxml1)
        self.assertEqual(self.testdata.postxml, self.testdataxml1)

    def testxml_empty(self):
        self.assertRaises(AssertionError, self.emptydata.serialize)
        self.assertRaises(AssertionError, self.emptypost.serialize)
        
class TestPostPoster(unittest.TestCase):
    def setUp(self):
        self.testemptypostobject = LaBLogPost()
        self.title = 'Test title'
        self.faketitle = 'Not the test title'
        self.testint = 1
        self.testfloat = 10.6
        self.testsection = 'API testing'
        self.testusername = DEFAULT_USERNAME
        self.testblog_id = '16'
        self.testcontent = 'Blah blah blah'
        self.testblog_sname = 'testing_sandpit'
        self.testmetadata = {'key1':'value1', 'key2':'value2'}


    def testBlogPost(self):
        testpostobject = LaBLogPost()
        testpostobject.set_title(self.title)
        testpostobject.set_username(self.testusername)
        testpostobject.set_section(self.testsection)
        testpostobject.set_blog_id(self.testblog_id)
        testpostobject.set_blog_sname(self.testblog_sname)
        testpostobject.set_content(self.testcontent)

        testpostobject.doPost()
        self.assertEqual(testpostobject.posted, True)
        self.assertEqual(testpostobject.post_status_code, '200')

class TestMultiDataFileUpload(unittest.TestCase):
    def setUp(self):
        self.testfilelist = ['ai.gif', 'ai2.gif']
        self.testfile = 'ai.gif'
        self.testfile2 = 'ai2.gif'
        self.testpostnames = 'test'
        self.testposttext = 'Some new test text'
        self.testmetadata = {'key1':'value1', 'key2':'value2'}
        self.testserver_url = DEFAULT_URL
        self.testblog_id = '17'
        self.testusername = DEFAULT_USERNAME
        self.testblog_sname = 'testing_sandpit'
        self.testsection = ''
        self.testuid = DEFAULT_UID
        self.test = MultiDataFileUpload()

    def tearDown(self):
        self.test.filelist = []
        self.test = None

    def testEmptyMultiCreation(self):
        self.test.addFile(self.testfile)
        self.test.addFile(self.testfile2)
        self.test.setPostNames(self.testpostnames)
        self.test.setPostText(self.testposttext)

        self.assertEqual(self.test.filelist, self.testfilelist)
        self.assertEqual(self.test.postnames, self.testpostnames)
        self.assertEqual(self.test.posttext, self.testposttext)

    def testErrorCatching(self):
        self.assertEqual(self.test.addFile('nonexistentfile'), 'Path not found')
        self.assertRaises(AssertionError, self.test.setPostNames, None)
        self.assertRaises(AssertionError, self.test.setPostNames, 1)
        self.assertRaises(AssertionError, self.test.setPostText, None)
        self.assertRaises(AssertionError, self.test.setPostText, 3)

        self.test.filelist = []
        self.assertEqual(self.test.doUpload(), 'Filelist is empty')
        self.test.addFile(self.testfile)
        self.assertEqual(self.test.doUpload(), 'No name given for post title')

    def testMultiPost(self):
        self.test = MultiDataFileUpload(
                  **{'filelist'   : self.testfilelist,
                     'postnames'  : self.testpostnames,
                     'posttext'   : self.testposttext,
                     'metadata'   : self.testmetadata,
                     'server_url' : self.testserver_url,
                     'blog_id'    : self.testblog_id,
                     'username'   : self.testusername,
                     'section'    : self.testsection,
                     'uid'        : self.testuid,
                     'blog_sname' : self.testblog_sname})

        data_fail, post_fail, length = self.test.doUpload()
        self.assertEqual(data_fail, 0)
        self.assertEqual(post_fail, 0)
        self.assertEqual(length, len(self.testfilelist))


if __name__ == '__main__':
    if set_proxy(False) == False:
        set_proxy(True)

    unittest.main()        
