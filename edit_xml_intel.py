import sys
import os
import xml.etree.ElementTree as ET
import array
#numOfVM=sys.argv[1]
vmName=sys.argv[1]
macAddrVMs=sys.argv[2]
numOfCPU=sys.argv[3]
ram=sys.argv[4]
numOfNets=sys.argv[5]
netNames=sys.argv[6]
netMacs=sys.argv[7]
slot=sys.argv[8]
ovsBridgePres=sys.argv[9]
interface=sys.argv[10]

top=[]
#os.system("ovs-vsctl add-br %s" %sys.argv[1])
os.system("cp /etc/libvirt/qemu/default.xml /etc/libvirt/qemu/%s.xml" %vmName)

filename="/etc/libvirt/qemu/%s.xml" %vmName
for i in range(int(numOfNets)):
    if ovsBridgePres.split(",")[i]=="Ovs" and interface.split(",")[i] == "bridge":
        ovsBridgeName=sys.argv[11]
        ovsBridgeMac=sys.argv[12]
        slot_ovs=sys.argv[13]

    top.append(ET.Element('interface'))
    top[i].set("type", "network")
    if(macAddrVMs!="null"):
        mac = ET.SubElement(top[i], 'mac')
        mac.set("address",netMacs.split(',')[i])
    source=ET.SubElement(top[i],'source')
    source.set("network",netNames.split(',')[i])
    model=ET.SubElement(top[i],"model")
    model.set("type","virtio")
    address=ET.SubElement(top[i],"address")
    address.set("type","pci")
    address.set("domain","0x0000")
    address.set("bus","0x00")
    address.set("slot",slot.split(',')[i])
    address.set("function","0x0")
    output=ET.tostring(top[i],encoding='utf-8',method='xml').decode()
    print(output)
if ovsBridgePres=="Ovs":
    subelem2 = ET.Element('interface')
    subelem2.set("type", "bridge")
    if(ovsBridgeMac!="null"):
        mac = ET.SubElement(subelem2, 'mac')
        mac.set("address",ovsBridgeMac)
    source=ET.SubElement(subelem2,'source')
    source.set("bridge",ovsBridgeName)
    virtualport=ET.SubElement(subelem2,"virtualport")
    virtualport.set("type","openvswitch")
    address=ET.SubElement(subelem2,"address")
    address.set("type","pci")
    address.set("domain","0x0000")
    address.set("bus","0x00")
    address.set("slot","%s" %slot_ovs)
    address.set("function","0x0")
    output=ET.tostring(subelem2,encoding='utf-8',method='xml').decode()

tree = ET.parse(filename).getroot()
my_file = open(filename, "r")
#a = list(tree)[1]       # Get parent node from EXISTING tree
for child in tree.findall('./devices/disk/source/[@file="/var/lib/libvirt/images/VM_q5-1.img"]'):
    child.set("file","/var/lib/libvirt/images/%s.img" %vmName)
for child in tree:
    if child.tag=="name":
        child.text=vmName
    elif child.tag=="uuid":
        tree.remove(child)
    elif child.tag=="vcpu":
        child.text=numOfCPU
    elif child.tag=="memory":
        child.text=ram
    elif child.tag=="devices":
        for source in child:
            if source.tag=="interface":
                if macAddrVMs!="null":
                    for tags in source:
                        if tags.tag=="mac":
                            tags.set("address",macAddrVMs)
                else:
                    child.remove(source)

        for i in range(int(numOfNets)):
            child.append(top[i])
        if ovsBridgePres=="Ovs":
            child.append(subelem2)

    #elif child.tag=="devices":
        #child.getroot()
        #for source in child:
        #    source.set("file","/var/lib/libvirt/images/%s" %sys.argv[5])
        #for subelem in child.iter():
        #    if subelem.tag=="disk":
        #        for sub_sub in subelem.iter():
        #            if sub_sub=="source":
        #                sub_sub.set("file","/var/lib/libvirt/images/%s" %sys.argv[5])
#tree.append(top)
#tree.append(subelem2)

my_file.close()
#print(sys.argv[1])
print(sys.argv[1])
#list(tree)[0].text=sys.argv[1]
#tree.remove(a)
output=ET.tostring(tree,encoding='utf-8',method='xml').decode()
print(output)
#tree.write("try1.xml",encoding='utf8')
my_network_xml=filename
my_network_xml_file=open(my_network_xml,"w+")
my_network_xml_file.write(str(output))
my_network_xml_file.close()
#print(command_define_net)
#print(cmd_start_net)
