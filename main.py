import sys
import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
import gui_methods as gm

# Global Variable
recipient_search_result_table_title = 'Recipient Search Result'
patient_search_result_table_title = 'Patient Search Result'

# End Global Variable

# App code -------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
Ui_MainWindow, QtBaseClass = uic.loadUiType("EzRx_GUI.ui")  # Load the .ui file

result_table_title_dict = {'patient_search': patient_search_result_table_title,
                           'recipient_search': recipient_search_result_table_title}



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):     # self = MainWindow Object => Current open GUI
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)  # set up the user interface based on the information in the .ui file.

    # Create & # Set the shortcut as a global shortcut -------------------------------------------------------------
        shortcut = QShortcut(QKeySequence("F11"),self)
        # Connect the shortcut to a function
        shortcut.activated.connect(lambda: gm.TabPCStatMethods
                                   .pc_stat_tab_ring_out(self))

    # AutoComplete for Drug Setup ----------------------------------------------------------------------------------
        names = pd.read_csv('auto_complete_drug_list.csv',usecols=['DRUG NAME'])['DRUG NAME'].values.tolist()
        completer = QCompleter(names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.main_tab_drug_request_textbox.setCompleter(completer)

    # Auto_Tab_Load when Tab Changes -------------------------------------------------------------------------------
        self.tabWidget.currentChanged.connect(
            lambda: gm.GeneralTabWindow
                      .tabBarClicked(self))

    # main_tab set up ----------------------------------------------------------------------------------------------
        gm.TabMainMethods.set_drug_tablewidget_col_width(window=self)

        # PATIENT SECTION ------------------------------------------------------------------------------------------

        # PRESET SMS -----------------------------------------------------------------------------------------------
        self.mainTab_send_pharm_info_cmd.clicked.connect(
            lambda: gm.TabMainMethods.mainTab_send_pharm_info_cmd_on_clicked(self))

        # RECIPIENT SECTION ----------------------------------------------------------------------------------------
        self.main_tab_recipient_search_textbox.returnPressed.connect(
            lambda: gm.TabMainMethods
                      .recipient_search_textbox_on_return_pressed(self,
                                                                  search_result_title=result_table_title_dict['recipient_search']))

        self.main_tab_search_tableview.doubleClicked.connect(
            lambda: gm.TabMainMethods
                      .main_tab_search_tableview_on_double_clicked(self,
                                                                   search_result_table_title_dict=result_table_title_dict))

        # DRUG SELECTION SECTION -----------------------------------------------------------------------------------
        self.main_tab_drug_direction_textbox.returnPressed.connect(
            lambda: gm.TabMainMethods
                      .main_tab_drug_direction_textbox_on_return_pressed(self))


        self.mainTab_remove_selected_drug_cmd.clicked.connect(
            lambda: gm.TabMainMethods
                      .mainTab_remove_selected_drug_cmd_on_click(self))


        self.main_tab_drug_direction_textbox.textChanged.connect(
            lambda: gm.TabMainMethods
                      .main_tab_drug_direction_textbox_on_textChanged(self))


    # pc_stat_tab set up -------------------------------------------------------------------------------------------
        self.pc_stat_tab_call_cmd.clicked.connect(
            lambda: gm.TabPCStatMethods
                      .pc_stat_tab_ring_out(self))

        self.pc_stat_tab_quick_dial_table_view.doubleClicked.connect(
            lambda: gm.TabPCStatMethods
                      .pc_stat_tab_ring_out(self))

        self.showNormal()


if __name__ == '__main__':
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
