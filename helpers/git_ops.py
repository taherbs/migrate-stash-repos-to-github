import os
import logging
import requests
import json
import subprocess
import re
import shutil

def mirror_repo(src_base_url, src_project, dest_base_url, dest_org, access_token, repo_name, tmp_dir):
    '''Mirror clone then mirror push repos from source repo to destination repo'''
    try:
        # clean the env before proceeding
        clean_cmd = "rm -rf {}/{}".format(tmp_dir, repo_name)
        subprocess.check_call(clean_cmd, shell=True)
        # clone repo
        clone_cmd = "git clone --mirror {0}/scm/{1}/{2}.git {3}/{2}".format(src_base_url, src_project, repo_name, tmp_dir)
        subprocess.check_call(clone_cmd, shell=True)
        logging.info("[{}] successfuly cloned from source {}".format(repo_name, src_base_url))
        # update origin
        update_org_cmd = "cd {3}/{2} && git remote set-url origin {0}/{1}/{2}".format(dest_base_url, dest_org, repo_name, tmp_dir)
        subprocess.check_call(update_org_cmd, shell=True)
        logging.info("[{}] successfuly updated repo origin".format(repo_name))       
        # push repo
        push_cmd  = "cd {3}/{2} && git push --mirror {0}/{1}/{2}.git".format(dest_base_url, dest_org, repo_name, tmp_dir)
        auth_push_cmd = re.sub(r"://", "://{}:x-oauth-basic@".format(access_token), push_cmd)
        subprocess.check_call(auth_push_cmd, shell=True)
        logging.info("[{}] successfuly pushed to destination {}".format(repo_name, dest_base_url))
        # clean Workspace
        subprocess.check_call(clean_cmd, shell=True)
        logging.info("Workspace cleaned")
    except Exception, e:
        raise Exception(e)

def create_repo(base_url, org_name, access_token, repo_name, timeout):
        '''Create a new empty repository'''
        try:
            git_url  = "{}/orgs/{}/repos".format(base_url, org_name)
            headers  = {'Content-type': 'application/json', 
                        'Authorization': 'token {}'.format(access_token)}
            response = requests.post(git_url,
                                     headers=headers,
                                     timeout=timeout,
                                     json={ "name":        repo_name,
                                            "description": "repo auto-created by atlas infra migration scripts",
                                            "private":     False
                                     })
            response_data = response.json()
            # check for errors
            if response.status_code != 201:
                error = "Repository [{}] creation failed under [{}] org\n - Error:\n {}".format(repo_name, org_name, response_data)
                raise Exception(error)
            # print success message
            logging.info("[{}] successfuly created under [{}] org".format(repo_name, org_name))
        except Exception, e:
            raise Exception(e)

