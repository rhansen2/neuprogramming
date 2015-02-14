#!/usr/bin/python


DEFAULT_PREFIX_LEN = 24
IP_MAX = 0xFFFFFFFF
ADDR_LEN = 32

def prefixToInt(prefix):
    octets = prefix.split('.')
    value = 0;
    value = value | (int(octets[0]) << 24)
    value = value | (int(octets[1]) << 16)
    value = value | (int(octets[2]) << 8)
    return value

def prefixDistanceCorrect(x, y):
    if(x['prefix_len'] != y['prefix_len']):
        return False
    x_shift = ADDR_LEN - x['prefix_len']
    y_shift = ADDR_LEN - y['prefix_len']
    #print bin((x['value'] >> x_shift) ^ (y['value'] >> y_shift))
    return (x['value'] >> x_shift) ^ (y['value'] >> y_shift) == 0b1


# This is going to be called while iterating through a sorted list 
# of ip prefixes that means we always attempt to aggregate with the 
# last item in the list the last item is the first one that can't be 
# aggregated into the ones before  Another note since they're sorted, 
# if the prefixes arent consecutive they wont  be aggregated since we 
# do not want to add aditional prefixes not explicitly stated  
# For Example: 202.232.1.0/24 and 202.232.4.0/24 should not be aggregated to
# 202.232.0.0/21 because that includes 202.232.5.0/24 which is not part of 
# the list
def aggregatePrefix(prefixes):
    aggregated = []
    current_group = []
    group_index = 0
    i = 0
    while i <  len(prefixes):
        if (i + 1 >= len(prefixes)):
            aggregated.append(prefixes[i])
            return aggregated
        
        prefix = prefixes[i]
        test = prefixes[i+1]
        if (prefixDistanceCorrect(prefix, test)):
            prefix['prefix_len'] = prefix['prefix_len'] - 1
            aggregated.append(prefix)
        else:
            aggregated.append(prefix)
            i = i + 1
            continue
        i = i + 2 

    return aggregated
        
         

prefixes = [];
with open('prefixes.txt', 'r') as file:
    for line in file:
        prefixes.append({ 'prefix': line.rstrip(' \n'), 
                          'value': prefixToInt(line.rstrip(' \n')), 
                          'prefix_len': DEFAULT_PREFIX_LEN} )

prefixes.sort(key=lambda x: x['value'])
# Aggregate prefixes
aggregated = aggregatePrefix(prefixes);
count = len(aggregated)
oldCount = 0
# This isn't a very 'smart' way of doing the aggregation
# keep aggregating until we dont get any smaller
while count != oldCount:
    aggregated = aggregatePrefix(aggregated)
    oldCount = count
    count = len(aggregated)

total = 0
rawTotal = 0
# Add address range into prefixes
for agg in aggregated:
    agg['address_count'] = 2**(ADDR_LEN - agg['prefix_len']) - 2
    agg['address_count_raw'] = 2**(ADDR_LEN - agg['prefix_len'])
    total += 2**(ADDR_LEN - agg['prefix_len']) - 2
    rawTotal += 2**(ADDR_LEN - agg['prefix_len'])

for aggregate in aggregated:
    print 'Prefix:', aggregate['prefix'] + '/'+ str(aggregate['prefix_len']), 'Address Count:', aggregate['address_count'], 'Address Count Raw:', aggregate['address_count_raw']


print 'Total Addresses:', total
print 'Total Raw Addresses:', rawTotal




