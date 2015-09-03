import logging
from lqm.tool import ToolConfig
from lqm.exceptions import ConfigurationError


class SysLogConfig(ToolConfig):
    """
       ToSyslog config variables:
        * = required
        *host - address of remote syslog address
        port - port that remote syslog server is listening on(defaults to 514)
        *protocol - protocol you want to communicate with(tcp/udp)
        *messageHead - Define what you want to have at the begining of every message sent to syslog
        *messageFields - specify what fields you want extracted from the alerts and included in the messages
            note: Selected fields will be appended to end of message as so:
            ex: *messageHead* indicatorType="IPV4" indicator="192.168.1.1"
    """
    def __init__(self, configData, csvToolInfo, unhandledCSV):
        ToolConfig.__init__(self, configData, csvToolInfo, unhandledCSV)
        self._logger = logging.getLogger("LQMT.SysLog.{0}".format(self.getName()))
        hasError = False
        self._port = 514  # default port for syslog is 514.

        if 'host' in configData:
            self._host = configData['host']
        else:
            self._logger.error("Host must be specified in the configuration")
            hasError = True

        if 'port' in configData:
            self._port = configData['port']
        else:
            self._logger.error("Port not specified. Defaulting to port 514. ")

        if 'protocol' in configData:
            protocol = configData['protocol']
            if protocol == 'udp' or protocol == 'tcp':
                self._protocol = protocol
            else:
                self._logger.error("Invalid protocol: {0}".format(protocol))
                hasError = True
            self._protocol = protocol
        else:
            self._logger.error("Protocol must be specified in the configuration")
            hasError = True

        if 'messageHead' in configData:
            self._messageHead = configData['messageHead']
        else:
            self._logger.error("A message head must be specified in the configuration.")

        if 'messageFields' in configData:
            self._messageFields = configData['messageFields']
        else:
            self._logger.error("Message fields must be specified in the configuration.")

        if hasError:
            self.disable()
            raise ConfigurationError()

    def getHost(self):
        return self._host

    def getPort(self):
        return self._port

    def getProtocol(self):
        return self._protocol

    def getMessageHead(self):
        return self._messageHead

    def getMessageFields(self):
        return self._messageFields