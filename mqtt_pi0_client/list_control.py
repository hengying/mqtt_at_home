
from layer import Layer
from button_enum import *
from event import *


BIAS_Y = -2

class ListControl(Layer):
    def __init__(self, holder, name, labels):
        super().__init__(holder, name)
        self._labels = labels
        self._current_item = 0
        self._top_item = 0

    def handle_event(self, event):
        super().handle_event(event)

        if type(event) == ButtonDownEvent:
            if event.button_type == ButtonType.STICK_UP:
                self._current_item -= 1
                if self._current_item < self._top_item:
                    self._top_item = self._current_item
                if self._current_item < 0:
                    self._current_item = len(self._labels) - 1
                    self._top_item = self._current_item - self._holder._row_count + 1
                    if self._top_item < 0:
                        self._top_item = 0
            if event.button_type == ButtonType.STICK_DOWN:
                self._current_item += 1
                if self._current_item >= self._top_item + self._holder._row_count:
                    self._top_item = self._current_item - self._holder._row_count + 1
                if self._current_item >= len(self._labels):
                    self._current_item = 0
                    self._top_item = self._current_item - self._holder._row_count + 1
                    if self._top_item < 0:
                        self._top_item = 0
            if event.button_type == ButtonType.STICK_LEFT or \
                event.button_type == ButtonType.BUTTON_1:
                self._holder.add_event(ListBack(self._name))
            if event.button_type == ButtonType.STICK_RIGHT or \
                event.button_type == ButtonType.STICK_PRESS or \
                event.button_type == ButtonType.BUTTON_3:
                self._holder.add_event(ListItemSelected(self._name, self._current_item))
            if event.button_type == ButtonType.BUTTON_2:
                pass

    def paint(self, image_draw):
        items_blow = len(self._labels) - self._top_item
        if items_blow > self._holder.row_count:
            items_blow = self._holder.row_count

        for i in range(items_blow):
            if i == self._current_item - self._top_item:
                image_draw.text((0, self._holder.row_height * i + BIAS_Y),
                                '>{}'.format(self._labels[self._top_item + i]),
                                font=self._holder.font16, fill=self._holder.foreground_color)
            else:
                image_draw.text((0, self._holder.row_height * i + BIAS_Y),
                                ' {}'.format(self._labels[self._top_item + i]),
                                font=self._holder.font16, fill=self._holder.foreground_color)
