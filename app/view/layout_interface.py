'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-26 15:18:24
FilePath: \aistore\app\view\layout_interface.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# coding:utf-8
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import FlowLayout, PushButton

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class LayoutInterface(GalleryInterface):
    """ Layout interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.layout,
            subtitle="qfluentwidgets.components.layout",
            parent=parent
        )
        self.setObjectName('layoutInterface')

        self.addExampleCard(
            self.tr('Flow layout without animation'),
            self.createWidget(),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/layout/flow_layout/demo.py',
            stretch=1
        )

        self.addExampleCard(
            self.tr('Flow layout with animation'),
            self.createWidget(True),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/layout/flow_layout/demo.py',
            stretch=1
        )

    def createWidget(self, animation=False):
        texts = [
            self.tr('Star Platinum'), self.tr('Hierophant Green'),
            self.tr('Silver Chariot'), self.tr('Crazy diamond'),
            self.tr("Heaven's Door"), self.tr('Killer Queen'),
            self.tr("Gold Experience"), self.tr('Sticky Fingers'),
            self.tr("Sex Pistols"), self.tr('Dirty Deeds Done Dirt Cheap'),
        ]

        widget = QWidget()
        layout = FlowLayout(widget, animation)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        for text in texts:
            layout.addWidget(PushButton(text))
        return widget
