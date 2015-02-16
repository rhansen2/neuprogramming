#!/usr/bin/python

import json

ICMP_TYPE = 3
ICMP_CODE_HOST_UNREACHABLE = 1
ICMP_CODE_PORT_UNREACHABLE = 3

with open('./pingResults.json', "r") as input, open('./validResponses.json', "w") as output:
    for line in input:
        sample = json.loads(line)
        if( sample['ping_sent'] == 0 or len(sample['responses']) == 0):
            continue
        for response in sample['responses']:
            if( response['icmp_code']    != ICMP_CODE_HOST_UNREACHABLE 
               and response['icmp_type'] == ICMP_TYPE 
               and response['from']      == sample['dst']):
                output.write(json.dumps(sample, separators=(',',':'))) 
                output.write('\n')
                break

with open('./validResponses.json', "r") as responses, open('./finalResults.txt', "w") as output:
    for line in responses:
        test = json.loads(line)
        sameIpIds = 0
        for response in test['responses']:
            if(response['probe_ipid'] == response['reply_ipid']):
                sameIpIds += 1
        if (len(test['responses']) != sameIpIds):
            output.write(test['dst'])
            output.write('\n')

