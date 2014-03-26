#! /usr/bin/env python
"""Checks one/multiple remote zypper instances for updates and updates via Amazon SNS
"""
import boto
import logging
import serverList as serverList
import subprocess
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
from prettytable import PrettyTable

__author__ = "Chaudhry Usman Ali"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Chaudhry Usman Ali"
__email__ = "mani.ali@unb.ca"
__status__ = "Development"

def send_sns_msg_aws(topic_arn,mesg,topicstring):
    try:
        c = boto.connect_sns()
        c.publish(topic_arn,mesg,topicstring)
    except Exception , e:
        print e

topic_string = 'Updates available in Zypper'
update_items={}
parser = OptionParser()
parser.add_option('-t','--topic',type='string',dest='topic_arn',help='Destination SNS topic ARN')
(options, args) = parser.parse_args()

if options.topic_arn is None :
    logging.error('Please specify a destination SNS topic ARN.')
    parser.print_help()
    sys.exit(-1)

tabular_updates_data = PrettyTable(["Package","HostNames"])
tabular_updates_data.padding_width = 1
tabular_updates_data.align["Package"] = "l"
tabular_updates_data.align["HostNames"] = "l"

for hostname, host_information in serverList.servers.iteritems() :
    p = subprocess.Popen([
                 'ssh',
                 '-i', host_information['authorized_key'],
                 host_information['authorized_user'] + '@' + hostname,
                 host_information['zypper_bin'] +
                 ' -x' +
                 ' lu'
                 ],stdout=subprocess.PIPE)
    p.wait()
    tree = ET.fromstring(p.stdout.read())
    for update in tree.iter('update'):
        update_ident_string = update.attrib['name']+'_'+update.attrib['edition']
        try:
            update_items[update_ident_string]
        except:
            update_items[update_ident_string]=[]
        update_items[update_ident_string].append(hostname)

if len(update_items) > 0:
    for update_name, hosts_list in update_items.iteritems() :
        tabular_updates_data.add_row([update_name,",\n".join(hosts_list)])
    send_sns_msg_aws(options.topic_arn,topic_string+":\n" +tabular_updates_data.get_string(),topic_string)
