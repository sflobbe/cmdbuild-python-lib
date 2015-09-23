# module for CMDBuild interfacing
# Trying to follow https://www.python.org/dev/peps/pep-0008/
#
# Changelog
# 2015-09-23 J. Baten Initial version
#
#Copyright 2015 Deltares
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

__author__ = 'Jeroen Baten'
__copyright__   = "Copyright 2015, Deltares"

import requests
import json
from pprint import pprint

# from requests.auth import HTTPDigestAuth
import logging

version = "1.0"
#logger = logging.getLogger(__name__)


class cmdbuild:
    """CMDBuild interface class. Please see _dir_ for methods"""

    def check_valid_json(self,myjson):
        """Function to check is object passed is valid json
        Argument:
            object  json object to check
        Returns:
            true if valid json, otherwise false
        """
        try:
            json_object = json.loads(myjson)
        except ValueError, e:
            return False
        return True

    def info(self):
        """Return version information."""
        return "CMDBuild python lib version:" + version

    def connect(self, url, user, password):
        """Method to authenticate to cmdbuild server

        Parameters: url: url of server.
                    user: username to authenticate as.
                    password: password to use when authenticating.

        Returns: 0 if succesfull or 1 for failure.
        """
        if not url:
            raise exception( 'ERROR: No URL supplied')

        if not user:
            raise exception('ERROR: No username supplied')

        if not password:
            raise exception('ERROR: No password supplied')

        logging.debug("*** Login and get authentication token ")

        cmdbuild_url = url + "/services/rest/v2/sessions/"
        data = {'username': user, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        r = requests.post(cmdbuild_url, data=json.dumps(data), headers=headers)

        logging.debug(pprint((r.json())))
        r1 = r.json()
        sessionid = r1["data"]["_id"]
        logging.debug("sessionid=" + str(pprint(sessionid)))
        logging.info(" Authentication token : " + sessionid)

        if (len(str(sessionid)) > 1):
            self.url = url
            self.user = user
            self.password = password
            self.sessionid = sessionid
            return 0
        else:
            return 1

    def session_info(self):
        """Return information about the current session in json format"""
        logging.debug("*** Session info")
        cmdbuild_url = self.url + "/services/rest/v2/sessions/" + self.sessionid
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def lookup_types_info(self):
        """Return list of defined lookup types

           Return: Lookup types found (in json format).
        """
        logging.debug("*** lookup_types")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(r.json())
        return r.json()

    def lookup_type_values(self, id):
        """Return values for given lookup type

        Argument: id of lookup type.

        Return: list of values found in json format.
        """
        logging.debug("\nTrying to find lookup values for : " + id)
        logging.debug("*** LookupType '" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types/" + id + "/values"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for lookup_type " + id + "?")
        logging.debug(r.json())
        return r.json()

    def lookup_type_details(self, name, id):
        """Return value for given lookup type id

        Argument: name of lookup type
                  id of lookup type value id.

        Return: All details of lookup type value in json format.
        """
        logging.debug("*** LookupTypeValue name'" + name + "'")
        logging.debug("*** LookupTypeValue id  '" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types/" + name + "/values/" + id
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()


    def domains_list(self):
        """Return list of domains defined"""
        logging.debug("*** domains")
        cmdbuild_url = self.url + "/services/rest/v2/domains"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.info("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(r.json())
        return r.json()


    def domain_relations(self, id):
        """Return relations of specified domain as json object

        Argument:
            id    id of requested domain
        """
        logging.debug("*** Domain relations of id:'" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id+ "/relations/"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(pprint(r.json()))
        return r.json()


    def domain_relation_details(self, name,id1):
        """Return relation details of specified domain as json object

        Argument:
            name    name of domain
            id      id of requested domain relation
        """
        logging.debug("*** Domain relation details of name "+name+ " and id " + str(id1)  )
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + name+ "/relations/" +str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(pprint(r.json()))
        return r.json()


    def domain_details(self, id):
        """Return details of specified domain

        Argument:
            name:  id of domain
        """
        logging.debug("*** Domain '" + id + "' details")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        pprint(r.json())


    def domain_attributes(self, id):
        """Return attributes of specified domain

        Argument:
            name:  id of domain
        """
        logging.debug("*** Domain '" + id + "' attributes")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id + "/attributes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        pprint(r.json())


    def classes_list(self):
        """Return list of available classes"""
        logging.debug("*** Classes ")
        cmdbuild_url = self.url + "/services/rest/v2/classes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(pprint(r.json()))
        return r.json()

    def classes_total(self):
        """Return list of available classes"""
        logging.debug("*** Classes ")
        cmdbuild_url = self.url + "/services/rest/v2/classes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(pprint(str(r.json()["meta"]["total"])))
        return (r.json()["meta"]["total"])

    def class_details(self, id):
        """Return details of specified class as json object

        Argument:
            id    id of requested class
        """
        logging.debug("*** Class details of id:'" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + id
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(pprint(r.json()))
        return r.json()


    def class_get_attributes_of_type(self, id):
        """Return attributes of specified class as json object

        Argument:
            id    id of requested class
        """
        logging.debug("*** Class  '" + id + "' attributes")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + id + "/attributes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " attributes ")
        logging.debug(r.json())
        return r.json()

    def class_get_all_cards_of_type(self, type):
        """Return all cards of specified class as json object

        Argument:
            id    id of requested class
        """
        logging.debug("*** Class  of type '" + type + "' cards")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + type + "/cards"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class of type " + type + " cards ")
        logging.debug(r.json())
        return r.json()


    def class_get_card_details(self, type, id1):
        """Return all cards of specified class as json object

        Argument:
            type    type of requested class
            id      id of requested card
        """
        logging.debug("*** Class  '" + type + "' card details " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(type) + "/cards/" + str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url,  headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()


    def class_insert_card(self,cardtype,cardobject):
        """Insert card with name into cmdbuild

        Arguments:
            name    name of card
            object  json object with all relevant parameters
        Returns
            id of object created in JSON format
            error message when second argument is not a valid JSON object
        """
        if (self.check_valid_json(cardobject)):
            logging.debug("Inserting card of type " +str(cardtype) + " and with object:" + str(pprint(json.dumps(cardobject))) )
            cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(cardtype) + "/cards/"
            headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
            try:
                r = requests.post(cmdbuild_url,  data=cardobject, headers=headers)
                if not r.status_code // 100 == 2:
                    return "Error: Unexpected response {}".format(r)
                logging.debug(r.json())
                return r.json()
            except requests.exceptions.RequestException as e:
                logging.debug('HTTP ERROR %s occured' % e.code)
                logging.debug(e)
                return e
        else:
            return "Second argument is not a valid JSON object"


    def get_id(self,id1):
        """Retrieve info by id NOT IMPLEMENTED YET!
        Arguments
            classid    id of requested classtype
            cardid     id of requested card
        """
        return 1
        # <resource path="{attachmentId}/">
        # <resource path="{attachmentId}/{file: [^/]+}">
        # <resource path="{cardId}/">
        # <resource path="{classId}/">
        # <resource path="{classId}/">
        # <resource path="{domainId}/">
        # <resource path="{id}/">
        # <resource path="{relationId}/">
        # <resource path="{username}/">
        # <resource path="{lookupTypeId}/">
        # <resource path="{lookupValueId}/">
        # <resource path="{processId}/">
        # <resource path="{processId}/generate_id">
        # <resource path="{processActivityId}/">
        # <resource path="{attachmentId}/">
        # <resource path="{attachmentId}/{file: [^/]+}">
        # <resource path="{emailId}/">
        # <resource path="{processInstanceId}">
        # <resource path="{processActivityId}">
        # <resource path="{reportId}/">
        # <resource path="{reportId}/attributes/">
        # <resource path="{reportId}/{file: [^/]+}">
        # <resource path="{id}/">

        # logging.debug("*** Get object with id "+ str(id1) )
        # cmdbuild_url = self.url + "/services/rest/v1/"+ str(id1)+"/"
        # headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        # r = requests.get(cmdbuild_url,  headers=headers)
        # if not r.status_code // 100 == 2:
        #     return "Error: Unexpected response {}".format(r)
        # logging.debug(r)
        # return r
