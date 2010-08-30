# makefile that prepares files for debian package and also some other useful things
#

APP_NAME=upload-image
VERSION=0.4
SOURCE_ROOT=../upload-image/trunk/
DEB_BUILD_ROOT=./deb-build
DEB_SPEC=../debian

default:
#default empty action
	@echo available targets:
	@echo 'make deb', 'make deb-clean'

deb: deb-dir
	cd $(DEB_BUILD_ROOT)/$(APP_NAME)-$(VERSION) && dpkg-buildpackage -rfakeroot

deb-dir: deb-clean sdist
#	create debian build tree
	mkdir $(DEB_BUILD_ROOT)
#	cp -r $(SOURCE_ROOT) $(DEB_BUILD_ROOT)/$(APP_NAME)-$(VERSION)
	cp $(SOURCE_ROOT)/dist/upload-image-$(VERSION).tar.gz $(DEB_BUILD_ROOT)/$(APP_NAME)_$(VERSION).orig.tar.gz
	cd $(DEB_BUILD_ROOT) && tar xf $(APP_NAME)_$(VERSION).orig.tar.gz
	cp -r $(DEB_SPEC) $(DEB_BUILD_ROOT)/$(APP_NAME)-$(VERSION)/debian
	cd $(DEB_BUILD_ROOT) && find . -name .svn -type d | xargs rm -rf

sdist:
	cd $(SOURCE_ROOT) && python setup.py sdist

deb-clean:
	# do clean debian build tree
	rm -rf $(DEB_BUILD_ROOT)
