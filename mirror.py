#!/usr/bin/env python
import logging
import logging.handlers
import sys
import yaml
from optparse        import OptionParser
from helpers.git_ops import *


def initialize_logger(debug):
    # specify the logging format
    level      = "DEBUG" if debug else "INFO"
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"

    # set up default logging settings
    logging.basicConfig(level=level, format=log_format)
    formatter = logging.Formatter(log_format)

    # create log file output
    file_handler = logging.handlers.RotatingFileHandler("{}/{}.log".format("logs", "run"), maxBytes=20971520, backupCount=10)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_handler)

def main():
    # get command line arguments for testing
    opt_parser = OptionParser()
    opt_parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="verbose logging and debugging")
    (opts, args) = opt_parser.parse_args()

    # initialize the logger
    initialize_logger(opts.debug)
    
    try:
        # get configurations
        # add try catch
        f = open("config/settings.yml")
        config = yaml.safe_load(f)
        f.close()
        # start migrating repos
        for repodata in config["source_stash"]["repos_to_migrate"]: 
            	# create a new empty repo on the destination github project
            	create_repo(base_url=config["destination_github"]["api_url"],
            				org_name=config["destination_github"]["org"],
            				access_token=config["destination_github"]["access_token"],
            				repo_name=repodata,
            				timeout=config["destination_github"]["timeout"])
            	# mirror the source project to destination
            	mirror_repo(src_base_url=config["source_stash"]["url"],
            				src_project=config["source_stash"]["project"],
            				dest_base_url=config["destination_github"]["url"],
            				dest_org=config["destination_github"]["org"],
            				access_token=config["destination_github"]["access_token"],
            				repo_name=repodata, 
            				tmp_dir=config["work_dir"])
    except Exception, e:
        logging.fatal("{}".format(e))


# main entry point
if __name__ == "__main__":
    main()