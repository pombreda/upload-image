import upimg
import os

from distutils.core import setup
setup(name="upload-image",
        version=upimg.__version__,
        description="A simple utility for uploading images to image hostings",
        long_description="",
        author=upimg.__author__,
        author_email=upimg.__email__,
        maintainer="Sergei Stolyarov",
        maintainer_email="sergei@regolit.com",
        platforms=["Linux"],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python',
            'Topic :: Utilities'
            ],
        keywords=["image", "photo", "upload"],
        url="",
        download_url="",
        license="GPL v.2",
        packages=["upimg", "upimg.services"],
        scripts=["upload-image"],
        data_files=[
            (os.path.join('share','man','man1'), ["upload-image.1"])
            ]
      )
