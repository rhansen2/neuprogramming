#!/usr/bin/python

import json

ICMP_TYPE = 3
ICMP_CODE_HOST_UNREACHABLE = 1
ICMP_CODE_PORT_UNREACHABLE = 3

with open('./pingResults.json', "r") as input, open('./validResponses.json', "w") as output, \
        open('./validResponsesDiffIp.json', "w") as diffIp, open('./invalidResponse.json', "w") as invalid: 
    for line in input:
        sample = json.loads(line)
        if( sample['ping_sent'] != 0 and len(sample['responses']) != 0):
            for response in sample['responses']:
                 if( response['icmp_code']    == ICMP_CODE_PORT_UNREACHABLE
                    and response['icmp_type'] == ICMP_TYPE):
                     if(response['from'] == sample['dst']):
                        output.write(json.dumps(sample, separators=(',',':'))) 
                        output.write('\n')
                        break 
                     else:
                        diffIp.write(json.dumps(sample, separators=(',', ':')))
                        diffIp.write('\n')
                        break
                 else:
                    invalid.write(json.dumps(sample, separators=(',', ':')))
                    invalid.write('\n')
                    break
        else:
            invalid.write(json.dumps(sample, separators=(',', ':')))
            invalid.write('\n')

with open('./validResponses.json', "r") as responses, open('./finalResults.txt', "w") as output,\
        open ('./echoIpIdResults.txt', "w") as error:
    for line in responses:
        test = json.loads(line)
        sameIpIds = 0
        for response in test['responses']:
            if(response['probe_ipid'] == response['reply_ipid']):
                sameIpIds += 1

        if (len(test['responses']) != sameIpIds):
            output.write(test['dst'])
            output.write('\n')
        else:
            error.write(test['dst'])
            error.write('\n')

with open('./validResponsesDiffIp.json', "r") as responses, open('./finalResultsDiffIp.txt', "w") as output, \
        open('./echoIpIdDiffIpResults.txt', "w") as error:
    for line in responses:
        test = json.loads(line)
        sameIpIds = 0
        for responses in test["responses"]:
            if(response['probe_ipid'] == response['reply_ipid']):
                sameIpIds += 1

        if(len(test['responses']) != sameIpIds):
            output.write(test['dst'])
            output.write(': ')
            response = test['responses'][0]
            output.write(response['from'])
            
            output.write('\n')
        else:
            error.write(test['dst'])
            error.write(': ')
            response = test['responses'][0]
            error.write(response['from'])
            error.write('\n')
