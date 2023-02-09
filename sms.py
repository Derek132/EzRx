from ringcentral import SDK

# Global vars
RINGCENTRAL_CLIENTID = 'RRwE_84GRlqscCZp5laULg'
RINGCENTRAL_CLIENTSECRET = 'cuHqZEeKSJO5xhIFii8kfAQSziuAB6QRyAL1NxfWStRw'
RINGCENTRAL_SERVER = 'https://platform.ringcentral.com'

RINGCENTRAL_USERNAME = '+14082229889'
RINGCENTRAL_PASSWORD = 'Cranberry!123'
RINGCENTRAL_EXTENSION = '101'


def sms(RECIPIENT, MESSAGE='Test'):
    if MESSAGE != '':
        rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
        platform = rcsdk.platform()
        platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

        platform.post('/restapi/v1.0/account/~/extension/~/sms',
                      {
                          'from': {'phoneNumber': RINGCENTRAL_USERNAME},
                          'to': [{'phoneNumber': RECIPIENT}],
                          'text': MESSAGE
                      })

        print('Sent: ', RECIPIENT)
        print('Message: ', MESSAGE)

    else:
        print('Empty Message. Message Not Sent')



def sms_with_attachment(ATTACHMENT_PATH, ATTCHMENT_NAME, RECIPIENT='2602322322', MESSAGE='Test'):
    rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

    builder = rcsdk.create_multipart_builder()
    builder.set_body({
        'from': {'phoneNumber': RINGCENTRAL_USERNAME},
        'to': [{'phoneNumber': RECIPIENT}],
        'text': MESSAGE
    })

    image = open(ATTACHMENT_PATH, 'rb')
    attachment = (ATTCHMENT_NAME, image, 'image/jpeg')
    builder.add(attachment)
    try:
        request = builder.request('/account/~/extension/~/sms')
        response = platform.send_request(request)
        print('Sent Attachement: ', ATTCHMENT_NAME)
        print('To Number: ', RECIPIENT)

    except Exception as e:
        print(e)


def ringout(FROM_NUMBER='+14084147608',
            RECIPIENT='+16025969958'):
    # pharmacist_number = '+14084147608'
    # tech_fill_number = '+14088249136'
    # tech_next_printer_number = '+14086382092'
    # tech_pickup_number = '+14086104098'

    RINGCENTRAL_CLIENTID = 'x9OLpCLXT4OOPYPMSy5d2Q'
    RINGCENTRAL_CLIENTSECRET = 'otI0zKlYSMaqVmOdWZHL1QAJFm4BoaS0GOhivXR5PmWA'
    RINGCENTRAL_SERVER = 'https://platform.ringcentral.com'


    rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

    resp = platform.post('/restapi/v1.0/account/~/extension/~/ring-out',
                         {
                             'from': {'phoneNumber': FROM_NUMBER},
                             'to': {'phoneNumber': RECIPIENT},
                             'playPrompt': False

                         })

    # print(f'Call placed. Call ID: {resp.json().id}')
    # print(f'Call placed. Call URI: {resp.json().uri}')

    print(f'Call placed: {RECIPIENT} \nCall status: {resp.json().status.callStatus}')
    print('\nPlease Pick Up The Phone to Start Conversation\nTerminal will be closed in 3 seconds')



def get_message(message_id):
    Pharmacy_Info_VN = 'Thông Tin HelloRx PHARMACY\n' + \
                       'Electronic Rx ID: *******\n' + \
                       'Phone: 408-222-9889\n' + \
                       'Fax: 408-222-9890\n' + \
                       'Address: 2268 Senter Rd STE-202, San Jose, CA 95112\n\n' + \
                       'Giờ Mở Cửa:\n' + \
                       'Thứ 2 - 6:\n' + \
                       '\t9 Giờ Sáng -> 6 Giờ Chiều\n ' + \
                       'Thứ 7:\n' + \
                       '\t9 Giờ Sáng -> 1 Giờ Trưa\n' + \
                       'Chủ Nhật: Đóng Cửa\n\n' + 'Xin Cám Ơn Quí Khách Đã Ủng Hộ HelloRx PHARMACY'

    MESSAGE_DICT = {'Pharmacy_Info_VNese': Pharmacy_Info_VN}

    return MESSAGE_DICT[message_id]



# sms(RECIPIENT='6025969958',MESSAGE='Hello World From HelloRx Pharmacy')