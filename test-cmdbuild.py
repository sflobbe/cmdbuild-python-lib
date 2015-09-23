#!/usr/bin/python
# script to test functionality of cmdbuild python module/package
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

import logging
from cmdbuild import *
from json import JSONEncoder

logging.basicConfig(level=logging.DEBUG)

def main(argv=None):

    cm1 = cmdbuild()

    print("\n==> dir(cmdbuild): " + str(dir(cm1)))

    print("\n==> cmdbuild.info(): " + str(cm1.info()))

    if (cm1.connect('http://server:8080/cmdbuild', 'userid', 'password')):
        print(returnvalue)
        print("\n==> Returned token: " + str(cm1.token))

    print "+++ Session_info()+++"
    pprint(cm1.session_info())
    #
    print "+++ lookup_types()+++"
    pprint(cm1.lookup_types_info())
    #
    print "+++ lookup_types_values()+++"
    pprint(cm1.lookup_type_values('APCT_SCFEWS_BBRANCH'))
    #
    print "+++ lookup_type_details()+++"
    pprint(cm1.lookup_type_details('APCT_SCFEWS_BBRANCH', '52106'))
    #
    print "+++ Domains()+++"
    pprint(cm1.domains_list())
    #
    print "+++ Domains() details+++"
    pprint(cm1.domain_details('IPV4_002_DV'))
    #
    print "+++ Domains() attributes+++"
    pprint(cm1.domain_attributes('IPV4_002_DV'))
    #
    print "+++ Domain relations()+++"
    pprint(cm1.domain_relations('IPV4_002_DV'))
    #
    print "+++ Domain relation details()+++"
    pprint(cm1.domain_relation_details('IPV4_002_DV',46441))
    #
    print "+++ Classes_total()+++"
    pprint(cm1.classes_total())
    #
    print "+++ Classes_list()+++"
    pprint(cm1.classes_list())
    #
    print "+++ Class_details()+++"
    pprint(cm1.class_details('CI_RS_PF_SVC_SW'))
    #
    pprint(cm1.class_details('CI_RS_PF_SVC_PGSQLRDBMS'))
    #
    print "+++ Class attributes()+++"
    pprint(cm1.class_get_attributes_of_type('CI_RS_PF_SVC_PGSQLRDBMS'))
    #
    #
    print "+++ Class all cards() of type+++"
    pprint(cm1.class_get_all_cards_of_type('CI_RS_PF_SVC_PGSQLRDBMS'))
    #
    print "+++ Class get cards details+++"
    pprint(cm1.class_get_card_details('CI_RS_PF_SVC_PGSQLRDBMS', 38182))
    #
    print "+++ get object by id +++"
    pprint(cm1.get_id(52106))

    print "+++ Insert Class+++"

    jsonString = JSONEncoder().encode({
        'Description': 'test-server',
        'Notes': 'Imported from python script'
    })
    classname='CI_RS_IFST_SVR'
    pprint(cm1.class_insert_card(classname, jsonString))

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("dir cmdbuild")
    pprint(dir(cmdbuild))

    print("vars cmdbuild instance")
    pprint(vars(cm1))


#####################################################################
if __name__ == "__main__":
    # sys.exit(main())
    main()
