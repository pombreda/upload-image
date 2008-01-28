# vim: expandtab sw=4 ts=4 :

__author__ = "Sergei Stolyarov"
__email__ = "sergei@regolit.com"
__version__ = "0.1"

import os
import servicecore

# list of all available services
upload_services = {}

def list_services():
    return upload_services.keys()

def get_service_desc(name):
    return upload_services[name]["description"]

def get_service_options(name):
    service_options = upload_services[name]["service_options"]()
    return service_options

# registration operation, should be used in specific service module

def register_service(
        name,
        handler, # handler class
        service_options, # function that returns list of service options
        options = None, # list of additional Option objects
        description = None,
        service_type = None,
        ):
    upload_services[name] = {
        'handler': handler,
    }
    upload_services[name]["description"] = description
    upload_services[name]["options"] = options
    upload_services[name]["service_options"] = service_options

def upload_files(options, files):
    service_name = options.service_name
    service = upload_services[service_name]["handler"](options=options)

    service.upload(files)

# register all services
services_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "./services"
        )
    )

for filename in os.listdir(services_dir):
    service_name, ext = os.path.splitext(filename)
    if ext == '.py' and service_name != '__init__':
        __import__("upimg.services.%s" % service_name)
