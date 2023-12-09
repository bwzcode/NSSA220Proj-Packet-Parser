from packet_parser import *
import csv
def compute():
	print('called compute function in compute_metrics.py')
	#gather all the parsed data
	data1, data2, data3, data4 = parse()
	for i in range(4):
		current=[]
		node_add=''
		same_net_add=''
		request_sent=0			#data size metric 1
		request_received=0		#data size metric 2
		reply_sent=0			#data size metric 3
		reply_received=0		#data size metric 4
		request_sent_length=0		#data size metric 5
		request_received_length=0	#data size metric 6
		request_sent_data=0		#data size metric 7
		request_received_data=0		#data size metric 8
		ping_rtt_pt1=0.0		#time based metric 1
		ping_rtt_pt2=0.0
		ping_rtt_final=0.0
		ping_rtt_counter=0
		frame_sizes=0.0			#time based metric 2
		throughput=0.0
		payload_sizes=0.0		#time based metric 3
		goodput=0.0
		reply_delay_pt1=0.0		#time based metric 4
		reply_delay_pt2=0.0
		reply_delay_final=0.0
		reply_delay_counter=0
		hop_count=0.0			#distance metric
		req_counter=0
		if i==0:
			current=data1
			node_add='192.168.100.1'
			same_net_add='192.168.100.2'
			output=open('metric_output.csv', mode='w')
		elif i==1:
			current=data2
			node_add='192.168.100.2'
			same_net_add='192.168.100.1'
			output=open('metric_output.csv', mode='a')
		elif i==2:
			current=data3
			node_add='192.168.200.1'
			same_net_add='192.168.200.2'
			output=open('metric_output.csv', mode='a')
		elif i==3:
			current=data4
			node_add='192.168.200.2'
			same_net_add='192.168.200.1'
			output=open('metric_output.csv', mode='a')
		for j in current:
			thelen=int(j[5])
			if "Echo (ping) request" in j[6]:
				if node_add in j[2]:
					if same_net_add in j[3]:
						hop_count=hop_count+1
					else:
						hop_count=hop_count+3
					req_counter=req_counter+1
					ping_rtt_pt1=float(j[1])
					request_sent=request_sent+1
					frame_sizes=frame_sizes+thelen
					payload_sizes=payload_sizes+thelen-42
					request_sent_length=request_sent_length+thelen
					request_sent_data=request_sent_data+thelen-42
				else:
					reply_delay_pt1=float(j[1])
					if node_add in j[3]:
						request_received=request_received+1
						request_received_length=request_received_length+thelen
						request_received_data=request_received_data+thelen-42
					else:
						ping_rtt_pt1=float(j[1])
			elif "Echo (ping) reply" in j[6]:
				if node_add in j[2]:
					reply_sent=reply_sent+1
					reply_delay_pt2=float(j[1])
					reply_delay_final=reply_delay_final+((reply_delay_pt2-reply_delay_pt1)*1000000)
					reply_delay_counter=reply_delay_counter+1
				else:
					ping_rtt_pt2=float(j[1])
					ping_rtt_final=ping_rtt_final+((ping_rtt_pt2-ping_rtt_pt1)*1000)
					ping_rtt_counter=ping_rtt_counter+1
					if node_add in j[3]:
						reply_received=reply_received+1
					else:
						reply_delay_pt2=float(j[1])
						reply_delay_final=reply_delay_final+((reply_delay_pt2-reply_delay_pt1)*1000000)
						reply_delay_counter=reply_delay_counter+1
		throughput=frame_sizes/ping_rtt_final
		goodput=payload_sizes/ping_rtt_final
		ping_rtt_final=ping_rtt_final/ping_rtt_counter
		reply_delay_final=reply_delay_final/reply_delay_counter
		hop_count=hop_count/req_counter
		Node = 'Node ' + str(i+1)
		output_writer=csv.writer(output, delimiter=',')
		output_writer.writerow([Node])
		output_writer.writerow([None])
		output_writer.writerow(['Echo Requests Sent', 'Echo Requests Received', 'Echo Replies Sent', 'Echo Replies Received'])
		output_writer.writerow([request_sent, request_received, reply_sent, reply_received])
		output_writer.writerow(['Echo Request Bytes Sent (bytes)', 'Echo Request Data Sent (bytes)'])
		output_writer.writerow([request_sent_length, request_sent_data])
		output_writer.writerow(['Echo Request Bytes Received (bytes)', 'Echo Request Data Received'])
		output_writer.writerow([request_received_length, request_received_data])
		output_writer.writerow([None])
		output_writer.writerow(['Average RTT (milliseconds)', round(ping_rtt_final, 2)])
		output_writer.writerow(['Echo Request Throughput (kB/sec)', round(throughput, 2)])
		output_writer.writerow(['Echo Request Goodput (kB/sec)', round(goodput, 2)])
		output_writer.writerow(['Average Reply Delay (microseconds)', round(reply_delay_final, 2)])
		output_writer.writerow(['Average Echo Request Hop Count', round(hop_count, 2)])
		output_writer.writerow([None])
		output.close()
compute()
