import re

event_types = ['delay',
               'suspende{0,1}d{0,1}\s',
               'rerout'
               ]
event_status = ['\sended',
                'resume\s',
                'resumed',
                'resuming'
                ]
event_codes = ['temp',
               'temporary',
               'emergency'
               ]
incident_reasons = ['medical',
                    'equipment',
                    'signal',
                    'switch',
                    'door',
                    'police',
                    'mechanical',
                    'track',
                    'fire',
                    'sick'
                    ]
lines = ['red',
         'brown',
         'blue',
         'yellow',
         'green',
         'purple'
         ]

def read_credentials(credentials_file):
    credentials = {}
    with open(credentials_file, 'rt') as f:
        for row in f:
            row_split = row.split(' ')
            credentials[row_split[0]] = re.sub('\n', '', row_split[1])
    return credentials


def regexp_from_list(val_list):
    regexp_str = '|'.join(val_list)
    regexp = re.compile(regexp_str)
    return regexp

def parse_groups(regexp_search):
    groups = []
    if regexp_search:
        for i in range(10):
            try:
                g = regexp_search.group(i)
                if g:
                    groups.append(g)
            except IndexError:
                break
    else:
        groups = None

    if groups:
        groups = ','.join(groups)
    return groups

def return_event_data(txt):
    txt_orig = txt
    txt = txt.lower()
    types = re_event_types.search(txt)
    codes = re_event_code.search(txt)
    reasons = re_reasons.search(txt)

    statuses = re_event_status.search(txt)
    buses = re_bus.search(txt)
    direction = re_direction.search(txt)
    location = re_location.search(txt)
    region = re_region.search(txt)

    this_type = parse_groups(types)
    this_code = parse_groups(codes)
    this_reason = parse_groups(reasons)
    this_status = parse_groups(statuses)

    l_lines = re_l_line.findall(txt)
    if len(l_lines) == 0:
        l_lines = None
    else:
        l_lines = ','.join(l_lines)

    if buses:
        this_bus = buses.groupdict()['bus_number']
    else:
        this_bus = None
    if direction:
        this_direction = direction.groupdict()['direction']#.strip()
    else:
        this_direction = None
    if location:
        this_location = location.groupdict()['location']#.strip()
    else:
        this_location = None
    if region:
        this_from = region.groupdict()['from']
        this_to = region.groupdict()['to']
    else:
        this_from, this_to = None, None
        
    out = {'type': this_type,
           'code': this_code,
           'reason': this_reason,
           'bus': this_bus,
           'l_line': l_lines,
           'location': this_location,
           'direction': this_direction,
           'status': this_status,
           'msg': txt_orig,
           'from_loc': this_from,
           'to_loc': this_to
           }
    return out

re_event_types = regexp_from_list(event_types)
re_event_status = regexp_from_list(event_status)
re_event_code = regexp_from_list(event_codes)
re_reasons = regexp_from_list(incident_reasons)
re_l_line = regexp_from_list(lines)

re_bus = re.compile('(?P<bus_number>[0-9].*?)bus(es){0,1}')
re_location = re.compile('\s(at|near)\s(?P<location>[a-zA-Z0-9/]+)')
re_event_reason = re.compile('due to (?P<reason>[a-zA-Z0-9]+)?(at|near|\.)')
re_direction = re.compile('(?P<direction>[\w\'/]+)\-{0,1}bound')
re_region = re.compile('between\s(?P<from>\w+)\sand\s(?P<to>\w+)')
