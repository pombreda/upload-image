'''
    imageshack.us service module
'''

import upimg
import pycurl
import re
from optparse import make_option
from gettext import gettext

_ = gettext


ih_imagelink_re = re.compile("<image_link>(.+)</image_link>")
ih_thumblink_re = re.compile("<thumb_link>(.+)</thumb_link>")
ih_adlink_re = re.compile("<ad_link>(.+)</ad_link>")
ih_resolution_re = re.compile("<resolution>(.+)</resolution>")

class ImageShackService(upimg.servicecore.Uploader):
    
    def _connect(self):
        self.msg(_("Connecting to imageshack.us..."))
        self.head("http://imageshack.us")

    def _upload_file(self, filename):
        upimg.servicecore.Uploader._upload_file(self, filename)
        self._curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        params = [
            ('fileupload', (pycurl.FORM_FILE, filename)),
            ('xml', "yes")
            ]
        self.post("http://imageshack.us/", params)
        data = self._buffer.getvalue()
        ''' # this is comment, response from the server looks like xml below
        data = """<?xml version="1.0" encoding="iso-8859-1"?><links>
    <image_link>http://img209.imageshack.us/img209/6697/nationvigr2.jpg</image_link>
    <thumb_link>http://img209.imageshack.us/img209/6697/nationvigr2.th.jpg</thumb_link>
    <ad_link>http://img209.imageshack.us/my.php?image=nationvigr2.jpg</ad_link>
    <thumb_exists>yes</thumb_exists>
    <total_raters>0</total_raters>
    <ave_rating>0.0</ave_rating>
    <image_location>img209/6697/nationvigr2.jpg</image_location>
    <thumb_location>img209/6697/nationvigr2.th.jpg</thumb_location>
    <server>img209</server>
    <image_name>nationvigr2.jpg</image_name>
    <done_page>http://img209.imageshack.us/content.php?page=done&amp;l=img209/6697/nationvigr2.jpg</done_page>
    <resolution>800x648</resolution>
    <filesize>215331</filesize>
    <image_class>r</image_class>
    </links>"""
        '''
        mo = ih_imagelink_re.search(data)
        if None != mo:
            direct_url = mo.group(1)

            mo = ih_adlink_re.search(data)
            if None != mo:
                img_page_url = mo.group(1)
            else: 
                img_page_url = direct_url

            self.msg(_("Direct URL: %s") % direct_url)
            if self.options.full:
                mo = ih_thumblink_re.search(data)
                if None != mo:
                    thumb_url = mo.group(1)
                    imgd = {
                        'img_page_url': img_page_url,
                        'thumb_url': thumb_url
                        }

                    self.msg(_("Thumbnail URL: %s") % thumb_url)
                    self.msg(_('HTML link: <a href="%(img_page_url)s"><img src="%(thumb_url)s"></a>') % imgd)
                    self.msg(_('Forum link 1: [URL=%(img_page_url)s][IMG]%(thumb_url)s[/IMG][/URL]') % imgd)
                    self.msg(_('Forum link 2: [url=%(img_page_url)s][img=%(thumb_url)s][/url]') % imgd)
        else:
            self.msg("Server response doesn't contain image URL.")
            self.msg("Response: %s" % data)
        #print data

    def _features(self):
        f = {
            'filesize_limit': 1500000, # 1.5 mb
            }
        return f

def get_service_options():
    options = []
    options.append(make_option("-f", "--full", 
        action="store_true", dest="full",
        help="Show BB and HTML links in the output along with a direct url")
        )
    return options

upimg.register_service(
    "imageshack.us",
    ImageShackService,
    get_service_options,
    description = "http://imageshack.us free image hosting.",
    service_type = "image-hosting"
    )
