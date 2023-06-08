import sys
import csv
import ipaddress
import os

output_f = open("test.csv","w")

class Entry:

    def __init__(
        self,
        timestamp: str,
        router_ip: ipaddress,
        peer_ip: ipaddress,
        peer_asn: int,
        prefix_ip: ipaddress,
        prefix_length: int,
        next_hop_ip: ipaddress,
        as_path,
        small_communities = [],
        large_communities = []
    ):
        self.timestamp = timestamp
        self.router_ip = router_ip
        self.peer_ip = peer_ip
        self.peer_asn = peer_asn
        self.prefix_ip = prefix_ip
        self.prefix_lengh = prefix_length
        self.next_hop_ip = next_hop_ip
        self.as_path = as_path
        self.small_communities = small_communities
        self.large_communities = large_communities
        
        self.writer = csv.writer(output_f,delimiter=',')
       
    def output(self):
        self.writer.writerow([self.timestamp, format(self.router_ip),
             format(self.peer_ip) , self.peer_asn ,
             format(self.prefix_ip) , self.prefix_lengh ,
             format(self.next_hop_ip) ,self.as_path,self.small_communities, self.large_communities])
        # result = "\"" +self.timestamp + "\"," + format(self.router_ip) + ","\
            # + format(self.peer_ip) + "," + self.peer_asn + ","\
            # + format(self.prefix_ip) + "," + self.prefix_lengh + ","\
            # + format(self.next_hop_ip) 
        # for community in self.small_communities:
        #     results += 
            #+ "," + self.as_path + ","\
            #+ self.small_communities + "," + self.large_communities

def is_ipv4_address(value: str) -> bool:
    
    return isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address)

def is_first_line(line):
    try:
        return (is_ipv4_address(line.split()[0].split("/")[0]))
    except ValueError as e:
        return False
    
def parse_first_line(line):
    tokens = line.split()
    # print(tokens)

    prefix_ip = tokens[0].split("/")[0]
    prefix_length = tokens[0].split("/")[1]
    date = tokens[3]
    time = tokens[4]
    router_ip = tokens[6].replace("]",'')
    
    return prefix_ip, prefix_length,date +" "+ time, router_ip
    
def main():
    f = open("route_dump.txt")
    line = f.readline()
    line = f.readline()
    flag = True
    while line:
        # entries = []
        prefix_ip, prefix_length, \
            datetime, router_ip = parse_first_line(line)
        # as_path = []
        community = []
        large_community = []
        # if(flag):
        line = f.readline()
            # flag = False
        # print(line
        
        while(not is_first_line(line)):
            
            # print(line)
            # print(is_first_line(line))
            # if(line.lstrip().startswith("Type")):
            #     continue
            # elif(line.lstrip().startswith("BGP.origin")):
            #     continue
            if(line.lstrip().startswith("BGP.as_path")):
                print(line)
                as_path = line.lstrip()[len("BGP.as_path:")+1:-1].replace("{","").replace("}","").split()
                as_path = list(map(int, as_path))

            elif(line.lstrip().startswith("BGP.next_hop")):
                next_hop = line.lstrip()[len("BGP.next_hop:")+1:-1]
            # elif(line.lstrip().startswith("BGP,local_pref")):
            elif(line.lstrip().startswith("BGP.community")):
                community = line.lstrip()[len("BGP.community:")+1:-1].split()
            elif(line.lstrip().startswith("BGP.large_community")):
                large_community = line.lstrip()[len("BGP.large_community")+1:-1].split()
            # else:
            #     print(line)
            #     print("BUG HERE")
            line = f.readline() 
            
        entry = Entry(datetime, router_ip, next_hop, as_path[0],
                      prefix_ip, prefix_length, next_hop, 
                      as_path, community,large_community)
        # line = f.readline()
        entry.output()

        # entries.append(entry)
        # import pdb
        # pdb.set_trace()
            
        
main()
    # entry_start = False
