'''
Base interface for all service classes.

Contains methods for communications with server using HTTP protocol.
'''

__author__ = "Sergei Stolyarov"
__email__ = "sergei@regolit.com"

import sys
import os
import pycurl
import StringIO
import upimg
import gettext
import logging
from featurechecker import check_feature
from upimg.progressbar import FileTransferSpeed
from upimg.progressbar import ProgressBar
from upimg.progressbar import Percentage
from upimg.progressbar import Bar
from upimg.progressbar import ETA

_ = gettext.gettext

# exception to simulate abstract methods
class NotImplemented(Exception):
    pass

class ConnectFailed(Exception):
    pass

class RequestFailed(Exception):
    pass

class Uploader:
    def __init__(self, debug = False, options = None):

        self.debug = debug
        self.options = options
        self.connected = False
        self._curl = pycurl.Curl()
        self._buffer = StringIO.StringIO()
        # Write output to string buffer
        self._curl.setopt(pycurl.WRITEFUNCTION, self._buffer.write)
        # We need to follow redirects
        self._curl.setopt(pycurl.FOLLOWLOCATION, 1)
        # We need cookies support, but we don't have to store them
        self._curl.setopt(pycurl.COOKIEFILE, "")
        # Set User-Agent string
        self._curl.setopt(pycurl.USERAGENT, "PyImageUploader/%s (en)" % upimg.__version__)

        # progressbar 
        self._widgets = [FileTransferSpeed(), ' [', Bar(), '] ', Percentage(),' ', ETA()]

    def _curl_upload_progress_callback(self, download_t, download_d, upload_t, upload_d):
        #print "Total to download", download_t
        #print "Total downloaded", download_d
        #print "Total to upload", upload_t
        #print "Total uploaded", upload_d
        # draw progressbar
        #complete_part = int(round(100 * upload_d / upload_t))
        logging.debug("uploaded: %s, to upload: %s" % (upload_d, upload_t))
        if upload_t == 0:
            return
        
        self._progressbar.maxval = upload_t
        self._progressbar.update(upload_d)

    def do_request(self):
        # Cleanup buffer at start
        self._buffer.truncate(0)
        # Do the request
        self._curl.perform()
        # Debugging
        if self.debug:
            self.dump_request()
    
    def dump_request():
        '''
        Dump request data
        '''
        pass

    def get(self, url):
        self._curl.setopt(pycurl.URL, url)
        self.do_request()

    def head(self, url):
        self._curl.setopt(pycurl.URL, url)
        self._curl.setopt(pycurl.NOBODY, True)
        self.do_request()

    def post(self, url, params = None):
        self._curl.setopt(pycurl.URL, url)
        self._curl.setopt(pycurl.NOPROGRESS, 0)
        self._curl.setopt(pycurl.PROGRESSFUNCTION, self._curl_upload_progress_callback)
        if params is None:
            params = []
        self._curl.setopt(pycurl.HTTPPOST, params)
        # start progress bar
        self._progressbar = ProgressBar(widgets=self._widgets)
        self._progressbar.start()
        self.do_request()
        self._progressbar.finish()
        self._progressbar = None
    
    # perform actual connect
    def _connect(self):
        raise NotImplemented()

    def connect(self):
        if not self.connected:
            self._connect()

    # prints given text to user (actually wrapper over print())
    def msg(self, text, noeol = False):
        if noeol:
            print text,
        else:
            print text
        sys.stdout.flush()

    # perform actual upload
    def _upload_file(self, filename):
        self.msg("")
        self.msg("Uploading file `%s'" % filename)

    def upload(self, images):
        # queue, will contain those files only that have passed checks
        images_queue = []

        for img in images:
            # check that file conform to service requirements
            features = self._features()
            try:
                for f in features.keys():
                    check_feature(f, features[f], img)
                images_queue.append(img)
            except OSError:
                self.msg(_("File `%s' not found.") % img)
            except upimg.featurechecker.NotConform, (value):
                self.msg(_("Check failed: %s") % str(value))

        if 0 == len(images_queue):
            self.msg("No images in queue")
            return

        self.connect()
        for img in images:
            self._upload_file(img)


    # subclass should redefine this method to return additional 
    # command line options specs
    def _options(self):
        raise NotImplemented()

    def options(self):
        opts = self._options()
        return opts

    # subclass should redefine this method to return supported 
    # features list, the return value is dictionary: {"feature_name": feature_desc}
    # list of possible key names: 
    def _features(self):
        raise NotImplemented()


# register

