"""
Files for Fabric interacting with the server
"""

from fabric.api import *
from fabric.contrib.files import exists
import ConfigParser
import time

CMS_SCRIPT = """
sudo sh -c "printf 'login \"Admin\" \"admin\"\n' > script.cms"
sudo sh -c "printf 'setCurrentProject \"Offline\"\n' >> script.cms"
sudo sh -c "printf 'publishProjectAndWait\n' >> script.cms"
sudo sh -c "printf 'clearCaches\n' >> script.cms"
sudo sh -c "printf 'exit' >> script.cms"
sudo sh cmsshell.sh -script=script.cms
sudo rm script.cms
"""

env.roledefs ={
    'dev': ['localhost'],
    'stage': ['ec2-54-249-194-79.ap-northeast-1.compute.amazonaws.com'],
    'devaoki': ['devaoki2.ubicast.com'],
    'ikumi': ['54.248.215.164']
    }


def bootstrap(config, section):
    """Bootstraps the environment. Can only be run once"""
    if not env.get("bootstrapped"):
        env.parser = ConfigParser.RawConfigParser(allow_no_value=True)
        env.parser.readfp(open(config))
        try:
            env.user = env.parser.get(section, "remote_user")            
            env.key_filename = [env.parser.get(section, "remote_key")]
        except ConfigParser.NoOptionError:
            print "Not using EC2 pem"
            
        #Set an env var to denote that the system has indeed been bootstrapped.
        env["bootstrapped"] = True


def sync(config, section):
    """Synchronizes files to a remote server"""
    def do_sync(attempt=3):
        if attempt > 0:
            try:
                local("bin/python syncer.py %s %s" % (section, config))
            except:
                time.sleep(2)
                do_sync(attempt - 1)
        else:
            raise RuntimeError()
    do_sync()


def publish(config, section):
    """Remote publishes all files on file system"""
    bootstrap(config, section)
    server = env.parser.get(section, "remote_dir").rstrip("/")
    servlet = env.parser.get(section, "remote_servlet")
    with cd("%s/webapps/%s/WEB-INF" % (server, servlet)):
        try:
            run(CMS_SCRIPT, timeout = 5 * 60)
        except:
            pass


def restart_server(config, section):
    """Restarts the specified install on the server"""
    bootstrap(config, section)
    use_service = False
    try:
        use_service = bool(env.parser.get(section, "use_service"))
    except:
        pass
    if use_service:
        sudo("service tomcat6 restart")
        return
    server = env.parser.get(section, "remote_dir").rstrip("/")
    with cd(server):
        if exists("bin"):
            sudo("sh bin/shutdown.sh")
        else:
            sudo("sh shutdown.sh")
        time.sleep(10)
        with settings(warn_only=True):
            if run("ps aux| grep %s | grep -v grep" % server):
                sudo("ps aux | grep %s | grep -v grep | awk {'print $2'}| sudo xargs kill -s kill" % server)

        if exists("bin"):
            sudo("sh bin/startup.sh", pty=False)
        else:
            sudo("sh startup.sh", pty=False)
        counts = 0
        test = ""
        while True:
            with settings(warn_only=True):
                test = run("ps aux | grep %s | grep -v grep" % server)
            if not test:
                print "Not found, sleeping and trying again in 10 seconds"
                time.sleep(10)
                if exists("bin"):
                    sudo("sh bin/startup.sh", pty=False)
                else:
                    sudo("sh startup.sh", pty=False)
                counts += 1
                if counts >= 10:
                    print "Failed too many times, breaking out"
                    break
            else:
                break

def deploy(config, section):
    """Deploys code, publishes and restarts a remote server"""
    sync(config, section)
    publish(config, section)
    restart_server(config,section)
