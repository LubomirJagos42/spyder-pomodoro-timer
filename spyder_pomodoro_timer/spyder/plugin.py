# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2021, Francisco Palm
#
# Licensed under the terms of the MIT license
# ----------------------------------------------------------------------------
"""
Spyder Pomodoro Timer Plugin.
"""

# Third-party imports
import qtawesome as qta

# Spyder imports
from spyder.api.plugin_registration.decorators import on_plugin_available
from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder.utils.icon_manager import ima

# Local imports
from spyder_pomodoro_timer.spyder.confpage import SpyderPomodoroTimerConfigPage
from spyder_pomodoro_timer.spyder.container import SpyderPomodoroTimerContainer
from spyder_pomodoro_timer.spyder.config import CONF_DEFAULTS, CONF_VERSION


_ = get_translation("spyder_pomodoro_timer.spyder")


class SpyderPomodoroTimer(SpyderPluginV2):
    """
    Spyder Pomodoro Timer plugin.
    """

    NAME = "spyder_pomodoro_timer"
    REQUIRES = [Plugins.StatusBar, Plugins.Toolbar, Plugins.Preferences]
    OPTIONAL = []
    CONTAINER_CLASS = SpyderPomodoroTimerContainer
    CONF_SECTION = NAME
    CONF_WIDGET_CLASS = SpyderPomodoroTimerConfigPage
    CONF_DEFAULTS = CONF_DEFAULTS
    CONF_VERSION = CONF_VERSION

    # --- Signals

    # --- SpyderPluginV2 API
    # ------------------------------------------------------------------------
    @staticmethod
    def get_name():
        return _("Spyder Pomodoro Timer")

    @staticmethod
    def get_description():
        return _("A very simple pomodoro timer that shows in the status bar.")

    @staticmethod
    def get_icon():
        return qta.icon("mdi.av-timer", color=ima.MAIN_FG_COLOR)

    # def on_initialize(self):
    #     container = self.get_container()
    #     print("SpyderPomodoroTimer initialized!")

    def on_initialize(self):
        # 1. Get the status bar plugin instance from Spyder
        statusbar = self.get_plugin(Plugins.StatusBar)

        # 2. Extract your timer widget from the plugin container
        container = self.get_container()
        timer_widget = container.pomodoro_timer_status

        # 3. Physically add it to the bottom bar layout
        statusbar.add_status_widget(timer_widget)

    @on_plugin_available(plugin=Plugins.Preferences)
    def on_preferences_available(self):
        preferences = self.get_plugin(Plugins.Preferences)
        preferences.register_plugin_preferences(self)

    # @on_plugin_available(plugin=Plugins.StatusBar)
    # def on_statusbar_available(self):
    #     statusbar = self.get_plugin(Plugins.StatusBar)
    #     if statusbar:
    #         statusbar.add_status_widget(self.pomodoro_timer_status)

    @on_plugin_available(plugin=Plugins.StatusBar)
    def on_statusbar_available(self):
        """Callback when the status bar plugin becomes available."""
        statusbar = self.get_plugin(Plugins.StatusBar)

        # --- COMMENT OUT OR REMOVE THIS LINE ---
        # statusbar.add_status_widget(self.pomodoro_timer_status)

        # Keep any other code that links your toolbar to the widget, such as:
        container = self.get_container()
        if hasattr(container, 'pomodoro_timer_toolbar'):
            container.pomodoro_timer_toolbar.set_status_widget(container.pomodoro_timer_status)

    @on_plugin_available(plugin=Plugins.Toolbar)
    def on_toolbar_available(self):
        container = self.get_container()
        toolbar = self.get_plugin(Plugins.Toolbar)
        toolbar.add_application_toolbar(container.pomodoro_timer_toolbar)

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------

    @property
    def pomodoro_timer_status(self):
        container = self.get_container()
        return container.pomodoro_timer_status
