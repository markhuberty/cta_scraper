#!/usr/bin/python 

import csv
import cta
import datetime
import time
import twitter
import asciidammit
import os


token_file = 'twitter_credentials.txt'
credentials = cta.read_credentials(token_file)

api = twitter.Api(consumer_key=credentials['consumer_key'],
                  consumer_secret=credentials['consumer_secret'],
                  access_token_key=credentials['oauth_token'],
                  access_token_secret=credentials['oauth_token_secret']
                  )

max_id = 0
all_messages = []
all_ids = []
all_times = []
cta_id = 'cta'
delay_interval = 600
output_path = '../data/cta_output.csv'
first_query = True

if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        reader = csv.DictReader(f)
        historic_ids = [row['id'] for row in reader]
    since_id = max(historic_ids)
    first_query=False
else:
    since_id = None
    
while True:
    query = api.GetUserTimeline(id=cta_id, since_id=since_id, count=100)

    if len(query) > 0:
        ids = [q.id for q in query]
        max_q_id = max(ids)
        since_id = max(since_id, max_q_id)

        times = [q.created_at for q in query]
        messages = [q.text for q in query]
        parsed_messages = [cta.return_event_data(m) for m in messages]

        for idx, t in enumerate(times):
            parsed_messages[idx]['time'] = t
            parsed_messages[idx]['id'] = ids[idx]

        with open(output_path, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=parsed_messages[0].keys())

            if first_query:
                header = dict(zip(writer.fieldnames, writer.fieldnames))
                writer.writerow(header)
                first_query = False
            for m in parsed_messages:
                for k in m:
                    if m[k] is not None:
                        if isinstance(m[k], str) or isinstance(m[k], unicode):
                            m[k] = m[k].encode('cp1252')
                            m[k] = asciidammit.asciiDammit(m[k])
                if m['bus'] or m['l_line']:
                    writer.writerow(m)

    print 'query done at ' + str(datetime.datetime.now())
    time.sleep(delay_interval)
