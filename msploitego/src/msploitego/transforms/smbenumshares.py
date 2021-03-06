from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "smb-enum-shares", ip)

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].scripts_results:
            output = res.get("output").split("\n")
            regex = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            bucket = bucketparser(regex,output,method="search")
            for item in bucket:
                header = item.get("Header")
                shareentity = mt.addEntity("msploitego.SambaShare", header)
                shareentity.setValue(header)
                sharename = header.split("\\")[-1].strip().strip(":")
                shareentity.addAdditionalFields("sharename", "Share Name", False, sharename)
                shareentity.addAdditionalFields("sambashare", "Samba Share", False, header)
                shareentity.addAdditionalFields("ip", "IP Address", False, ip)
                shareentity.addAdditionalFields("port", "Port", False, port)
                for k,v in item.items():
                    if k == "Header":
                        continue
                    shareentity.addAdditionalFields(k.lower(), k, False, v)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbenumservices.py',
#  'smb/445:39',
#  'properties.metasploitservice=smb/445:39#info=Windows 2000 SP0 - 4 (language:English) (name:JD)#name=smb#proto=tcp#hostid=39#service.name=smb#port=445#banner=Windows 2000 SP0 - 4 (language:English) (name:JD)#properties.service= #ip=10.11.1.24#state=open#fromfile=/root/data/report_pack/msploitdb_oscp-20180325.xml']
# dotransform(args)
