script_base = """<?xml version="1.0"?>
<project name="auto-sync" default="endpoint" basedir=".">

  <taskdef
      name="webdav-sync"
      classname="be.re.webdav.cmd.SyncAntTask"
      classpath="%(current)s/webdav_sync1_0_1.jar" />

  <property name="module.loc" value="http://%(user)s:%(password)s@%(endpoint)s/webdav/system/modules/%(module)s" />
  <property name="site.loc" value="" />
  <property name="test.loc" value="" />
  <property name="direction" value="up" />
  <property name="excludes" value="__properties*,\.*,.*~,.*#" />

  <target name="endpoint">
    %(transfers)s
  </target>

</project>
"""

entry_base = """
<webdav-sync direction="${direction}" url="${module.loc}/" directory="." excludes="${excludes}"/>
<webdav-sync direction="${direction}" url="${module.loc}/%(url)s/" directory="%(directory)s" excludes="${excludes}"/>
"""
