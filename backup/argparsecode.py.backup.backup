import argparse

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-host", "--hostname", dest = "hostname", default = "xyz.edu", help="Server name")
parser.add_argument("-db", "--database", dest = "db", default = "ding_dong", help="Database name")
parser.add_argument("-u", "--username",dest ="username", help="User name")
parser.add_argument("-p", "--password",dest = "password", help="Password")
parser.add_argument("-size", "--binsize",dest = "binsize", help="Size", type=int)

args = parser.parse_args()

print( "Hostname {} db {} User {} Password {} size {} ".format(
        args.hostname,
        args.db,
        args.username,
        args.password,
        args.binsize
        ))