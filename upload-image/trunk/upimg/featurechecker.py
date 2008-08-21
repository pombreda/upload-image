# vim: expandtab sw=4 ts=4 :

__author__ = "Sergei Stolyarov"
__email__ = "sergei@regolit.com"

import sys
import os
import stat
import gettext

_ = gettext.gettext

supported_features = ("filesize_limit")#, "supported_formats", "max_img_width", "max_img_height")

# throw when feature is unknown
class UnknownFeature(Exception):
    pass

class NotConform(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
    pass

def check_feature(feature_name, feature_data, filename):
    '''
        Check that given file conform given feature. If doesn't function 
        will throw an exception.
    '''
    if not feature_name in supported_features:
        raise UnknownFeature()
    function_name = "checker_%s" % feature_name
    function = globals()[function_name]
    function(feature_data, filename)

def checker_filesize_limit(data, filename):
    filesize = os.stat(filename)[stat.ST_SIZE]
    if data < filesize:
        raise NotConform(_("file `%s' is too large, it should be less than %d bytes") % (filename, data) )
        

