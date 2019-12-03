#!/usr/bin/env python

from cortexutils.responder import Responder
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert
import requests
import json


class PowerAutomate(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.flow_master_controller = self.get_param('config.flow_master_controller', None, "Endpoint is Missing")
        self.thehive_instance = self.get_param('config.thehive_instance', 'localhost:9000')
        self.thehive_api_key  = self.get_param('config.thehive_api_key', 'YOUR_KEY_HERE')
        self.api = TheHiveApi(self.thehive_instance,self.thehive_api_key)
        self.Cert_Path = self.get_param('config.Cert_Path')


    def run(self):

        alertId = self.get_param('data.id')
        alertTitle = self.get_param('data.title')
        alertType = self.get_param('data.type')
        alertSource = self.get_param('data.source')
        alertSourceRef = self.get_param('data.sourceRef')
        alertDescription = self.get_param('data.description')
        alertTags = self.get_param('data.tags')
        alertArtifacts = self.get_param('data.artifacts')
        
        # Add a PowerAutomate tag to the alert

        if alertTags:

            if not 'PowerAutomate' in alertTags:    
                alertTags.append(u"PowerAutomate")
            
        else:
            print('no alert tags adding')
            alertTags = ["PowerAutomate"]


        # Output JSON blob
        json_data = {}
        use_case = []
        src = []
        dst = []
        email_subject = [] 
        
        for artifact in alertArtifacts:

            if artifact['message'] == 'use_case':
                use_case = artifact['data']

            if artifact['message'] == 'src':
                src = artifact['data']
            
            if artifact['message'] == 'dst':
                dst = artifact['data']

            if artifact['message'] == 'email_subject':
                email_subject.append(artifact['data'])
            
        headers = {
            'content-type': 'application/json'
        }

        data = {'alertId':alertId,'use_case': use_case, 'src': src, 'dst': dst, 'email_subject': email_subject}
        
        # Mark the alert as "read"
        self.api.mark_alert_as_read(alertId)

        if self.Cert_Path == '':
            r = requests.post(self.flow_master_controller, data=json.dumps(data), headers=headers)
        else:
            r = requests.post(self.flow_master_controller, data=json.dumps(data), headers=headers, verify=self.Cert_Path)

        if r.status_code == 200 or \
                r.status_code == 202 or \
                r.status_code == 409:
             
            self.report({'message': 'Workflow initiated.  Over to Power Automate.'})
        else:
            self.error({'message': r.status_code})

        self.report({'message': 'Workflow initiated.  Over to PowerAutomate.'})

if __name__ == '__main__':
    PowerAutomate().run()