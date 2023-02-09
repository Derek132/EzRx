import ezRx_methods
from PyQt5.QtCore import QAbstractTableModel, Qt
import uuid             #lib for getting MAC address
import socket        #lib for getting local ip address
import requests         #lib for html request
import psutil           #check for running process
import threading
from PyQt5.QtWidgets import *
import sms

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class GeneralTabWindow():
    # Main_Tab_To_Do_List
    def tab_main_clicked_to_do_task(window):
        print('Main Tab Clicked')
        pass

    def tab_info_clicked_to_do_task(window):
        print('Info Tab Clicked')
        thread = threading.Thread(target=TabPCStatMethods.
                                         tabPCStatMethodThread, args=(window, ))
        thread.start()

    def tabBarClicked(window):
        index = window.tabWidget.currentIndex()

        if window.tabWidget.tabBar().tabText(index) == 'Main':
            GeneralTabWindow.tab_main_clicked_to_do_task(window=window)

        elif window.tabWidget.tabBar().tabText(index) == 'Info':
            GeneralTabWindow.tab_info_clicked_to_do_task(window=window)

class TabMainMethods():
    # PRETEXT SMS -----------------------------------------------------------------------------------------------
    def validate_phone_number(phone_number):
        if len(phone_number) == 10 or (len(phone_number) == 11 and phone_number[0] == 1):
            return True
        else:
            return False
    def phone_num_clean_up(phone_number):
        numbers = list(str(phone_number))
        new_number = ''
        if numbers:
            for number in numbers:
                if number.isdigit():
                    new_number = new_number + str(number)
        return new_number

    def mainTab_send_pharm_info_cmd_on_clicked(window):
        phone_number = window.main_tab_patient_phone_textbox.text()
        phone_number = TabMainMethods.phone_num_clean_up(phone_number)
        isValidPhoneNum = TabMainMethods.validate_phone_number(phone_number)

        if isValidPhoneNum:
            sms.sms(RECIPIENT=phone_number,
                    MESSAGE= sms.get_message(message_id='Pharmacy_Info_VNese'))

    # RECIPIENT SECTION -----------------------------------------------------------------------------------------
    def recipient_search_textbox_on_return_pressed(window, search_result_title):
        window.patient_recipient_qtableview_label.setText(search_result_title)
        result_df = ezRx_methods.recipient_search(search_input=window.main_tab_recipient_search_textbox.text(),
                                                  recipient_csv_file_path='provider_list.csv')
        model = PandasModel(result_df)
        window.main_tab_search_tableview.setModel(model)  # Display Search Result
        window.main_tab_search_tableview.horizontalHeader().setDefaultSectionSize(200)  # Adjust width of all columns

    def main_tab_search_tableview_on_double_clicked(window, search_result_table_title_dict):
        # get the horizontal header
        horizontal_header = window.main_tab_search_tableview.horizontalHeader()

        # get the number of columns
        num_columns = horizontal_header.count()

        selected_index = window.main_tab_search_tableview.selectedIndexes()[0]

        if window.patient_recipient_qtableview_label.text() == search_result_table_title_dict['recipient_search']:
            provider_headers = ['DoctorName', 'Street1', 'Phone', 'Fax', 'NPI', 'City', 'Zip', 'State', 'DEA']
            provider_dict = {}
            for header in provider_headers:
                for column in range(num_columns):
                    # get the text of the header at the given column
                    header_text = horizontal_header.model().headerData(column, Qt.Horizontal, Qt.DisplayRole)
                    if header_text == header:
                        model = window.main_tab_search_tableview.model()
                        current_index = model.index(selected_index.row(), column)
                        cell_value = model.data(current_index)
                        provider_dict[header] = cell_value
                        break

            address_full = provider_dict['Street1'] + ', ' + provider_dict['City'] \
                           + ', ' + provider_dict['State'] + ', ' + provider_dict['Zip']

            window.main_tab_recipient_search_textbox.setText(provider_dict['DoctorName'])
            window.main_tab_dea_textbox.setText(provider_dict['DEA'])
            window.main_tab_npi_textbox.setText(provider_dict['NPI'])
            window.main_tab_title_textbox.setText('Future Feature')
            window.main_tab_fax_textbox.setText(provider_dict['Fax'])
            window.main_tab_phone_textbox.setText(provider_dict['Phone'])
            window.main_tab_address_textbox.setText(address_full)
            window.main_tab_notes_textbox.setText('Future Feature')



    # DRUG SELECTION --------------------------------------------------------------------------------------------
    def set_drug_tablewidget_col_width(window):
        drug_col_width = {'Drug Name': 300, 'Quantity': 100, 'Refill': 100, 'Direction': 900}

        for key, value in drug_col_width.items():
            for j in range(0, len(drug_col_width)):
                header_name = window.mainTab_drug_tablewidget.horizontalHeaderItem(j).text()

                if header_name == key:
                    # Set column width
                    window.mainTab_drug_tablewidget.setColumnWidth(j, value)
                    print(header_name, value)

    def main_tab_drug_direction_textbox_on_return_pressed(window):
        window.mainTab_drug_tablewidget.setRowCount(10)
        drug_name = window.main_tab_drug_request_textbox.text().upper()
        quantity = window.main_tab_drug_quantity_textbox.text().upper()
        refill_request = window.main_tab_drug_refill_num_textbox.text().upper()
        direction = window.main_tab_drug_direction_textbox.text().upper()

        drug_col_value = {'Drug Name': drug_name, 'Quantity': quantity, 'Refill': refill_request, 'Direction': direction}

        total_row = 10
        new_row = 0
        # Get Next Empty drug_name
        for j in range(0, 10):
            cell_item = window.mainTab_drug_tablewidget.item(j, 0)
            if cell_item is None:
                new_row = j
                break

        print('New Row:', new_row)
        for key,value in drug_col_value.items():
            for i in range(0,len(drug_col_value)):
                header_text=window.mainTab_drug_tablewidget.horizontalHeaderItem(i).text()
                if header_text == key:
                    item = QTableWidgetItem(value)
                    window.mainTab_drug_tablewidget.setItem(new_row, i, item)     # Set value



    def mainTab_remove_selected_drug_cmd_on_click(window):
        selectedRanges=window.mainTab_drug_tablewidget.selectedRanges()

        if selectedRanges:
            # sort the list of selected rows in descending order
            selectedRows = sorted([r.bottomRow() for r in selectedRanges], reverse=True)

            for row in selectedRows:
                window.mainTab_drug_tablewidget.removeRow(row)
        else:
            print("No row is selected")


    def mainTab_sig_list_tableview_display(window, search_key):
        filtered_df = ezRx_methods.sig_list_filter(search_key=search_key,
                                                   sig_csv_file_path=r'D:\__HelloRx Pharmacy\GoogleDriveMirror\Python\HelloRxPharmacy\EzRx\sigcode.csv')

        model = PandasModel(filtered_df)
        window.mainTab_sig_list_tableview.setModel(model)  # Display Search Result
        window.mainTab_sig_list_tableview.horizontalHeader().setDefaultSectionSize(200)

    def main_tab_drug_direction_textbox_on_textChanged(window):
        # get the text from the QTextEdit
        text = window.main_tab_drug_direction_textbox.text()
        new_text = text

        words = text.split()
        if not words:
            return
        else:
            TabMainMethods.mainTab_sig_list_tableview_display(window=window, search_key=words[-1])

        # check if the text ends with a space
        if text.endswith(" "):
            words = text.split()
            if not words:
                return
            else:
                # get the last word
                last_word = words[-1]

                filtered_df = ezRx_methods.sig_list_filter(search_key=last_word,
                                                           sig_csv_file_path=r'D:\__HelloRx Pharmacy\GoogleDriveMirror\Python\HelloRxPharmacy\EzRx\sigcode.csv')

                if not filtered_df.empty:
                    translation = filtered_df['translation'].iloc[0]

                    # remove the last word
                    new_text = " ".join(words[:-1]).rstrip() + " "
                    new_text = new_text + translation

                    window.main_tab_drug_direction_textbox.setText(new_text.strip() + ' ')







class TabPCStatMethods():
    def tabPCStatMethodThread(window):
        TabPCStatMethods.pc_stat_tab_get_info(window)
        TabPCStatMethods.pc_stat_tab_load_quick_dial_list(window)
        TabPCStatMethods.pc_stat_tab_load_traceable_data(window)

    def get_pc_mac_address(self=None):
        mac_address=uuid.getnode()
        mac_address_string = ':'.join(['{:02x}'.format((mac_address >> i) & 0xff) for i in range(0, 8 * 6, 8)][::-1])
        return mac_address_string

    def isLocaltoHelloRxPharmacyNetwork(pc_local_ip):
        host_id = pc_local_ip.split('.')[3]
        if int(host_id) > 210 and int(host_id) < 218:
            return True
        else:
            return False

    def get_pc_station_number(isLocaltoHelloRxPharmacyNetwork):
        if isLocaltoHelloRxPharmacyNetwork == False:
            return 'Non-Network PC'
        else:
            pass    #Will work on getting station number later

    def is_process_running(name):
        for proc in psutil.process_iter():
            try:
                if name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def pc_stat_tab_get_info(window):
        mac_address= TabPCStatMethods.get_pc_mac_address().upper()
        local_ip= socket.gethostbyname(socket.gethostname())
        isLocalToHelloRxPharmacy = TabPCStatMethods.isLocaltoHelloRxPharmacyNetwork(local_ip)
        station_number= TabPCStatMethods.get_pc_station_number(isLocalToHelloRxPharmacy)
        public_ip = requests.get('https://api.ipify.org').text
        is_media_player_process_running= TabPCStatMethods.is_process_running('wmplayer.exe')

        window.pc_stat_tab_local_pc_textbox.setText(str(isLocalToHelloRxPharmacy))
        window.pc_stat_tab_station_num_textbox.setText(station_number)
        window.pc_stat_tab_mac_address_textbox.setText(mac_address)
        window.pc_stat_tab_lan_ip_textbox.setText(local_ip)
        window.pc_stat_tab_public_ip_textbox.setText(public_ip)
        window.pc_stat_tab_media_player_status_textbox.setText(str(is_media_player_process_running))

    def pc_stat_tab_load_quick_dial_list(window):
        quick_dial_df = ezRx_methods.read_quick_dial_csv(quick_dial_csv_file_path='quick_dial.csv')
        model = PandasModel(quick_dial_df)
        window.pc_stat_tab_quick_dial_table_view.setModel(model)  # Display Search Result
        window.pc_stat_tab_quick_dial_table_view.horizontalHeader().setDefaultSectionSize(200)  # Adjust width of all columns

    def pc_stat_tab_load_traceable_data(window):
        traceable_data = ezRx_methods.get_thermometer_data(thermometer_data_csv_file_path='thermometer_data.csv')
        traceable_df = traceable_data['df']
        model = PandasModel(traceable_df)
        window.pc_stat_tab_fridge_freezer_data_tableView.setModel(model)  # Display Search Result
        window.pc_stat_tab_fridge_freezer_data_tableView.horizontalHeader().setDefaultSectionSize(120)  # Adjust width of all columns
        window.pc_stat_tab_fridge_current_temp_textbox.setText(' ' +
            str(traceable_data['current_fridge_temp']) + ' F')
        window.pc_stat_tab_freezer_current_temp_textbox.setText(
            str(traceable_data['current_freezer_temp']) + ' F')
        window.pc_stat_tab_fridge_average_temp_textbox.setText(' ' +
            str(traceable_data['average_fridge_temp']) + ' F')
        window.pc_stat_tab_freezer_average_temp_textbox.setText(
            str(traceable_data['average_freezer_temp']) + ' F')
        window.pc_stat_tab_fridge_freezer_last_timestamp_textbox.setText(
            traceable_data['last_datetime'] + ' - ' + str(traceable_data['minutes_since_last_datetime']) + ' Minutes Ago')

        if traceable_data['minutes_since_last_datetime'] > 30:
            window.pc_stat_tab_fridge_status_label.setText ('WARNING: LAST DATA POINT IS >30 MIN AGO')
            #rgba() function to set the color with an additional "alpha" value, which controls the transparency of the color.
            window.pc_stat_tab_fridge_status_label.setStyleSheet("background-color: rgba(255, 0, 50, 0.5);;")
        else:
            window.pc_stat_tab_fridge_status_label.setText ('STATUS: OK')
            window.pc_stat_tab_fridge_status_label.setStyleSheet("background-color: rgba(0, 255, 0, 0.5);;")




    def pc_stat_tab_ring_out(window):
        # get the horizontal header
        horizontal_header = window.pc_stat_tab_quick_dial_table_view.horizontalHeader()

        # get the number of columns
        num_columns = horizontal_header.count()

        if window.pc_stat_tab_quick_dial_table_view.selectedIndexes():  # List is available & not empty
            selected_index = window.pc_stat_tab_quick_dial_table_view.selectedIndexes()[0]

            for column in range(num_columns):
                # get the text of the header at the given column
                header_text = horizontal_header.model().headerData(column, Qt.Horizontal, Qt.DisplayRole)
                if header_text == 'Phone':
                    model = window.pc_stat_tab_quick_dial_table_view.model()
                    current_index = model.index(selected_index.row(), column)
                    phone_number = model.data(current_index).replace('-','')
                    break

            print(phone_number)


