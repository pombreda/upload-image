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

    # override _add_help_option method, it required to force upimgOptionParser not to exit
    # when --help/-h option is specified, so option "--help" must be added implicitly
    def _add_help_option(self):
        pass

    def format_option_help(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        formatter.store_option_strings(self)
        result = []
        #result.append(formatter.format_heading(_("Options")))
        formatter.indent()
        if self.option_list:
            result.append(optparse.OptionContainer.format_option_help(self, formatter))
            result.append("\n")
        for group in self.option_groups:
            result.append(group.format_help(formatter))
            result.append("\n")
        formatter.dedent()
        # Drop the last "\n", or the header if no options or option groups:
        return "".join(result[:-1])

class upimgOptionGroup(optparse.OptionGroup):
    pass
