import optparse
from optparse import BadOptionError

class upimgOptionParser(optparse.OptionParser):
    
    __ignore_unknow_args = False
    
    def ignore_unknown_args(self, b):
        self.__ignore_unknow_args = b

    def _process_args(self, largs, rargs, values):
        if self.__ignore_unknow_args:
            try:
                optparse.OptionParser._process_args(self, largs, rargs, values)
            # pay attention! This is a dirty hack to prevent calling sys.exit()
            # this WON'T work in python < 2.5
            # we are caught exception BadOptionError and _process_args will not
            # termiate program
            except BadOptionError:
                pass
        else:
            optparse.OptionParser._process_args(self, largs, rargs, values)

