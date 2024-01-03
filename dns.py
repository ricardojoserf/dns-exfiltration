import datetime
import socket
import argparse
from dnslib import DNSRecord

DNS_RECORD_TYPE_A = 1 # https://en.wikipedia.org/wiki/List_of_DNS_record_types


def listener(ns_subdomain, log_file):
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.bind(('0.0.0.0', 53))

	print("Monitoring DNS queries for subdomain " + ns_subdomain)
	print("Storing queries in " + log_file)

	log_entries = []
	while True:
		data, addr = server.recvfrom(4096)
		d = DNSRecord.parse(data)
		subdomain = str(d.questions[0]._qname).split(ns_subdomain)[0]

		# if (d.questions[0].qtype == DNS_RECORD_TYPE_A):
		now = datetime.datetime.now()
		current_time = now.strftime(f"%H:%M")
		log_entry = current_time + " " + subdomain
		one_min_ago = now - datetime.timedelta(minutes=1)
		one_min_ago_time = one_min_ago.strftime(f"%H:%M")
		log_entry_one_min_ago = one_min_ago_time + " " + subdomain

		# Note: I only log DNS queries not repeated in the last minute, if you want more you can uncomment the else statement but queries will be redundant
		if log_entry not in log_entries and log_entry_one_min_ago not in log_entries:
			print(log_entry)
			log_entries.append(log_entry)
			f = open(log_file, "a")
			f.write(log_entry + "\n")
			f.close()
		#else:
		#	print("Not adding the subdomain again to the list.")


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--logfile', required=False, action='store', default = "log.txt" , help='Log file. Default: log.txt')
	parser.add_argument('-s', '--subdomain', required=False, action='store', default = "exfil", help='Subdomain to monitor. Default: exfil')
	my_args = parser.parse_args()
	return my_args


def main():
	args = get_args()
	listener("."+args.subdomain, args.logfile)


if __name__== "__main__":
	main()
