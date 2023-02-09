from ringcentral import SDK
import time
import ctypes
import json

def fax(recipient_fax_number,faxfilepath):
    print('start faxing function')
    RECIPIENT = recipient_fax_number

    RINGCENTRAL_CLIENTID = 'VR-QQMuSRhywXvFbzthPPw'
    RINGCENTRAL_CLIENTSECRET = 'rs5_-TYeQf6U8FoRZHkp5gDvVqBpy4SuOmN-Luhi1MbQ'
    RINGCENTRAL_SERVER = 'https://platform.ringcentral.com'

    RINGCENTRAL_USERNAME = '+14084004755'
    RINGCENTRAL_PASSWORD = 'Senter04'
    RINGCENTRAL_EXTENSION = '101'

    rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)
    print('Log in sucessfully')

    builder = rcsdk.create_multipart_builder()
    builder.set_body({
        'to': [{'phoneNumber': RECIPIENT}],
        'faxResolution': "High",
        'coverPageText': "",
        'coverIndex':'0'
    })

    #filepath = 'C:\\Users\\lekic\\Dropbox\\2332_001(003).pdf'
    filepath = faxfilepath
    attachment = (filepath, open(filepath, 'rb').read())
    builder.add(attachment)

    request = builder.request('/account/~/extension/~/fax')

    resp = platform.send_request(request)
    #ctypes.windll.user32.MessageBoxW(0, 'Fax status: ' + resp.json().messageStatus, 'Notification', 0x40 | 0x0)
    print('Fax sent. Message status: ' + resp.json().messageStatus)
    print('Fax ID: {}'.format(resp.json().id))



def check_fax_status():


    RINGCENTRAL_CLIENTID = 'VR-QQMuSRhywXvFbzthPPw'
    RINGCENTRAL_CLIENTSECRET = 'rs5_-TYeQf6U8FoRZHkp5gDvVqBpy4SuOmN-Luhi1MbQ'
    RINGCENTRAL_SERVER = 'https://platform.ringcentral.com'

    RINGCENTRAL_USERNAME = '+14084004755'
    RINGCENTRAL_PASSWORD = 'Senter04'
    RINGCENTRAL_EXTENSION = '101'

    rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)


    from_date='2020-08-02'

    # Tips: message_type = ['Fax', 'SMS', 'VoiceMail', 'Pager', 'Text']
    message_type = ['Fax']

    # Tips: 'direction': [ 'Inbound', 'Outbound']
    direction = ['Outbound']

    # phone number
    # phonenumber = '+1'+'4089230344'

    # OPTIONAL QUERY PARAMETERS
    queryParams = {
        #'availability': [ 'Alive', 'Deleted', 'Purged' ],
        #'conversationId': 000,
        'dateFrom': from_date,
        # 'dateTo': to_date,
        'direction': direction,
        #'distinctConversations': true,
        'messageType': message_type,
        #'readStatus': [ 'Read', 'Unread' ],
        #'page': 1,
        # 'perPage': 100,
        # 'phoneNumber': phonenumber
    }

    response = platform.get('/restapi/v1.0/account/~/extension/~/message-store',queryParams)
    # print(response.text())

    # # See methods of objects
    # object_methods = [method_name for method_name in dir(response)
    #                   if callable(getattr(response, method_name))]

    # https://community.ringcentral.com/questions/8457/pull-call-data-python-api.html
    for record in response.json().records:
        print ("\nCall type: " + record.type)
        print('Fax ID: {}'.format(record.id))
        # print('To Phone Number: {}'.format(record.phoneNumber))
        print('Status: {}'.format(record.messageStatus))
        print('Direction: {}\n'.format(record.direction))



if __name__ == '__main__':
    check_fax_status()
