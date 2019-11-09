# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.filemanager.analysis

class NoOpGcodeAnalysisQueue(octoprint.filemanager.analysis.AbstractAnalysisQueue):
    def __init__(self, finished_callback): pass
    def enqueue(self, entry, high_priority=False): pass
    def dequeue(self, location, path): pass
    def dequeue_folder(self, location, path): pass
    def pause(self): pass
    def resume(self): pass

class DisableGcodeAnalysisPlugin(octoprint.plugin.SettingsPlugin,
                                 octoprint.plugin.RestartNeedingPlugin):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ Analysis factories hook

    def get_analysis_factories(self, *args, **kwargs):
        return dict(gcode=NoOpGcodeAnalysisQueue)

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            disable_gcode_analysis=dict(
                displayName="Disable Gcode Analysis Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="buddydvd",
                repo="octoprint-disable-gcode-analysis",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/buddydvd/octoprint-disable-gcode-analysis/archive/{target_version}.zip"
            )
        )

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = DisableGcodeAnalysisPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.filemanager.analysis.factory": __plugin_implementation__.get_analysis_factories,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
