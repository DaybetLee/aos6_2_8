import re
import os

########################################################


def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1


def taggedRange(vlanId, vlanInterfaceChassis, switchport, tagged):
    vlanRange = "vlan " + str(vlanId) + " members port " + \
        vlanInterfaceChassis + "/1/" + str(switchport)
    outputFile.write(vlanRange + " " + tagged + "\n")
    return vlanRange


def unpRange(interfaceChassis, switchport):
    range = "unp port " + interfaceChassis + "/1/" + str(switchport)
    outputFile.write(range + " port-type bridge\n")
    outputFile.write(range + " port-template voice-template\n")
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

########################################################


# portMobile = ""
tacacsServer = ""
# defaultVlan = 0
# voiceVlan = 0
tacacsServerKey = ""
defaultVlanName = ""
voiceVlanName = ""
vlanTaggedCount = 0
vlanUntaggedCount = 0
unpCount = 0
confirmation = "n"

# filename = input("Please enter the filename with extenesion: ")
# while not portMobile == "n" and not portMobile == "y":
#     portMobile = input("Is the switch using mobile tag? (y/n): ").lower()
# while defaultVlan < 1 and portMobile == "y":
#     defaultVlan = int(input(
#         "Please enter the default VLAN for port mobile [1-4096]: "))
# while voiceVlan < 1 and portMobile == "y":
#     voiceVlan = int(input(
#         "Please enter the voice VLAN for port mobile [1-4096]: "))
# while not tacacsServer == "n" and not tacacsServer == "y":
#     tacacsServer = input(
#         "Is the switch authenticate by TACACS Server? (y/n): ").lower()
# while tacacsServerKey == "" and tacacsServer == "y":
#     while confirmation == "n" and not confirmation == "y":
#         tacacsServerKey = input("Please enter the TACACS key: ")
#         confirmation = input("You have entered the TACACS key '" + tacacsServerKey +
#                              "' \nPlease confirm the key is entered correctly (y/n): ").lower()
#     confirmation = "n"
# input("\nPress any key to start the convertion:")


filename = "Original.txt"  # for development
portMobile = "y"  # for development
defaultVlan = 15  # for development
voiceVlan = 17  # for development
tacacsServerKey = "Neratel123+"  # for development

inputFile = open(filename, "r")
os.remove("AOS6_Converted_" + filename)  # for development
outputFile = open("AOS6_Converted_" + filename, "a")
tempFile = open("temp.txt", "w")

for line in inputFile.readlines()[1:290]:
    stripedLine = line.strip()
    if not stripedLine.endswith(":"):
        # print(stripedLine)
        ###########################################################
        # System name
        if re.match(r'(system\sname\s.+)', line):
            system_Name = stripedLine.strip("system name ").strip('"')
            # print("system name " + '"' + system_Name + '"')
            outputFile.write("system name " + '"' + system_Name + '"' + "\n")
        # System name
        if re.match(r'(system\scontact\s.+)', line):
            system_Contact = stripedLine.strip("system contact ").strip('"')
            # print("system contact " + '"' + system_Contact + '"')
            outputFile.write("system contact " + '"' +
                             system_Contact + '"' + "\n")
        # System location
        if re.match(r'(system\slocation\s.+)', line):
            system_Location = stripedLine.strip("system location ").strip('"')
            # print("system location " + '"' + system_Location + '"')
            outputFile.write("system location " + '"' +
                             system_Location + '"' + "\n")
        # System timezone
        if re.match(r'(system\stimezone\s.+)', line):
            outputFile.write("system timezone ZP8" + "\n")

        # System daylight saving
        if re.match(r'(system\sdaylight\ssavings\stime\sdisable)', line):
            outputFile.write("system daylight-savings-time enable\n")
        elif re.match(r'(system\sdaylight\ssavings\stime\senable)', line):
            outputFile.write("system daylight-savings-time enable\n")

        # mac-retention
        if re.match(r'(mac-retention\sstatus\senable)', line):
            outputFile.write("mac-retention admin-state enable\n")
        elif re.match(r'(mac-retention\sstatus\sdisable)', line):
            outputFile.write("mac-retention admin-state disable\n")

        # VLAN
        if stripedLine.startswith("vlan"):
            vlanId = stripedLine.split()[1]
            # enable VLAN and Name
            if re.match(r'(vlan\s\d+\senable\sname\s.+)', line):
                vlanName = stripeName(stripedLine)
                # print("vlan " + vlanId + " name " + vlanName)
                outputFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                tempFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                # print("vlan " + vlanId + " admin-state enable")
                outputFile.write("vlan " + vlanId +
                                 " admin-state enable" + "\n")
            # disable VLAN and Name
            elif re.match(r'(vlan\s\d+\sdisable\sname\s.+)', line):
                vlanName = stripeName(stripedLine)
                # print("vlan " + vlanId + " name " + vlanName)
                outputFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                tempFile.write("vlan " + vlanId + " name " + vlanName + "\n")
                # print("vlan " + vlanId + " admin-state disable")
                outputFile.write("vlan " + vlanId +
                                 " admin-state disable" + "\n")
            # vlan untagged
            if re.match(r'(vlan\s\d+\sport\sdefault.+)', line):
                vlanInterfaceChassis = listToString(re.findall(
                    r'(?<=default ).*$', stripedLine)).split("/")[0]
                vlanInterfacePort = listToString(re.findall(
                    r'(?<=default ).*$', stripedLine)).split("/")[1]
                # print("vlan " + vlanId + " members port " +
                #       vlanInterfaceChassis + "/1/" + vlanInterfacePort + " untagged")
                tempFile.write("vlan " + vlanId + " members port " +
                               vlanInterfaceChassis + "/1/" + vlanInterfacePort + " untagged" + "\n")
                vlanUntaggedCount = vlanUntaggedCount + 1

            # unp profile
            if re.match(r'vlan\s'+str(defaultVlan)+'\s(enable|disable)\sname\s.+', line):
                defaultVlanName = stripeName(stripedLine)
            elif re.match(r'(vlan\s\d+\smobile-tag\senable)', line):
                voiceVlanName = stripeName(stripedLine)

            # unp ports
            if re.match(r'(vlan\sport\smobile\s.+)', line):
                vlanInterfaceChassis = listToString(re.findall(
                    r'(?<=mobile ).*$', stripedLine)).split("/")[0]
                vlanInterfacePort = listToString(re.findall(
                    r'(?<=mobile ).*$', stripedLine)).split("/")[1]
                tempFile.write("unp port " +
                               vlanInterfaceChassis + "/1/" + vlanInterfacePort + " port-type bridge" + "\n")
                tempFile.write("unp port " +
                               vlanInterfaceChassis + "/1/" + vlanInterfacePort + " port-template voice-template" + "\n")
                unpCount = unpCount + 1

        # ip services (https and network syntax changed)
        if re.match(r'(no\sip\sservice\sftp)', line):
            outputFile.write("ip service ftp admin-state disable\n")
        elif re.match(r'(ip\sservice\sftp)', line):
            outputFile.write("ip service ftp admin-state enable\n")
        if re.match(r'(no\sip\sservice\sssh)', line):
            outputFile.write("ip service ssh admin-state disable\n")
        elif re.match(r'(ip\sservice\sssh)', line):
            outputFile.write("ip service ssh admin-state enable\n")
        if re.match(r'(no\sip\sservice\stelnet)', line):
            outputFile.write("ip service telnet admin-state disable\n")
        elif re.match(r'(ip\sservice\stelnet)', line):
            outputFile.write("ip service telnet admin-state enable\n")
        if re.match(r'(no\sip\sservice\shttp)', line):
            outputFile.write("ip service http admin-state disable\n")
        elif re.match(r'(ip\sservice\shttp)', line):
            outputFile.write("ip service http admin-state enable\n")
        if re.match(r'(no\sip\sservice\ssecure-http)', line):
            outputFile.write("ip service https admin-state disable\n")
        elif re.match(r'(ip\sservice\ssecure-http)', line):
            outputFile.write("ip service https admin-state enable\n")
        if re.match(r'(no\sip\sservice\ssnmp)', line):
            outputFile.write("ip service snmp admin-state disable\n")
        elif re.match(r'(ip\sservice\ssnmp)', line):
            outputFile.write("ip service snmp admin-state enable\n")
        if re.match(r'(no\sip\sservice\snetwork-time)', line):
            outputFile.write("ip service ntp admin-state disable\n")
        elif re.match(r'(ip\sservice\snetwork-time)', line):
            outputFile.write("ip service ntp admin-state enable\n")

        # ip interface
        if re.match(r'(ip\sinterface\s.+\saddress\s.+\smask\s.+\svlan.+)', line):
            outputFile.write(listToString(re.findall(
                r'(ip\sinterface\s.+\saddress\s.+\smask\s.+\svlan\s\d+)', stripedLine)) + "\n")

        # ip interface dhcp-client
        if re.match(r'(ip\sinterface\sdhcp-client\svlan\s\d+)', line):
            outputFile.write(listToString(re.findall(
                r'(ip\sinterface\sdhcp-client\svlan\s\d+)', stripedLine)) + "\n")

        # ip mulitcast
        if re.match(r'(ip\smulticast\sstatus\senable)', line):
            outputFile.write("ip multicast admin-state enable\n")
        elif re.match(r'(ip\smulticast\sstatus\sdisable)', line):
            outputFile.write("ip multicast admin-state disable\n")

        # tacaus server
        if re.match(r'(aaa\stacacs\+-server\s.+\shost\s.+\skey\s.+\sport\s\d+\stimeout\s\d+)', line):
            outputFile.write(listToString(re.findall(
                r'(aaa\stacacs\+-server\s.+\shost\s.+\skey\s)', stripedLine)) + tacacsServerKey + " port " + listToString(re.findall(
                    r'(?<=port ).*$', stripedLine)) + "\n")

        # aaa authentication
        if re.match(r'(^aaa\sauthentication\s(default|console|telnet|ssh|snmp|http|ftp)\s)', line):
            outputFile.write(stripedLine + "\n")
        elif re.match(r'(^no\saaa\sauthentication\s(default|console|telnet|ssh|snmp|http|ftp)\s)', line):
            outputFile.write(stripedLine + "\n")

        if re.match(r'(user\spassword-(expiration\s\d+|policy\smin-(uppercase|digit|nonalpha)\s\d+|history\s\d+|min-age\s\d+))', line):
            outputFile.write(stripedLine + "\n")

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
vlanId = 0
vlanRange = ""
rangeUNP = ""
vlanInterfaceChassis = ""
unpInterfaceChassis = ""


for line in tempFile.readlines():

    stripedLine = line.strip()
    # Range untagged port
    if re.match(r'(vlan\s\d+.members\sport\s\d+\/\d+\/\d+\suntagged)', line):

        if not vlanId is int(stripedLine.split()[1]):  # is it same vlan?

            vlanId = int(stripedLine.split()[1])

            vlanInterfaceChassis = getInterfaceChassis(stripedLine)

            switchport = getSwitchport(stripedLine)

            vlanRange = taggedRange(
                vlanId, vlanInterfaceChassis, switchport, "untagged")

        elif vlanId is int(stripedLine.split()[1]):   # the vlan is the same

            if vlanInterfaceChassis == getInterfaceChassis(stripedLine):
                # if switchport is continuous

                if getSwitchport(stripedLine) - switchport == 1:
                    switchport = getSwitchport(stripedLine)
                    if vlanUntaggedCount <= 1:
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " untagged\n")
                else:  # switchport is not continuos
                    if not listToString(re.findall(
                            r'(?<=\/1\/).*$', vlanRange)).split(" ")[0] == str(switchport):
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " untagged\n")

                    switchport = getSwitchport(stripedLine)

                    vlanRange = taggedRange(
                        vlanId, vlanInterfaceChassis, switchport, "untagged")
            else:
                vlanId = int(stripedLine.split()[1])

                vlanInterfaceChassis = getInterfaceChassis(stripedLine)

                switchport = getSwitchport(stripedLine)

                vlanRange = taggedRange(
                    vlanId, vlanInterfaceChassis, switchport, "untagged")
        vlanUntaggedCount = vlanUntaggedCount - 1
    # Range tagged port
    elif re.match(r'(vlan\s\d+.members\sport\s\d+\/\d+\/\d+\stagged)', line):
        print("it is kicked in")
        if not vlanId is int(stripedLine.split()[1]):  # is it same vlan?

            vlanId = int(stripedLine.split()[1])

            vlanInterfaceChassis = getInterfaceChassis(stripedLine)

            switchport = getSwitchport(stripedLine)

            vlanRange = taggedRange(
                vlanId, vlanInterfaceChassis, switchport, "tagged")

        elif vlanId is int(stripedLine.split()[1]):   # the vlan is the same

            if vlanInterfaceChassis == getInterfaceChassis(stripedLine):

                # if switchport is continuous
                if getSwitchport(stripedLine) - switchport == 1:

                    switchport = getSwitchport(stripedLine)
                    if vlanUntaggedCount <= 1:
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " tagged\n")
                else:  # switchport is not continuos

                    if not listToString(re.findall(
                            r'(?<=\/1\/).*$', vlanRange)).split(" ")[0] == str(switchport):
                        outputFile.write(
                            vlanRange + "-" + str(switchport) + " tagged\n")

                    switchport = getSwitchport(stripedLine)

                    vlanRange = taggedRange(
                        vlanId, vlanInterfaceChassis, switchport, "tagged")
            else:
                vlanId = int(stripedLine.split()[1])

                vlanInterfaceChassis = getInterfaceChassis(stripedLine)

                switchport = getSwitchport(stripedLine)

                vlanRange = taggedRange(
                    vlanId, vlanInterfaceChassis, switchport, "tagged")
        vlantaggedCount = vlantaggedCount - 1
    # Range unp port
    if re.match(r'(unp\sport\s\d\/\d\/\d+\sport-type\sbridge)', line):
        if unpInterfaceChassis == getInterfaceChassis(stripedLine):
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
                rangeUNP = unpRange(unpInterfaceChassis,
                                    unpSwitchport)
        else:
            unpInterfaceChassis = getInterfaceChassis(stripedLine)

            unpSwitchport = getSwitchport(stripedLine)

            rangeUNP = unpRange(unpInterfaceChassis,
                                unpSwitchport)
        unpCount = unpCount - 1

tempFile.close()

outputFile.close()
# os.remove("temp.txt")
