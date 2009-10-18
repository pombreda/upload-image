'''
    radikal.ru service module
'''

import upimg
import pycurl
import re
import os.path
from optparse import make_option
from gettext import gettext

_ = gettext


ih_imagelink_re = re.compile("<rurl>(.+)</rurl>")
ih_thumblink_re = re.compile("<rurlt>(.+)</rurlt>")
ih_thumblink2_re = re.compile("<rurlx>(.+)</rurlx>")

class RadikalRuService(upimg.servicecore.Uploader):
    
    def _connect(self):
        self.msg(_("Connecting to radikal.ru..."))
        self.head("http://www.radikal.ru")

    def _upload_file(self, filename):
        upimg.servicecore.Uploader._upload_file(self, filename)
        self._curl.setopt(pycurl.USERAGENT, "RADIKALCLIENT")
        self._curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        params = [
            ("image", (pycurl.FORM_FILE, filename)),
            ("upload", "yes"),
            ("object", "clum"),
            ("0", ""), # ""|"yes" change size
            ("M", "640"), # chnage size width
            ("RE", ""), # ""|"yes" rotate
            ("R", ""), # Rotate to angle, clockwise: 0:0, 1:90, 2:180, 3:270
            ("XE", ""),# ""|"yes" label on the image
            ("X", ""), # text of the label
            ("J", ""), # ""|"yes" optimization 
            ("N", ""), # ""|"yes" some other optimization
            ("JQ", "85"), # JPEG quality, 1-100
            ("IM", "7"), # Interpolation: 7:HighQualityBicubic, 6:HighQualityBilinear, 4:Bicubic, 3:Bilinear, 5:NearestNeighbor
            ("CP", "yes"), # unknown
            ("VM", "180"), # preview size
            ("VE", ""), # ""|"yes" label on preview
            ("V", ""), # text of the preview label
            ("FS", ""), # unknown
            ("alb_id", ""), # album id
            ("select_thema", ""), # unknown
            ("input_comment", ""), # comment
            ("user_url", ""), # url 
            ("OPTIMIZATION", "True"), # don't know 
            ("FORCED_OPTIMIZATION", "False"),# don't know
            ("MAX_WIDTH", "640"), 
            ("ROTATION", "0"), 
            ("SIGNATURE", ""),
            ("JPEG_QUALITY", "85"),
            ("INTERPOLATION", "7"),
            ("ORIGINAL_LENGTH", str(os.path.getsize(filename))), # size of the file in bytes
            ("ORIGINAL_WIDTH", "128"), # width 
            ("ORIGINAL_HEIGHT", "128"), # height
            ("ANIMATION", "False"),
            ("COEFF_M", "1"),
            ("OPTIMIZED", "True"),
            ("RESULT_LENGTH", "128"), # don't know
            ("RESULT_WIDTH", "128"),
            ("RESULT_HEIGHT", "128"),
            ("MIMETYPE", "image/jpeg"),
            ("EXTENSION", "jpg"),
            ]
        #self.post("http://localhost:3333/", params)
        self.post("http://www.radikal.ru/FOTODESKTOP/PostImgH.ashx", params)
        data = self._buffer.getvalue()
        ''' # this is comment, response from the server looks like xml below
        data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><images>
        <image><rid>1f431c3893a042ec8ae095cfb2059598</rid>
        <rurl>http://s57.radikal.ru/i157/0903/43/711b94e7abbe.jpg</rurl>
        <rurlt>http://s57.radikal.ru/i157/0903/43/711b94e7abbet.jpg</rurlt>
        <rurlx>http://s57.radikal.ru/i157/0903/43/711b94e7abbex.jpg</rurlx>
        <rcomm></rcomm></image></images>"""
        '''
        mo = ih_imagelink_re.search(data)
        if None != mo:
            direct_url = mo.group(1)

            self.msg(_("Direct URL: %s") % direct_url)
            if self.options.full:
                mo = ih_thumblink_re.search(data)
                if None != mo:
                    thumb_url = mo.group(1)
                    imgd = {
                        'direct_url': direct_url,
                        'thumb_url': thumb_url
                        }

                    self.msg(_("Thumbnail URL: %s") % thumb_url)
                    self.msg(_('HTML link: <a href="%(direct_url)s"><img src="%(thumb_url)s"></a>') % imgd)
                    self.msg(_('Forum link 1: [URL=%(direct_url)s][IMG]%(thumb_url)s[/IMG][/URL]') % imgd)
                    self.msg(_('Forum link 2: [url=%(direct_url)s][img=%(thumb_url)s][/url]') % imgd)
        else:
            self.msg("Server response doesn't contain image URL.")
        #print data

    def _features(self):
        f = {
            'filesize_limit': 10000000, # ~10 mb
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
    "radikal.ru",
    RadikalRuService,
    get_service_options,
    description = "http://radikal.ru free image hosting.",
    service_type = "image-hosting"
    )
