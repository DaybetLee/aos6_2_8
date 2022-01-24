import re
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

########################################################


def listToString(s, space=0):
    # initialize an empty string
    str1 = ""

    if space == 0:
        # traverse in the string
        for ele in s:
            str1 += ele
    elif space == 1:
        # traverse in the string
        for ele in s:
            str1 += ele + " "
        # return string
    return str1


def taggedRange(vlanId, vlanIntChassis, switchport, tagged):
    vlanRange = "vlan " + str(vlanId) + " members port " + \
        vlanIntChassis + "/1/" + str(switchport)
    outputFile.write(vlanRange + " " + tagged + "\n")
    return vlanRange


def unpRange(interfaceChassis, switchport):
    range = "unp port " + interfaceChassis + "/1/" + str(switchport)
    outputFile.write(range + " port-type bridge\n")
    outputFile.write(range + " port-template voice-template\n")
    return range


def portSecPortRange(interfaceChassis, switchport, option="enable"):
    range = "port-security port " + interfaceChassis + "/1/" + str(switchport)
    outputFile.write(range + " admin-state " + option + "\n")
    return range


def portSecMaxPortRange(portMax, interfaceChassis, switchport):
    range = "port-security port " + interfaceChassis + "/1/" + str(switchport)
    outputFile.write(range + " maximum " + str(portMax) + "\n")
    return range


def getSwitchport(stripedLine):
    return int(listToString(re.findall(
        r'(?<=\/1\/).*$', stripedLine)).split(" ")[0])


def getInterfaceChassis(stripedLine):
    return listToString(re.findall(
        r'(?<=port ).*$', stripedLine)).split("/")[0]


def stripeName(stripedLine):
    return listToString(re.findall(
        r'(?<=name ).*$', stripedLine))


def addCommaToUsrInputStr(syntax):
    usrInputStr = stripedLine.strip(syntax).strip('"')
    outputFile.write(syntax + ' "' + usrInputStr + '"' + "\n")


def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')
    # print out some text

########################################################


portMobile = ""
tacacsServer = ""
defaultVlan = 0
voiceVlan = 0
tacacsServerKey = ""
defaultVlanName = ""
voiceVlanName = ""
vlanTaggedCount = 0
vlanUntagCount = 0
portSecEnaCount = 0
portSecDisCount = 0
portSecMaxCount = 0
unpCount = 0
confirmation = "n"
filename = ""
fileSelectRetry = 0


input("\nPlease select the configuration file to be converted [Enter]:")
while filename == "":
    filename = filedialog.askopenfilename()
    fileSelectRetry = fileSelectRetry + 1
    if fileSelectRetry == 3:
        print("No file selected. Closing Script. Goodbye.")
        exit()
while not portMobile == "n" and not portMobile == "y":
    portMobile = input("\nIs the switch using mobile tag? (y/n): ").lower()
while defaultVlan < 1 and portMobile == "y":
    defaultVlan = int(input(
        "\nPlease enter the default VLAN for port mobile [1-4096]: "))
while voiceVlan < 1 and portMobile == "y":
    voiceVlan = int(input(
        "\nPlease enter the voice VLAN for port mobile [1-4096]: "))
while not tacacsServer == "n" and not tacacsServer == "y":
    tacacsServer = input(
        "\nIs the switch authenticate by TACACS Server? (y/n): ").lower()
while tacacsServerKey == "" and tacacsServer == "y":
    while confirmation == "n" and not confirmation == "y":
        tacacsServerKey = input("\nPlease enter the TACACS key: ")
        confirmation = input(
            "\nPlease confirm the key is entered correctly (y/n): ").lower()
    confirmation = "n"
input("\nPress any key to start the convertion:")


outputfilename = filename.split(
    "/")[-1].split(".")[0] + "_converted." + filename.split("/")[-1].split(".")[-1]

inputFile = open(filename, "r")
# os.remove("AOS6_Converted_" + filename)  # for development
outputFile = open(outputfilename, "a")
tempFile = open("temp.txt", "w")

for line in inputFile.readlines()[:]:
    stripedLine = line.strip()
    if not stripedLine.endswith(":"):
        # print(stripedLine)
        ###########################################################
        # Chassis
        if re.match(r'(system\sname\s.+)', line):
            addCommaToUsrInputStr("system name")
            continue

        if re.match(r'(system\scontact\s.+)', line):
            addCommaToUsrInputStr("system contact")
            continue

        if re.match(r'(system\slocation\s.+)', line):
            addCommaToUsrInputStr("system location")
            continue

        # System timezone
        if re.match(r'(system\stimezone\s.+)', line):
            outputFile.write("system timezone ZP8" + "\n")
            continue

        # System daylight saving
        if re.match(r'(system\sdaylight\ssavings\stime\sdisable)', line):
            daylightSavingStatus = listToString(re.findall(
                r'(?<=time ).*$', stripedLine))
            outputFile.write("system daylight-savings-time " +
                             daylightSavingStatus+"\n")
            continue

        # mac-retention
        if re.match(r'(mac-retention\sstatus\senable)', line):
            macRetenStatus = listToString(
                re.findall(r'(?<=status ).*$', stripedLine))
            outputFile.write("mac-retention admin-state " +
                             macRetenStatus+"\n")
            continue

        # VLAN
        if stripedLine.startswith("vlan"):
            vlanId = stripedLine.split()[1]
            # VLAN and Name
            if re.match(r'(vlan\s\d+\senable\sname\s.+)', line):
                vlanName = stripeName(stripedLine)
                vlanStatus = stripedLine.split()[2]
                outputFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                tempFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                outputFile.write("vlan " + vlanId +
                                 " admin-state " + vlanStatus + "\n")

            # vlan untagged
            if re.match(r'(vlan\s\d+\sport\sdefault\s\d+\/\d+$)', line):
                vlanIntChassis = listToString(re.findall(
                    r'(?<=default ).*$', stripedLine)).split("/")[0]
                vlanIntPort = listToString(re.findall(
                    r'(?<=default ).*$', stripedLine)).split("/")[1]
                tempFile.write("vlan " + vlanId + " members port " +
                               vlanIntChassis + "/1/" + vlanIntPort + " untagged" + "\n")
                vlanUntagCount = vlanUntagCount + 1

            if re.match(r'(vlan\s\d+\sport\sdefault\s\d+$)', line):
                vlanLinkagg = stripedLine.split()[-1]
                outputFile.write("vlan "+vlanId+" members linkagg " +
                                 vlanLinkagg+" untagged\n")

            # vlan tagged
            if re.match(r'(vlan\s\d+\s802.1q\s\d+\/\d+\s.+)', line):
                vlanInterface = listToString(re.findall(
                    r'vlan\s\d+\s802.1q\s\d+\/\d+', stripedLine)).split()[-1].split("/")[0] + "/1/" + listToString(re.findall(
                        r'vlan\s\d+\s802.1q\s\d+\/\d+', stripedLine)).split()[-1].split("/")[1]
                tempFile.write("vlan "+vlanId+" members port " +
                               vlanInterface+" tagged\n")
                vlanTaggedCount = vlanTaggedCount + 1

            if re.match(r'(vlan\s\d+\s802.1q\s\d+\s)', line):
                vlanLinkagg = stripedLine.split()[3]
                outputFile.write("vlan "+vlanId+" members linkagg " +
                                 vlanLinkagg+" tagged\n")

            # unp profile
            if re.match(r'vlan\s'+str(defaultVlan)+'\s(enable|disable)\sname\s.+', line):
                defaultVlanName = stripeName(stripedLine)

            elif re.match(r'vlan\s'+str(voiceVlan)+'\s(enable|disable)\sname\s.+', line):
                voiceVlanName = stripeName(stripedLine)

            # unp ports
            if re.match(r'(vlan\sport\smobile\s.+)', line):
                vlanIntChassis = listToString(re.findall(
                    r'(?<=mobile ).*$', stripedLine)).split("/")[0]
                vlanIntPort = listToString(re.findall(
                    r'(?<=mobile ).*$', stripedLine)).split("/")[1]
                tempFile.write("unp port " +
                               vlanIntChassis + "/1/" + vlanIntPort + " port-type bridge" + "\n")
                tempFile.write("unp port " +
                               vlanIntChassis + "/1/" + vlanIntPort + " port-template voice-template" + "\n")
                unpCount = unpCount + 1
            continue

        # ip services (https and network syntax changed)
        if re.match(r'(^(no\sip|ip)\sservice\s(ftp|ssh|telnet|http|snmp|secure-http|network-time))', line):
            service = stripedLine.split()[-1]

            if stripedLine.split()[0] != "no":
                if service == "secure-http":
                    outputFile.write("ip service https admin-state enable\n")
                    continue
                elif service == "network-time":
                    outputFile.write("ip service ntp admin-state enable\n")
                    continue
                else:
                    outputFile.write("ip service " + service +
                                     " admin-state enable\n")
                    continue
            else:
                service = listToString(re.findall(
                    r'(?<=service ).*$', stripedLine))
                if service == "secure-http":
                    outputFile.write("ip service https admin-state disable\n")
                    continue
                elif service == "network-time":
                    outputFile.write("ip service ntp admin-state disable\n")
                    continue
                else:
                    outputFile.write("ip service " + service +
                                     " admin-state disable\n")
                    continue

        # ip interface
        if re.match(r'(ip\sinterface\s.+\saddress\s.+\smask\s.+\svlan.+)', line):
            outputFile.write(listToString(re.findall(
                r'(ip\sinterface\s.+\saddress\s.+\smask\s.+\svlan\s\d+)', stripedLine)) + "\n")
            continue

        # ip interface dhcp-client
        if re.match(r'(ip\sinterface\sdhcp-client\svlan\s\d+)', line):
            outputFile.write(listToString(re.findall(
                r'(ip\sinterface\sdhcp-client\svlan\s\d+)', stripedLine)) + "\n")
            continue

        # ip mulitcast
        if re.match(r'(ip\smulticast\sstatus\senable)', line):
            mulitcastStatus = listToString(
                re.findall(r'(?<=status ).*$', stripedLine))
            outputFile.write("ip multicast admin-state " +
                             mulitcastStatus+"\n")
            continue

        # IPMS
        if re.match(r'ip\smulticast\s(querying|querier-forwarding)\s(enable|disable)', line):
            outputFile.write(line)
            continue

        # tacaus server
        if re.match(r'(aaa\stacacs\+-server\s.+\shost\s.+\skey\s.+\sport\s\d+\stimeout\s\d+)', line):
            outputFile.write(listToString(re.findall(
                r'(aaa\stacacs\+-server\s.+\shost\s.+\skey\s)', stripedLine)) + tacacsServerKey + " port " + listToString(re.findall(
                    r'(?<=port ).*$', stripedLine)) + "\n")
            continue

        # aaa authentication
        if re.match(r'(^aaa\sauthentication\s(default|console|telnet|ssh|snmp|http|ftp)\s)', line):
            outputFile.write(line)
            continue
        elif re.match(r'(^no\saaa\sauthentication\s(default|console|telnet|ssh|snmp|http|ftp)\s)', line):
            outputFile.write(line)
            continue

        if re.match(r'(user\spassword-(expiration\s\d+|policy\smin-(uppercase|digit|nonalpha)\s\d+|history\s\d+|min-age\s\d+))', line):
            outputFile.write(line)
            continue

        # Interface
        if re.match(r'interfaces\s\d+\/\d+\shybrid\scopper', line):
            HybridInterface = "/1/".join(stripedLine.split()[1].split("/"))
            HybridMode = stripedLine.split()[3]
            outputFile.write("interfaces " + HybridInterface +
                             " hybrid-mode " + HybridMode + "\n")
            continue

        # QOS
        if re.match(r'(policy\sport\sgroup\sUserPorts\s+)', stripedLine):
            UserPorts = listToString(re.findall(
                r'(?<=UserPorts ).*$', stripedLine)).split()
            userPortList = []
            for port in UserPorts:
                userPortList.append('/1/'.join(port.split("/")) + " ")
            outputFile.write("policy port group UserPorts " +
                             listToString(userPortList) + "\n")
            continue

        if re.match(r'policy\sservice\s\w+\s(source|destination)\stcp\sport\s\d+', stripedLine):
            outputFile.write(stripedLine.replace("tcp port", "tcp-port")+"\n")
            continue
        elif re.match(r'(^(policy|qos)\s(apply|trust|service|network|condition|action|rule))', stripedLine):
            outputFile.write(line)
            continue

        # Session Manager
        if re.match(r'(session\sbanner\scli\s.+)', line):
            addCommaToUsrInputStr("session cli banner")
            continue

        if re.match(r'(^command-log\s(enable|disable))', line):
            outputFile.write(line)
            continue

        if re.match(r'(session\sprompt\sdefault\s.+)', line):
            outputFile.write(line)
            continue

        if re.match(r'(session\stimeout\scli\s.+)', line):
            outputFile.write(line)
            continue

        # SNMP
        if re.match(r'(^snmp\s(security|station\s))', line):
            outputFile.write(line)
            continue

        if re.match(r'(snmp\sauthentication\strap)', line):
            outputFile.write("snmp authentication-trap " + listToString(re.findall(
                r'(?<=trap ).*$', stripedLine)) + "\n")
            continue

        # IP route
        if re.match(r'(^ip\sstatic-route\s.+)', line):
            outputFile.write(line)
            continue

        # IP route
        if re.match(r'(^interfaces\s\d+\/\d+\s(alias|duplex|speed))', line):
            toExtract = listToString(re.findall(
                r'(?<=interfaces ).*$', stripedLine))
            port = toExtract.split()[0].split(
                "/")[0] + "/1/" + toExtract.split()[0].split("/")[1]
            outputFile.write("interfaces port " + port + " " +
                             listToString(toExtract.split()[1:], 1) + "\n")
            continue
        if re.match(r'(^trap\s\d+\/\d+\sport\slink\senable)', line):
            portlinkStatus = stripedLine.split()[-1]
            toExtract = listToString(re.findall(
                r'(?<=trap ).*$', stripedLine))
            port = toExtract.split()[0].split(
                "/")[0] + "/1/" + toExtract.split()[0].split("/")[1]
            outputFile.write("interfaces port " + port +
                             " link-trap "+portlinkStatus+"\n")
            continue

        if re.match(r'(^interfaces\s\d+\/\d+\sadmin\sdown)', line):
            interfaceStatus = stripedLine.split()[-1]
            toExtract = listToString(re.findall(
                r'(?<=interfaces ).*$', stripedLine))
            port = toExtract.split()[0].split(
                "/")[0] + "/1/" + toExtract.split()[0].split("/")[1]

            if interfaceStatus == "down":
                outputFile.write("interfaces port " + port +
                                 " admin-state disable\n")
                continue
            else:
                outputFile.write("interfaces port " + port +
                                 " admin-state enable\n")
                continue

        # Link Aggregate
        if re.match(r'(^lacp\slinkagg\s\d+\ssize\s\d+\sadmin\sstate\s(enable|disable))', line):
            aggId = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[0]
            linkaggSize = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[2]
            linkaggStatus = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[-1]
            outputFile.write("linkagg lacp agg "+aggId+" size " +
                             linkaggSize+" admin-state "+linkaggStatus+"\n")
            continue
        elif re.match(r'(^lacp\slinkagg\s\d+\sname)', line):
            aggId = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[0]
            outputFile.write("linkagg lacp agg " + aggId + ' name "' + listToString(re.findall(
                r'(?<=name ).*$', stripedLine)).strip('"') + '"\n')
            continue
        elif re.match(r'(^lacp\slinkagg\s\d+\sactor\sadmin\skey\s)', line):
            aggId = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[0]
            adminKey = listToString(re.findall(
                r'(?<=linkagg ).*$', stripedLine)).split()[-1]
            outputFile.write("linkagg lacp agg "+aggId +
                             " actor admin-key "+adminKey+"\n")
            continue
        elif re.match(r'(^lacp\sagg\s\d+\/\d+\sactor\sadmin\skey\s)', line):
            aggInterfaces = listToString(re.findall(
                r'(?<=agg ).*$', stripedLine)).split()[0].split("/")[0] + "/1/" + listToString(re.findall(
                    r'(?<=agg ).*$', stripedLine)).split()[0].split("/")[1]
            adminKey = listToString(re.findall(
                r'(?<=agg ).*$', stripedLine)).split()[-1]
            outputFile.write("linkagg lacp port "+aggInterfaces +
                             " actor admin-key "+adminKey+"\n")
            continue

        # Spanning Tree
        if re.match(r'(bridge\smode\s1x1)', line):
            outputFile.write('mvrp disable\n')
            outputFile.write('spantree mode per-vlan\n')
            continue
        elif re.match(r'(bridge\smode\sflat)', line):
            outputFile.write('spantree mode flat\n')
            continue
        if re.match(r'(bridge\s+1x1\s\d+\s\d+\s)', line):
            vlanId = stripedLine.split()[2]
            linkaggId = stripedLine.split()[3]
            stpStatus = stripedLine.split()[-1]
            outputFile.write("spantree vlan " + vlanId + " linkagg " +
                             linkaggId + " " + stpStatus + "\n")
            continue
        if re.match(r'(bridge\s+1x1\s\d+\s\d+\/\d+\s)', line):
            vlanId = stripedLine.split()[2]
            sptInterface = stripedLine.split()[3].split(
                "/")[0] + "/1/" + stripedLine.split()[3].split("/")[-1]
            stpStatus = stripedLine.split()[-1]
            outputFile.write("spantree vlan " + vlanId + " port " +
                             sptInterface + " " + stpStatus + "\n")
            continue

        # Port Security
        if re.match(r'(port-security\s\d+\/\d+\sadmin-status)', line):
            portSecInt = stripedLine.split()[1].split(
                "/")[0] + "/1/" + stripedLine.split()[1].split("/")[1]
            portSecState = stripedLine.split()[-1]
            tempFile.write("port-security port " + portSecInt +
                           " admin-state " + portSecState + "\n")
            if portSecState == "enable":
                portSecEnaCount = portSecEnaCount + 1
            else:
                portSecDisCount = portSecDisCount + 1
            continue
        if re.match(r'(port-security\s\d+\/\d+\smaximum)', line):
            portSecInt = stripedLine.split()[1].split(
                "/")[0] + "/1/" + stripedLine.split()[1].split("/")[1]
            portSecMaximum = stripedLine.split()[-1]
            tempFile.write("port-security port " + portSecInt +
                           " maximum " + portSecMaximum + "\n")
            portSecMaxCount = portSecMaxCount + 1
            continue
        if re.match(r'port-security\s\d+\/\d+\smax-filtering\s\d+', line):
            portSecInt = "/1/".join(stripedLine.split()[1].split('/'))
            portSecMacFiltering = stripedLine.split()[-1]
            outputFile.write("port-security port " + portSecInt +
                             " max-filtering " + portSecMacFiltering + "\n")
            continue

        # System Service
        if re.match(r'((swlog|ip)\s(output|name-server|domain-lookup$|console)|\s(socket|level))', line):
            outputFile.write(line)
            continue

        # NTP
        if re.match(r'(ntp\sserver\s)', line):
            outputFile.write(line)
            continue

        if re.match(r'ntp\sclient\s(enable|disable)', line):
            ntpStatus = stripedLine.split()[-1]
            outputFile.write("ntp client admin-state " + ntpStatus + "\n")
            continue

        # LLDP
        if re.match(r'(lldp\s(network-policy|chassis)\s(\d+|tlv|med)\s(application|med|network-policy)\s+(voice|network-policy|\d+))', line):
            outputFile.write(line)
            continue
        if re.match(r'lldp\s\d+\/\d+\stlv\smed\s+network-policy\s(enable|disable)', line):
            lldpInt = "/1/".join(stripedLine.split()[1].split("/"))
            lldpNetPolicStatus = stripedLine.split()[-1]
            outputFile.write("lldp port " + lldpInt + " tlv med network-policy " +
                             lldpNetPolicStatus + "\n")
            continue

        if re.match(r'lldp\s\d+\/\d+\smed\snetwork-policy\s\d+', line):
            lldpInt = "/1/".join(stripedLine.split()[1].split("/"))
            lldpNetPolicNo = stripedLine.split()[-1]
            outputFile.write("lldp port " + lldpInt + " med network-policy " +
                             lldpNetPolicStatus + "\n")
            continue

        # UDP Relay
        if re.match(r'ip\shelper\sdhcp-snooping\s(enable|disable)', line):
            dhcpSnoopingStatus = stripedLine.split()[-1]
            outputFile.write("dhcp-snooping admin-state " +
                             dhcpSnoopingStatus + "\n")
            continue
        if re.match(r'ip\shelper\sdhcp-snooping\sbinding\s(enable|disable)', line):
            dhcpSnoopingStatus = stripedLine.split()[-1]
            outputFile.write("dhcp-snooping binding admin-state " +
                             dhcpSnoopingStatus + "\n")
            continue
        if re.match(r'ip\shelper\sdhcp-snooping\slinkagg\s', line):
            outputFile.write(stripedLine.replace("ip helper ", "") + "\n")
            continue

        if re.match(r'ip\shelper\sdhcp-snooping\sport\s', line):
            dhcpSnoopingInt = "/1/".join(stripedLine.split()[-2].split("/"))
            dhcpSnoopingTrust = stripedLine.split()[-1]
            outputFile.write("dhcp-snooping port " +
                             dhcpSnoopingInt + " " + dhcpSnoopingTrust + "\n")
            continue

        # lanpower
        if re.match(r'lanpower\s(start|stop)\s\d+', line):
            slot = stripedLine.split()[-1]
            lanpowerStatus = stripedLine.split()[1]
            outputFile.write("lanpower slot " + slot +
                             "/1 service " + lanpowerStatus + "\n")
            continue

    print(stripedLine)
print("\n============================(End of Convertion)============================")
print("\nLines above are not able to be converted.")
print("\nYou can find the converted configuration in the following directory.\n")
print(os.getcwd() + "\\" + outputfilename)

while (res := input("\nDo you wish to continue converting another file? (y/n): ").lower()) not in {"y", "n"}:
    pass
if res == "y":
    os.system('AOS6_2_8.py')
    exit()
else:
    exit()

inputFile.close()
tempFile.close()

######################## UNP ########################
if portMobile == "y":
    outputFile.write("unp profile " + voiceVlanName + " mobile-tag\n")
    outputFile.write("unp profile " + defaultVlanName + " mobile-tag\n")
    outputFile.write("unp profile " + voiceVlanName +
                     " map vlan " + str(voiceVlan) + "\n")
    outputFile.write("unp profile " + defaultVlanName +
                     " map vlan " + str(defaultVlan) + "\n")
    outputFile.write("unp port-template voice-template direction both default-profile " +
                     defaultVlanName + " classification trust-tag admin-state enable \n")

######################## Interface range ########################
tempFile = open("temp.txt", "r")

switchport = 0
unpSwitchport = 0
portSecEnaPort = 0
portSecDisPort = 0
portSecMaxPort = 0
vlanId = 0
portMax = 0
vlanRange = ""
rangeUNP = ""
portSecEnaRange = ""
portSecDisRange = ""
portSecMaxRange = ""
vlanIntChassis = ""
unpIntChassis = ""
portSecEnaIntChassis = ""
portSecDisIntChassis = ""
portSecMaxIntChassis = ""


for line in tempFile.readlines():

    stripedLine = line.strip()
    # Range untagged port
    if re.match(r'(vlan\s\d+.members\sport\s\d+\/\d+\/\d+\suntagged)', line):

        if not vlanId is int(stripedLine.split()[1]):  # is it same vlan?

            vlanId = int(stripedLine.split()[1])

            vlanIntChassis = getInterfaceChassis(stripedLine)

            switchport = getSwitchport(stripedLine)

            vlanRange = taggedRange(
                vlanId, vlanIntChassis, switchport, "untagged")

        elif vlanId is int(stripedLine.split()[1]):   # the vlan is the same

            if vlanIntChassis == getInterfaceChassis(stripedLine):
                # if switchport is continuous

                if getSwitchport(stripedLine) - switchport == 1:
                    switchport = getSwitchport(stripedLine)
                    if vlanUntagCount <= 1:
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " untagged\n")
                else:  # switchport is not continuos
                    if not listToString(re.findall(
                            r'(?<=\/1\/).*$', vlanRange)).split(" ")[0] == str(switchport):
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " untagged\n")

                    switchport = getSwitchport(stripedLine)

                    vlanRange = taggedRange(
                        vlanId, vlanIntChassis, switchport, "untagged")
            else:
                vlanId = int(stripedLine.split()[1])

                vlanIntChassis = getInterfaceChassis(stripedLine)

                switchport = getSwitchport(stripedLine)

                vlanRange = taggedRange(
                    vlanId, vlanIntChassis, switchport, "untagged")
        vlanUntagCount = vlanUntagCount - 1

    # Range tagged port
    elif re.match(r'(vlan\s\d+.members\sport\s\d+\/\d+\/\d+\stagged)', line):

        if not vlanId is int(stripedLine.split()[1]):  # is it same vlan?

            vlanId = int(stripedLine.split()[1])

            vlanIntChassis = getInterfaceChassis(stripedLine)

            switchport = getSwitchport(stripedLine)

            vlanRange = taggedRange(
                vlanId, vlanIntChassis, switchport, "tagged")

        elif vlanId is int(stripedLine.split()[1]):   # the vlan is the same

            if vlanIntChassis == getInterfaceChassis(stripedLine):

                # if switchport is continuous
                if getSwitchport(stripedLine) - switchport == 1:

                    switchport = getSwitchport(stripedLine)
                    if vlanUntagCount <= 1:
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " tagged\n")
                else:  # switchport is not continuos

                    if not listToString(re.findall(
                            r'(?<=\/1\/).*$', vlanRange)).split(" ")[0] == str(switchport):
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " tagged\n")

                    switchport = getSwitchport(stripedLine)

                    vlanRange = taggedRange(
                        vlanId, vlanIntChassis, switchport, "tagged")
            else:
                vlanId = int(stripedLine.split()[1])

                vlanIntChassis = getInterfaceChassis(stripedLine)

                switchport = getSwitchport(stripedLine)

                vlanRange = taggedRange(
                    vlanId, vlanIntChassis, switchport, "tagged")
        vlanTaggedCount = vlanTaggedCount - 1

    # Range unp port
    if re.match(r'(unp\sport\s\d\/\d\/\d+\sport-type\sbridge)', line):
        if unpIntChassis == getInterfaceChassis(stripedLine):
            if getSwitchport(stripedLine) - unpSwitchport == 1:
                unpSwitchport = getSwitchport(stripedLine)
                if unpCount <= 1:
                    outputFile.write(
                        rangeUNP + "-" + str(unpSwitchport) + " port-type bridge\n")
                    outputFile.write(
                        rangeUNP + "-" + str(unpSwitchport) + " port-template voice-template\n")
            else:
                if not listToString(re.findall(r'(?<=\/1\/).*$', rangeUNP)).split(" ")[0] == str(unpSwitchport):
                    outputFile.write(
                        rangeUNP + "-" + str(unpSwitchport) + " port-type bridge\n")
                    outputFile.write(
                        rangeUNP + "-" + str(unpSwitchport) + " port-template voice-template\n")
                unpSwitchport = getSwitchport(stripedLine)
                rangeUNP = unpRange(unpIntChassis,
                                    unpSwitchport)
        else:
            unpIntChassis = getInterfaceChassis(stripedLine)

            unpSwitchport = getSwitchport(stripedLine)

            rangeUNP = unpRange(unpIntChassis,
                                unpSwitchport)
        unpCount = unpCount - 1
    # Range port security enabled port
    if re.match(r'(port-security\sport\s\d+\/\d+\/\d+\sadmin-state\senable)', line):
        if portSecEnaIntChassis == getInterfaceChassis(stripedLine):
            if getSwitchport(stripedLine) - portSecEnaPort == 1:
                portSecEnaPort = getSwitchport(stripedLine)
                if portSecEnaCount <= 1:
                    outputFile.write(
                        portSecEnaRange + "-" + str(portSecEnaPort) + " admin-state enable\n")
            else:
                if not listToString(re.findall(r'(?<=\/1\/).*$', portSecEnaRange)).split(" ")[0] == str(portSecEnaPort):
                    outputFile.write(
                        portSecEnaRange + "-" + str(portSecEnaPort) + " admin-state enable\n")
                portSecEnaPort = getSwitchport(stripedLine)
                portSecEnaRange = portSecPortRange(portSecEnaIntChassis,
                                                   portSecEnaPort)
        else:
            portSecEnaIntChassis = getInterfaceChassis(
                stripedLine)

            portSecEnaPort = getSwitchport(stripedLine)

            portSecEnaRange = portSecPortRange(portSecEnaIntChassis,
                                               portSecEnaPort)
        portSecEnaCount = portSecEnaCount - 1

    # Range port security diabled port
    if re.match(r'(port-security\sport\s\d+\/\d+\/\d+\sadmin-state\sdisable)', line):
        if portSecDisIntChassis == getInterfaceChassis(stripedLine):
            if getSwitchport(stripedLine) - portSecDisPort == 1:
                portSecDisPort = getSwitchport(stripedLine)
                if portSecDisCount <= 1:
                    outputFile.write(
                        portSecDisRange + "-" + str(portSecDisPort) + " admin-state disable\n")
            else:
                if not listToString(re.findall(r'(?<=\/1\/).*$', portSecDisRange)).split(" ")[0] == str(portSecDisPort):
                    outputFile.write(
                        portSecDisRange + "-" + str(portSecDisPort) + " admin-state disable\n")
                portSecDisPort = getSwitchport(stripedLine)
                portSecDisRange = portSecPortRange(portSecDisIntChassis,
                                                   portSecDisPort, "disable")
        else:
            portSecDisIntChassis = getInterfaceChassis(
                stripedLine)

            portSecDisPort = getSwitchport(stripedLine)

            portSecDisRange = portSecPortRange(portSecDisIntChassis,
                                               portSecDisPort, "disable")
        portSecDisCount = portSecDisCount - 1

# def portSecMaxPortRange(portMax, interfaceChassis, switchport):
#     range = "port-security port " + interfaceChassis + "/1/" + str(switchport)
#     outputFile.write(range + " maximum " + str(portMax) + "\n")
#     return range

    # Range port security max port
    if re.match(r'(port-security\sport\s\d+\/\d+\/\d+\smaximum)', line):
        # print(stripedLine.split()[-1])
        if not portMax is int(stripedLine.split()[-1]):  # is it same vlan?

            portMax = int(stripedLine.split()[-1])

            portSecMaxIntChassis = getInterfaceChassis(stripedLine)

            portSecMaxPort = getSwitchport(stripedLine)

            portSecMaxRange = portSecMaxPortRange(
                portMax, portSecMaxIntChassis, portSecMaxPort)

        elif portMax is int(stripedLine.split()[-1]):   # the vlan is the same

            if portSecMaxIntChassis == getInterfaceChassis(stripedLine):
                # if portSecMaxPort is continuous

                if getSwitchport(stripedLine) - portSecMaxPort == 1:
                    portSecMaxPort = getSwitchport(stripedLine)
                    if portSecMaxCount <= 1:
                        outputFile.write(
                            portSecMaxRange + "-" + str(portSecMaxPort) + " maximum " + str(portMax) + "\n")
                else:  # portSecMaxPort is not continuos
                    if not listToString(re.findall(
                            r'(?<=\/1\/).*$', portSecMaxRange)).split(" ")[0] == str(portSecMaxPort):
                        outputFile.write(
                            portSecMaxRange + "-" + str(portSecMaxPort) + " maximum " + str(portMax) + "\n")

                    portSecMaxPort = getSwitchport(stripedLine)

                    portSecMaxRange = portSecMaxPortRange(
                        portMax, portSecMaxIntChassis, portSecMaxPort)
            else:
                portMax = int(stripedLine.split()[-1])

                portSecMaxIntChassis = getInterfaceChassis(stripedLine)

                portSecMaxPort = getSwitchport(stripedLine)

                portSecMaxRange = portSecMaxPortRange(
                    portMax, portSecMaxIntChassis, portSecMaxPort)
        portSecMaxCount = portSecMaxCount - 1

tempFile.close()

outputFile.close()
# os.remove("temp.txt")
