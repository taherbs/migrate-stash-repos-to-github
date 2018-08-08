# Migrate Stash Repos to Github

The job will migrate atlassian stash repos to github org repos.

## Getting Started

### Prerequisites

Much of the configuration in this project is set up to use Python environment and installation
helpers. As such, the following tools are expected to be installed on the system that will be
developing/running the application:

- easy_install
- pip
- virtualenv
- git

Run the following command to install all the prerequisites:

```bash
sudo apt-get update && sudo apt-get install -y python-pip python-dev python-setuptools build-essential git
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
```

### Set-up and run

Un-pack the compressed package and/or clone from Git. Once complete, create/activate the
virtualenv environment to contain all required libraries, and install the dependent libraries:

```bash
# Prepare
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Configuration

Once installation has completed, you must configure the software for your environment. The
configurations are all contained within the config/settings.yml file. To create this file,
first copy the sample file to the environment-specific file. It is also best practice to lock
down the file to be readable/wriateable only by administrators/root because this file can and
likely will contain password information:

```bash
cp config/settings.yml.sample config/settings.yml
chmod 600 config/settings.yml
chown root config/settings.yml
# now, edit the file and specify any/all configuration settings for your environment
```

### Running

Now that the configurations are in place, you can run the job manually using the following
command structure:

```bash
./mirror.py
```
