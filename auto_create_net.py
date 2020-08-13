import json
import yaml
import sys
import os
import subprocess
import time
with open("datamodel/hooks.json", "r") as read_file:
    data=json.load(read_file)
with open("datamodel/user_input.json", "r") as read_file:
    data_user=json.load(read_file)
print("data is %s" %(data["namespace_router"][0]["name"]))
loop=len(data["namespace_router"])
print("printing loop")
print(loop)
i=1
ip=data["namespace_router"][0]["infip"]
router="%s" %(data["namespace_router"][0]["name"])
rout=subprocess.Popen(["sudo ip netns show | grep %s" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
op=rout.communicate()
if router not in op[0]:
    create_router_ns=subprocess.Popen(["sudo ip netns add %s" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
    print("sudo ip netns add %s" %(data["namespace_router"][0]["name"]))
    hyp_veth_pair=subprocess.Popen(["sudo ip link add int_pn type veth peer name in_pn"],shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    push_veth_ns=subprocess.Popen(["sudo ip link set in_pn netns %s" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
    add_ip_hyp=subprocess.Popen(["sudo ip addr add 99.99.99.1/24 dev int_pn"],shell=True, stdout=subprocess.PIPE)
    set_link_up_hyp=subprocess.Popen(["sudo ip link set int_pn up"],shell=True, stdout=subprocess.PIPE)
    ip_netns=subprocess.Popen(["sudo ip netns exec %s ip addr add 99.99.99.2/24 dev in_pn" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
    time.sleep(4)
    ip_netns_up=subprocess.Popen(["sudo ip netns exec %s ip link set in_pn up" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
    masq=subprocess.Popen(["sudo iptables -t nat -A POSTROUTING -s 99.99.99.0/24 ! -d 99.99.99.0/24 -j MASQUERADE"],shell=True, stdout=subprocess.PIPE)
    ip_table_netns=subprocess.Popen(["sudo ip netns exec %s ip route add default via 99.99.99.1" %(data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
for name,value in data_user.items():
    print(value)
    for list_1 in value:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(list_1)
        vpc="%s_%d" %(data["namespace_router"][1]["name"],i)
        #print("here!!!!!!!!!!!!!!!!!!!1")
        #print("sudo ip netns show | grep %s_%d" %(data["namespace_router"][1]["name"],i))
        time.sleep(1)
        grep=subprocess.Popen(["sudo ip netns show | grep %s_%d" %(data["namespace_router"][1]["name"],i)],shell=True, stdout=subprocess.PIPE)
        op=grep.communicate()
        print("sudo ip netns show | grep %s_%d" %(data["namespace_router"][1]["name"],i))
        print(op)
        if vpc not in op[0]:

            create_ns=subprocess.Popen(["sudo ip netns add %s_%d" %(data["namespace_router"][1]["name"],i)],shell=True, stdout=subprocess.PIPE)
            print("sudo ip netns add %s_%d" %(data["namespace_router"][1]["name"],i))
            create_veth_pair=subprocess.Popen(["sudo ip link add %s_%d type veth peer name %s_%d" %(data["namespace_router"][0]["vethpair_name"],i,data["namespace_router"][1]["vethpair_name"],i)],shell=True, stdout=subprocess.PIPE)
            print("sudo ip link add %s_%d type veth peer name %s_%d" %(data["namespace_router"][0]["vethpair_name"],i,data["namespace_router"][1]["vethpair_name"],i))
            time.sleep(1)
            edit_ip=ip.split(".")

            set_ip_link_up=subprocess.Popen(["sudo ip link set %s_%d netns %s_%d" %(data["namespace_router"][1]["vethpair_name"],i,data["namespace_router"][1]["name"],i)],shell=True, stdout=subprocess.PIPE)
            
            print("sudo ip link set %s_%d netns %s_%d" %(data["namespace_router"][1]["vethpair_name"],i,data["namespace_router"][1]["name"],i))
            set_ip_link_up2=subprocess.Popen(["sudo ip link set %s_%d netns %s" %(data["namespace_router"][0]["vethpair_name"],i,data["namespace_router"][0]["name"])],shell=True, stdout=subprocess.PIPE)
            time.sleep(1)
            print("sudo ip link set %s_%d netns %s" %(data["namespace_router"][0]["vethpair_name"],i,data["namespace_router"][0]["name"]))
            intf_ip1=subprocess.Popen(["sudo ip netns exec %s_%d ip addr add %s.%s.%s.1/24 dev %s_%d" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],i,data["namespace_router"][1]["vethpair_name"],i)],shell=True, stdout=subprocess.PIPE)
            print("sudo ip netns exec %s_%d ip addr add %s.%s.%s.1/24 dev %s_%d" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],i,data["namespace_router"][1]["vethpair_name"],i))
            time.sleep(1)
            intf_ip2=subprocess.Popen(["sudo ip netns exec %s ip addr add %s.%s.%s.2/24 dev %s_%d" %(data["namespace_router"][0]["name"],edit_ip[0],edit_ip[1],i,data["namespace_router"][0]["vethpair_name"],i)],shell=True, stdout=subprocess.PIPE)
            print("sudo ip netns exec %s ip addr add %s.%s.%s.2/24 dev %s_%d" %(data["namespace_router"][0]["name"],edit_ip[0],edit_ip[1],i,data["namespace_router"][0]["vethpair_name"],i))
            set_up=subprocess.Popen(["sudo ip netns exec %s ip link set %s_%d up" %(data["namespace_router"][0]["name"],data["namespace_router"][0]["vethpair_name"],i)],shell=True, stdout=subprocess.PIPE)
            set_up=subprocess.Popen(["sudo ip netns exec %s_%d ip link set %s_%d up" %(data["namespace_router"][1]["name"],i,data["namespace_router"][1]["vethpair_name"],i)],shell=True, stdout=subprocess.PIPE)
            masq_vpc=subprocess.Popen(["sudo ip netns exec %s iptables -t nat -A POSTROUTING -s %s.%s.%s.0/24 ! -d %s.%s.%s.0/24 -j MASQUERADE" %(data["namespace_router"][0]["name"],edit_ip[0],edit_ip[1],i,edit_ip[0],edit_ip[1],i)],shell=True, stdout=subprocess.PIPE)
            time.sleep(4)
            #print("sudo ip netns exec %s_%d ip route add default via %s.%s.%s.2/24" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],i))
            add_route_vpc=subprocess.Popen(["sudo ip netns exec %s_%d ip route add default via %s.%s.%s.2" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],i)],shell=True, stdout=subprocess.PIPE)
        i+=1
i=1
for name,value in data_user.items():
    for list_1 in value:
        j=1
        for name_2,value_2 in list_1.items():
            print("value_2 is ")

            print(value_2)
            if name_2 == "routes":
                print(name_2)
                for list_2 in value_2:
                    for name_3,value_3 in list_2.items():
                        print(name_3)
                        if name_3 == "vpcs_subnet":
                            print(name_3)
                            subnet="%s_%d_%d" %(data["namespace_router"][2]["name"],i,j)
                            grep=subprocess.Popen(["sudo ip netns show | grep %s_%d_%d" %(data["namespace_router"][2]["name"],i,j)],shell=True, stdout=subprocess.PIPE)
                            op=grep.communicate()
                            print(op)
                            if subnet not in op[0]:
                                subnet_router=subprocess.Popen(["sudo ip netns add %s_%d_%d" %(data["namespace_router"][2]["name"],i,j)],shell=True, stdout=subprocess.PIPE)
                                create_veth_pair_3=subprocess.Popen(["sudo ip link add %s_%d_%d type veth peer name %s_%d_%d" %(data["namespace_router"][1]["vethpair_connect_subrouter"],i,j,data["namespace_router"][2]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                time.sleep(1)
                                edit_ip=data["namespace_router"][2]["subrouip"].split(".")

                                set_ip_link_up=subprocess.Popen(["sudo ip link set %s_%d_%d netns %s_%d_%d" %(data["namespace_router"][2]["vethpair_connect_subrouter"],i,j,data["namespace_router"][2]["name"],i,j)],shell=True, stdout=subprocess.PIPE)

                                set_ip_link_up2=subprocess.Popen(["sudo ip link set %s_%d_%d netns %s_%d" %(data["namespace_router"][1]["vethpair_connect_subrouter"],i,j,data["namespace_router"][1]["name"],i)],shell=True, stdout=subprocess.PIPE)
                                time.sleep(1)
                                intf_ip1=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip addr add %s.%s.%s.1/24 dev %s_%d_%d" %(data["namespace_router"][2]["name"],i,j,edit_ip[0],edit_ip[1],j,data["namespace_router"][2]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                time.sleep(1)
                                intf_ip2=subprocess.Popen(["sudo ip netns exec %s_%d ip addr add %s.%s.%s.2/24 dev %s_%d_%d" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],j,data["namespace_router"][1]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                set_up=subprocess.Popen(["sudo ip netns exec %s_%d ip link set %s_%d_%d up" %(data["namespace_router"][1]["name"],i,data["namespace_router"][1]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                set_up=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip link set %s_%d_%d up" %(data["namespace_router"][2]["name"],i,j,data["namespace_router"][2]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                time.sleep(4)
                                masq_vpc=subprocess.Popen(["sudo ip netns exec %s_%d iptables -t nat -A POSTROUTING -s %s.%s.%s.0/24 ! -d %s.%s.%s.0/24 -j MASQUERADE" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],j,edit_ip[0],edit_ip[1],j)],shell=True, stdout=subprocess.PIPE)
                                #print("sudo ip netns exec %s_%d_%d ip route add default via %s.%s.%s.2/24" %(data["namespace_router"][2]["name"],i,j,edit_ip[0],edit_ip[1],j))
                                add_route_vpc=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip route add default via %s.%s.%s.2" %(data["namespace_router"][2]["name"],i,j,edit_ip[0],edit_ip[1],j)],shell=True, stdout=subprocess.PIPE)
                            j+=1

        i+=1    

print("here!!!!!!!!!!!!!")
i=1
additional_net={}
for name,value in data_user.items():
    for list_1 in value:
        j=1
        for name_2,value_2 in list_1.items():
            #print("value_2 is ")

            #print(value_2)
            if name_2 == "routes":
                #print(name_2)
                for list_2 in value_2:
                    k=1
                    for name_3,value_3 in list_2.items():
                        #print(name_3)
                        if name_3 == "vpcs_subnet":
                            #print(name_3)
                            #print("%%%%")
                            for list_3 in value_3:
                                subnet="%s_%d_%d" %(data["namespace_router"][2]["name"],i,j)
                                grep=subprocess.Popen(["sudo ip addr | grep %s_%d_%d_%d" %(data["namespace_router"][3]["vethpair_connect_bridge"],i,j,k)],shell=True, stdout=subprocess.PIPE)
                                op=grep.communicate()
                                if("%s_%d_%d_%d" %(data["namespace_router"][3]["vethpair_connect_bridge"],i,j,k) not in op[0]):

                                    #print(value_3)
                                    #for name_4,value_4 in list_3.items():
                                    #print(name_4,value_4)
                                    print("sudo ip link add %s_%d_%d_%d type veth peer name %s_%d_%d_%d" %(data["namespace_router"][3]["vethpair_connect_bridge"],i,j,k,data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k))
                                    create_veth_pair_4=subprocess.Popen(["sudo ip link add %s_%d_%d_%d type veth peer name %s_%d_%d_%d" %(data["namespace_router"][3]["vethpair_connect_bridge"],i,j,k,data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k)],shell=True, stdout=subprocess.PIPE)
                                    time.sleep(1)
                                    #mask=value_4.split("/")
                                    #ip=mask[0]
                                    #mask=mask[1]
                                    edit_ip_start=list_3["subnet_start"].split(".")
                                    edit_ip_end=list_3["subnet_end"].split(".")
                                    set_ip_link_up=subprocess.Popen(["sudo ip link set %s_%d_%d_%d netns %s_%d_%d" %(data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k,data["namespace_router"][2]["name"],i,j)],shell=True, stdout=subprocess.PIPE)
                                    intf_ip1=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip addr add %s/24 dev %s_%d_%d_%d" %(data["namespace_router"][2]["name"],i,j,list_3["subnet_start"],data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k)],shell=True, stdout=subprocess.PIPE)
                                    time.sleep(4)
                                    #intf_ip2=subprocess.Popen(["sudo ip netns exec %s_%d ip addr add %s.%s.%s.2/24 dev %s_%d_%d" %(data["namespace_router"][1]["name"],i,edit_ip[0],edit_ip[1],j,data["namespace_router"][1]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                    set_up=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip link set %s_%d_%d_%d up" %(data["namespace_router"][2]["name"],i,j,data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k)],shell=True, stdout=subprocess.PIPE)
                                    masq_vpc=subprocess.Popen(["sudo ip netns exec %s_%d_%d iptables -t nat -A POSTROUTING -o  %s_%d_%d -j MASQUERADE" %(data["namespace_router"][2]["name"],i,j,data["namespace_router"][2]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                        #set_up=subprocess.Popen(["sudo ip netns exec %s_%d_%d ip link set %s_%d_%d up" %(data["namespace_router"][2]["name"],i,j,data["namespace_router"][2]["vethpair_connect_subrouter"],i,j)],shell=True, stdout=subprocess.PIPE)
                                edit_ip_start=list_3["subnet_start"].split(".")
                                edit_ip_end=list_3["subnet_end"].split(".")

                                network=list_3["name"]
                                additional_net["name"]=list_3["name"]
                                additional_net["forwardMode"]="route"
                                additional_net["iprange"]=list_3["subnet_start"]
                                additional_net["bridgename"]="bridge_%s_%s_%s" %(i,j,k)
                                additional_net["isOvs"]="Ovs"
                                additional_net["already_present"]="False"
                                additional_net["netMac"]="null"
                                additional_net["namespace"]="%s_%s_%s" %(data["namespace_router"][2]["name"],i,j)
                                additional_net["dhcp_range"]="%s.%s.%s.%s,%s,12h" %(edit_ip_start[0],edit_ip_start[1],edit_ip_start[2],(int(edit_ip_start[3])+1),list_3["subnet_end"])
                                additional_net["subnet_address"]="%s/24" %(list_3["subnet_start"])
                                additional_net["interface"]="%s_%s_%s_%s" %(data["namespace_router"][3]["vethpair_connect_bridge"],i,j,k)
                                additional_net["interface2"]="%s_%s_%s_%s" %(data["namespace_router"][2]["vethpair_connect_bridge"],i,j,k)
                                flag=False
                                with open('ansible/vars/net_details.yml','r') as yaml_load:
                                    data1=yaml.load(yaml_load, Loader=yaml.FullLoader)
                                    if(data1["Networks"]):
                                        print(network)
                                        print(data1["Networks"])
                                        for check in data1["Networks"]:
                                            print(check)
                                            print("_____________________________________________________________")
                                            if(check["name"]==network):
                                                data1["Networks"][data1["Networks"].index(check)]["already_present"]="True"
                                                flag=True
                                        if not flag:
                                            data1["Networks"].append(additional_net)

                                    else:
                                        data1["Networks"]=[]
                                        data1["Networks"].append(additional_net)
                                    print(data1)
                                with open('ansible/vars/net_details.yml','w') as yaml_load:
                                    yaml.safe_dump(data1,yaml_load)

                                k+=1 
                            j+=1

        i+=1   
trigger_ansible=subprocess.Popen(["sudo ansible-playbook ansible/tasks/create_ovs_infra.yml"],shell=True, stdout=subprocess.PIPE)
op=trigger_ansible.communicate()
print(op)

trigger_ansible=subprocess.Popen(["sudo ansible-playbook ansible/tasks/create_network.yml"],shell=True, stdout=subprocess.PIPE)
op=trigger_ansible.communicate()
print(op)


i=1
additional_net={}
for name,value in data_user.items():
    for list_1 in value:
        j=1
        for name_2,value_2 in list_1.items():
            #print("value_2 is ")

            #print(value_2)
            if name_2 == "routes":
                #print(name_2)
                for list_2 in value_2:
                    k=1
                    for name_3,value_3 in list_2.items():
                        #print(name_3)
                        if name_3 == "vpcs_vm":
                            #print(name_3)
                            #print("%%%%")
                            for list_3 in value_3:
                                #print(value_3)
                                print(list_3)
                                addition={}
                                addition["vmName"]=list_3["vmName"]
                                addition["ram"]=list_3["ram"]

                                addition["cpus"]=list_3["cpus"]
                                addition["mem"]=list_3["mem"]
                                #addition["mac"]=list_3["mac"]
                                addition["numOfNet"]=list_3["numOfNet"]

                                addition["netName"]=list_3["netName"]
                                #addition["netMac"]=list_3["netMac"]
                                addition["pci"]=list_3["pci"]
                                addition["already_present"]="False"
                                addition["packages"]=list_3["packages"]
                                isOvs="Ovs"
                                interf="network"
                                netmac="null"
                                for i in range(int(list_3["numOfNet"])-1):
                                    isOvs+=",Ovs"
                                    interf+=",network"
                                    netmac+=",null"
                                addition["netMac"]=netmac
                                addition["mac"]="null"
                                addition["isOvs"]=isOvs
                                addition["img"]="false"
                                addition["pwd"]=list_3["pwd"]
                                addition["interface"]=interf
                                vmName=list_3["vmName"]
                                flag=False
                                with open('ansible/vars/VM_details.yml','r') as yaml_load:
                                    data1=yaml.load(yaml_load, Loader=yaml.FullLoader)
                                    print(data1)
                                    print("!!!!!")
                                    if(data1["guests"]):
                                        print(vmName)
                                        print(data1["guests"])
                                        for check in data1["guests"]:
                                            print(check)
                                            print("_____________________________________________________________")
                                            if(check["vmName"]==vmName):
                                                data1["guests"][data1["guests"].index(check)]["already_present"]="True"
                                                flag=True
                                        if not flag:
                                            data1["guests"].append(addition)

                                    else:
                                        data1["guests"]=[]
                                        data1["guests"].append(addition)
                                    print(data1)
                                with open('ansible/vars/VM_details.yml','w') as yaml_load:
                                    yaml.safe_dump(data1,yaml_load)

                                k+=1
                            j+=1

        i+=1

trigger_ansible=subprocess.Popen(["sudo ansible-playbook ansible/tasks/createVM.yml -vv"],shell=True, stdout=subprocess.PIPE)
op=trigger_ansible.communicate()
print(op)


i=1
additional_net={}
for name,value in data_user.items():
    for list_1 in value:
        j=1
        for name_2,value_2 in list_1.items():
            #print("value_2 is ")

            #print(value_2)
            if name_2 == "routes":
                #print(name_2)
                for list_2 in value_2:
                    k=1
                    for name_3,value_3 in list_2.items():
                        #print(name_3)
                        if name_3 == "vpcs_vm":
                            #print(name_3)
                            #print("%%%%")
                            for list_3 in value_3:

                                k+=1
                            j+=1

        i+=1





