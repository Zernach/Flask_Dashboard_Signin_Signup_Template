from firebase_admin import firestore
import pandas as pd
import datetime
import json
import time


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INSTANTIATE VALUES IN USER SESSION DICTIONARY
# # # # # # # # # # # # # # # # # # # # # # # #
def createFreshSessionData():
    new_session_data = {
        # User
        'user_email': '',
        'userRef': '',
        'html_dataframe': '',
        'uploaded_columns': '',
        'total_amount_dollars': 0,
        'UID': '',
        'firstName': '',
        'lastName': '',
        'email': '',
        'phone': 0,
        'firstThreePhone': '',
        'secondThreePhone': '',
        'lastFourPhone': '',
        'address': '',
        'city': '',
        'state': '',
        'zip': 0,
        # Organization
        'orgID': '',
        'locationsDictionaryOfLists': {'': [], '': []},
        'companyName': '',
        'publicStoreName': '',
        'orgEmail': '',
        'orgPhotoURL': '',
        'firstThreeOrgPhone': '',
        'secondThreeOrgPhone': '',
        'lastFourOrgPhone': '',
        # Programmer's Variables
        'svg_dict': {
            'dashboarddashboard': '<svg class="feather feather-home" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
            'dashboardinbox': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-inbox"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"></polyline><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path></svg>',
            'dashboardproducts': '<svg class="feather feather-shopping-cart" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>',
            'dashboardcustomers': '<svg class="feather feather-users" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"> <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path> <circle cx="9" cy="7" r="4"></circle> <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path> <path d="M16 3.13a4 4 0 0 1 0 7.75"></path> </svg>',
            'dashboardreports': '<svg class="feather feather-bar-chart-2" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"> <line x1="18" x2="18" y1="20" y2="10"></line> <line x1="12" x2="12" y1="20" y2="4"></line> <line x1="6" x2="6" y1="20" y2="14"></line> </svg>',
            'dashboardintegrations': '<svg class="feather feather-layers" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"> <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon> <polyline points="2 17 12 22 22 17"></polyline> <polyline points="2 12 12 17 22 12"></polyline> </svg>',
            'dashboardprofile': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user"> <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path> <circle cx="12" cy="7" r="4"></circle> </svg>',
            'dashboardorganization': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-map-pin"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>',
            }
    }
    return new_session_data


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ADD NEW USER TO DATABASE
# # # # # # # # # # # # # # # # # # # # # # # #
def addNewUserToDB(session_data):
    db = firestore.client()
    user_ref = db.collection(u'users').document(session_data['UID'])

    # CREATE NEW USER
    new_user_data = {
        'firstName': 'FirstName',
        'lastName': 'LastName',
        'email': session_data['user_email'],
        'city': 'city',
        'state': 'state',
        'zip': 12345,
        'phone': 1234567890,
        'userType': 'vendor',
        'profilePhotoURL': "https://github.com/landscapesupply/images/blob/main/landscape_supply_app_default_profile_icon_dark_350x350.png?raw=true",
    }
    user_ref.set(new_user_data)