import sys
import os
import xml.etree.ElementTree as ET

netName=sys.argv[1]
forwardMode=sys.argv[2]
bridgeName=sys.argv[3]
isOvs=sys.argv[4]
if forwardMode == "bridge" or isOvs == "Ovs":
    ipaddr="null"
    macaddr="null"
    forwardMode="bridge"
else:
    ipaddr=sys.argv[6]
    macaddr=sys.argv[5]

#os.system("ovs-vsctl add-br %s" %sys.argv[1])
os.system("cp /etc/libvirt/qemu/networks/default.xml /etc/libvirt/qemu/networks/%s.xml" %netName)
filename="/etc/libvirt/qemu/networks/default.xml"
tree = ET.parse(filename).getroot()
#subelem=ET.Element('forward')
#subelem.set("mode",sys.argv[2])
my_file = open(filename, "r")
flag=False
for child in tree:
    if child.tag=="uuid":
        tree.remove(child)
#a = list(tree)[1]       # Get parent node from EXISTING tree
for child in tree:
    print(child.tag)
    if child.tag=="forward":
        child.set("mode",forwardMode)
    elif child.tag=="name":
        child.text=netName
    elif child.tag=="bridge":
        child.set("name",bridgeName)
    elif child.tag=="mac":
        child.set("address",macaddr)
    elif child.tag=="ip":
        if ipaddr != "null": 
            ipaddr=ipaddr.split("/")[0]
            child.set("address",ipaddr)
            iparr=ipaddr.split(".")
            ipstart=iparr[0]+"."+iparr[1]+"."+iparr[2]+"."+"3"
            ipend = iparr[0] + "." + iparr[1] + "." + iparr[2] + "." + "254"
            list(list(child)[0])[0].set("start",ipstart)
            list(list(child)[0])[0].set("end", ipend)

if macaddr =="null":
    for child in tree:
        if child.tag=="mac":
            tree.remove(child)



if forwardMode=="bridge" or isOvs == "Ovs":
    for child in tree:
        if child.tag=="ip":
            tree.remove(child)
    for child in tree:
        if child.tag=="mac":
            tree.remove(child)
    subelem1=ET.Element("bridge")
    subelem1.set("name",bridgeName)
    for child in tree:
        if child.tag=="bridge":
            tree.remove(child)
    tree.append(subelem1)
if isOvs=="Ovs":
    subelem=ET.Element("virtualport")
    subelem.set("type","openvswitch")
    tree.append(subelem)
#tree.append(subelem)
#list(tree)[1].set("mode",sys.argv[2])
my_file.close()
#print(sys.argv[1])
#list(tree)[0].text=sys.argv[1]
#tree.remove(a)
output=ET.tostring(tree,encoding='utf-8',method='xml').decode()
print(output)
#tree.write("try1.xml",encoding='utf8')
my_network_xml="/etc/libvirt/qemu/networks/%s.xml" %sys.argv[1]
my_network_xml_file=open(my_network_xml,"w+")
my_network_xml_file.write(str(output))
my_network_xml_file.close()
#command_define_net="virsh net-define /etc/libvirt/qemu/networks/%s.xml" %sys.argv[2]
#print(command_define_net)
#os.system(command_define_net)
#cmd_start_net="virsh net-start %s" %sys.argv[3]
#print(cmd_start_net)
#os.system(cmd_start_net)
