'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-19 18:28:16
FilePath: \aistore\app\common\signal_bus.py
Description: Defining global signal(notify)
'''
# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = pyqtSignal(str, int)
    micaEnableChanged = pyqtSignal(bool)
    supportSignal = pyqtSignal()

    # FaceFusion
    facefusion_progressSig = pyqtSignal()
    facefusion_unzipSig = pyqtSignal()
    facefusion_installSig = pyqtSignal()
    facefusion_finishedSig = pyqtSignal()

    software_registySig = pyqtSignal(list)

signalBus = SignalBus()