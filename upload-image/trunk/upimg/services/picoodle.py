'''
    imageshack.us service module
'''

import upimg
import pycurl
import re
from optparse import make_option
from gettext import gettext

_ = gettext

re_upload_server = re.compile('action="(http://img[0-9]{2}\.picoodle\.com/upload\.php)"')
re_stage1_url = re.compile('<form action="http://www\.picoodle\.com/getcode\.php\?url=(.+)\&pwidget=\&callback=\&mode=" method=POST name=continueform>')

class PicoodleService(upimg.servicecore.Uploader):
    
    __upload_server = None

    def header_callback(self, buf):
        print buf, ">>"

    def _connect(self):
        # connect and retrieve upload server name
        self.msg(_("Connecting to picoodle.com..."))
        self.get("http://www.picoodle.com/")
        data = self._buffer.getvalue()
        mo = re_upload_server.search(data)
        if mo:
            url = mo.group(1)
            self.__upload_server = url
        else:
            raise upimg.servicecore.ConnectFailed("Server returned HTML that doesn't contain correct upload server name.")

    def _upload_file(self, filename):
        self.msg("")
        self.msg("Uploading image file `%s' ... " % filename, True)
        #self._curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        #self._curl.setopt(pycurl.HEADERFUNCTION, self.header_callback)
        params = [
            ('pic', (pycurl.FORM_FILE, filename)),
            ('op', 'upload')
            ]
        
        self.post(self.__upload_server, params)
        data = self._buffer.getvalue()
        mo = re_stage1_url.search(data)
        if mo:
            self.msg("")
            self.msg(_("Direct URL: http://%s") % (mo.group(1)) )
        else:
            raise upimg.servicecore.RequestFailed("Returned web page doesn't contain correct link to uploading results.")

    def _features(self):
        f = {
            'filesize_limit': 2000000, # 2.0 mb
            }
        return f

def get_service_options():
    options = []
    """
    options.append(make_option("-f", "--full", 
        action="store_true", dest="show_full",
        help="Show BB and HTML links in the output along with a direct url")
        )
    """
    return options

upimg.register_service(
    "picoodle",
    PicoodleService,
    get_service_options,
    description = "http://www.picoodle.com/ free image hosting.",
    service_type = "image-hosting"
    )
