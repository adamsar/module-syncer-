"""
Files for Fabric interacting with the server
"""

from fabric.api import *
import ConfigParser
import time

CMS_SCRIPT = """
sudo sh -c "printf 'login \"Admin\" \"admin\"\n' > script.cms"
sudo sh -c "printf 'setCurrentProject \"Offline\"\n' >> script.cms"
sudo sh -c "printf 'publishProjectAndWait\n' >> script.cms"
sudo sh -c "printf 'exit' >> script.cms"
sudo sh cmsshell.sh -script=script.cms
sudo rm script.cms
"""


def bootstrap(config, section):
    """Bootstraps the environment. Can only be run once"""
    if not env.get("bootstrapped"):
        env.parser = ConfigParser.RawConfigParser(allow_no_value=True)
        env.parser.readfp(open(config))
        env.hosts.extend([env.parser.get(section, "remote_server")])
        env.host = env.parser.get(section, "remote_server")
        env.user = env.parser.get(section, "remote_user")
        env.key_filename = [env.parser.get(section, "remote_key")]
        env["bootstrapped"] = True


def sync(config, section):
    """Synchronizes fileson the remote server"""
    local("bin/python syncer.py %s %s" % (section, config))


def publish(config, section):
    """Remote publishes all files on file system"""
    bootstrap(config, section)
    server = env.parser.get(section, "remote_dir").rstrip("/")
    with cd("%s/webapps/ROOT/WEB-INF" % server):
        run(CMS_SCRIPT)
    

@hosts(["devandy2.ubicast.com"])            
def restart_server(config, section):
    """Restarts a remote server, require a config and a section"""
    bootstrap(config, section)
    sync(config, section)
    publish(config, section)
    server = env.parser.get(section, "remote_dir").rstrip("/")
    with cd(server):
        run("sudo sh shutdown.sh")
        time.sleep(5)
        run("ps aux | grep %s | grep -v grep| awk {'print $2'} | sudo xargs kill" %
            server)
        run("sudo sh startup.sh")
        
    
