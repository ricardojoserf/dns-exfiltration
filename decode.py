import base64
import argparse


def Decode(encoded_msg):
	decoded_msg = base64.b64decode(encoded_msg)
	decoded_string = decoded_msg.decode("utf-8")
	return decoded_string


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filter', required=True, action='store', help='Filter minutes')
	parser.add_argument('-l', '--logfile', required=True, action='store', help='Log file')
	my_args = parser.parse_args()
	return my_args


def GetMsg(logfile, filter):
	print("Reading the minutes " + filter + " from " + logfile)
	filter_array = filter.split(",")
	filtered_entries = ""
	log_entries = open(logfile).read().splitlines()
	for log in log_entries:
		for time in filter_array:
			if time in log:
				subdomain = log.split(" ")[1]
				filtered_entries += subdomain
	return filtered_entries


def main():
	args = get_args()
	enc_msg = GetMsg(args.logfile, args.filter)
	msg = Decode(enc_msg)
	print(msg)


if __name__== "__main__":
	main()
