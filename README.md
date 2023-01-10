# aos6_2_8
Python Script to convert Alcatel Lucent OmniSwitch AOS Release 6 to 8 CLI

- This script was created using AOS6 6.4.4.645.R01 and AOS8 8.7.354.R01 syntax.
- Read & convert from 'show configuration snapshot' 
- Look below on the steps on how to run the script
- Only the following commands are converted:

system name [string]

system contact [string]

system location [string]

system timezone [timezone]

system daylight savings time [enable|disable]

mac-retention status [enable|disable]

vlan [int] enable name [string]

vlan [int] port default [switchport]

vlan [int] mobile-tag [enable|disable]

vlan [int] port default [switchport]

[no] ip service ftp

[no] ip service ssh

[no] ip service telnet

[no] ip service udp-relay

[no] ip service http

[no] ip service network-time

[no] ip service snmp

ip interface [string] address [IP address] mask [netmask] vlan [int]

ip multicast status [enable|disable]

aaa tacacs+-server [string] host [IP address] key [string] port 49

aaa authentication console [string]

aaa authentication snmp [string]

aaa authentication ssh [string]

user password-expiration [int]

user password-policy min-uppercase [int]

user password-policy min-digit [int]

user password-policy min-nonalpha [int]

user password-history [int]

user password-min-age [int]

qos trust ports user-port shutdown bpdu 

policy service ....

policy network group ...

policy port group UserPorts ...

policy condition ...

policy action ...

policy rule ...

qos apply

session banner [string]

session timeout cli [int]

session prompt default [string]

command-log [enable|disable]

snmp security authentication all

snmp authentication trap [enable|disable]

snmp station ...

ip static-route [IP address] gateway [IP address]

interfaces [switchport] alias [string]

interfaces [switchport] duplex [option]

interfaces [switchport] speed [int]

trap [switchport] port link [enable|disable]

interfaces [switchport] admin [down/up]

lacp linkagg [int] size [int] admin state [enable|disable]

lacp linkagg [int] name [string]

lacp linkagg [int] actor admin key [int]

lacp agg [switchport] actor admin key [21]

vlan [int] port default [linkagg]

vlan [int] 802.1q [switchport]

bridge mode 1x1 

bridge  1x1 [int] 1 [enable|disable] 

port-security [switchport] admin-status [enable|disable] 

port-security [switchport] maximum [int]

ip helper dhcp-snooping [enable|disable] 

ip helper dhcp-snooping binding [enable|disable] 

ip helper dhcp-snooping linkagg [int] trust

lanpower [start|stop] [int]

ntp server [IP address]

ip wccp admin-state [enable|disable] 

lldp network-policy [int] application voice vlan [int] l2-priority 5 dscp 0

lldp [int] tlv med  network-policy [enable|disable] 

lldp [int] med network-policy 1

# How to run the script

1. Download python. -> https://www.python.org/downloads/
2. Download script from here.
3. Run the script and hit enter on prompt,

![image](https://user-images.githubusercontent.com/55645717/150755102-70466b23-12a8-4d42-915f-b2e16f296c6f.png)

4. Select your AOS 6 confiugration and enter the neccessary information.

![image](https://user-images.githubusercontent.com/55645717/150755359-b996d9a5-53e1-4342-99dc-bbd5b2550a2c.png)
