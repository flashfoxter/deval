# -*- coding: utf-8 -*-


from deval.component.std.inputcomponent import InputComponent
from deval.utils.ios.iosfuncs import IOSProxy, _check_platform_ios, retry_session
from deval.utils.parse import parse_uri


class IOSInputComponent(InputComponent):   

    def __init__(self, uri, dev, name=None):
        super(IOSInputComponent, self).__init__(uri, dev, name)

        try:
            self.proxy = self.dev.iosproxy
        except AttributeError:
            self.dev.iosproxy = IOSProxy(**_check_platform_ios(uri))
            self.proxy = self.dev.iosproxy

    @retry_session
    def click(self, pos, **kwargs):
        duration = kwargs.get("duration", 0.05)
        # trans pos of click
        pos = self.proxy._touch_point_by_orientation(pos)

        # scale touch postion
        x, y = pos[0] * self.proxy._touch_factor, pos[1] * self.proxy._touch_factor
        if duration >= 0.5:
            self.proxy.session.tap_hold(x, y, duration)
        else:
            self.proxy.session.tap(x, y)

    def swipe(self, p1, p2, **kwargs):
        duration = kwargs.get("duration", 0.5)
        fx, fy = self.proxy._touch_point_by_orientation(p1)
        tx, ty = self.proxy._touch_point_by_orientation(p2)
        self.proxy.session.swipe(fx * self.proxy._touch_factor, fy * self.proxy._touch_factor, tx * self.proxy._touch_factor, ty * self.proxy._touch_factor, duration)

    def double_tap(self, pos, **kwargs):
        # trans pos of click
        pos = self.proxy._touch_point_by_orientation(pos)
        x, y = pos[0] * self.proxy._touch_factor, pos[1] * self.proxy._touch_factor
        self.proxy.session.double_tap(x, y)
