import http.client
import json

conn = http.client.HTTPConnection('127.0.0.1', 8080, timeout=10)
#this heather defines type of hatt data= json 
headers = {'Content-type' : 'application/json'} 
#an example for json
json_txt = {"buffer": [
            {'id' : '001', 'date' : '30.04.1968 12:55', 'status' : '0'},
            {'id' : '001', 'date' : '30.04.1968 12:56', 'status' : '1'},
            {'id' : '001', 'date' : '30.04.1968 12:57', 'status' : '1'},
            {'id' : '001', 'date' : '30.04.1968 12:58', 'status' : '0'},
            {'id' : '001', 'date' : '30.07.1968 12:58', 'status' : '2'},
            {'id' : '001', 'date' : '30.06.1968 12:58', 'status' : '2'},
            {'id' : '001', 'date' : '30.05.1968 12:58', 'status' : '2'},
            {'id' : '001', 'date' : '31.04.1968 12:58', 'status' : '0'},
            {'id' : '001', 'date' : '30.04.1968 12:59', 'status' : '2'}
            ]
}
#dumps- converts text to jason 
json_data = json.dumps(json_txt)

#sends request to the server 
conn.request('POST', '/send_buffer', json_data, headers)

response = conn.getresponse()
print(response.read().decode())