'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-24 09:56:54
FilePath: \aistore\app\common\signal_bus.py
Description: Defining global signal(notify)
'''
# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    appMessageSig = pyqtSignal(object)          # APP 
    appErrorSig = pyqtSignal(str)               # APP 
    appRestartSig = pyqtSignal()                # APP restart

    switchToSampleCard = pyqtSignal(str, int)
    micaEnableChanged = pyqtSignal(bool)
    supportSignal = pyqtSignal()
    
    switchToAppInterfaceSig = pyqtSignal(object)
    switchToModelLibraryInterfaceSig = pyqtSignal(object)

    # FaceFusion
    facefusion_progressSig = pyqtSignal()
    facefusion_unzipSig = pyqtSignal()
    facefusion_installSig = pyqtSignal()
    facefusion_finishedSig = pyqtSignal()

    software_registrySig = pyqtSignal(list)
    
    software_versionSig = pyqtSignal(object)

    software_installSig = pyqtSignal(object, object)
    software_uninstallSig = pyqtSignal(object)
    software_runSig = pyqtSignal(object)
    software_stopSig = pyqtSignal(object)

    model_downloadSig = pyqtSignal(str,str)
    # app_model_downloadSig = pyqtSignal(str, str)



signalBus = SignalBus()