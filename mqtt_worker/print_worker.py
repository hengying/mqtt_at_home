from config import Config
from worker import Worker
from escpos import config
from escpos.printer import Dummy
from printer_util import PrinterUtil

PRINT_TOPIC_ROOT = 'home/print/'
PRINT_TOPIC_SUBSCRIBE = PRINT_TOPIC_ROOT + '+'
MAX_QR_CODE_CHAR_COUNT = 450

class PrintWorker(Worker):
    def __init__(self, holder):
        super().__init__(holder)
        self._config = Config()

        self._printer_config = config.Config()
        self._printer = self._printer_config.printer()
        self._pu = PrinterUtil(self._printer)

    def on_connect(self, client, userdata, flags):
        super().on_connect(client, userdata, flags)
        client.subscribe(PRINT_TOPIC_SUBSCRIBE)

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)

        payload = msg.payload.decode('UTF-8')

        if msg.topic.startswith(PRINT_TOPIC_ROOT):
            command = msg.topic.rsplit("/", 1)[-1]
            if command == 'print':
                result = self._print_text(payload)
                client.publish(msg.topic + '/reply', payload=result, qos=2)
            elif command == 'print2':
                result = self._print_text(payload, 2)
                client.publish(msg.topic + '/reply', payload=result, qos=2)
            elif command == 'qr':
                result = self._print_qr(payload)
                client.publish(msg.topic + '/reply', payload=result, qos=2)

    """
    # 20210130 今天 .text() 方法打不出东西
    # 安装新版本：
    #     sudo pip3 install python-escpos --pre
    # 乱码。
    # 在这里找了个办法，凑活用一下：
    #     https://github.com/python-escpos/python-escpos/issues/190
    def _print_text(self, content, font_size=1):
        try:
            # 每次新建 Dummy，是为了清空前面的内容
            dummy = self._get_dummy_printer(font_size)
            dummy._raw(content.encode('GB18030'))
            dummy._raw('\n\n\n'.encode('GB18030'))
            self._printer._raw(dummy.output)
            return 'ok'
        except:
            return 'failed'
    """

    def _print_text(self, content, font_size=1):
        try:
            self._pu.init()
            self._pu.font_size(font_size, font_size)
            self._pu.text(content.encode('GB18030'))
            self._printer.ln(3)
            self._pu.init()
            return 'ok'
        except:
            return 'failed'

    def _print_qr(self, content):
        try:
            if len(content.encode('utf-8')) > MAX_QR_CODE_CHAR_COUNT:
                return 'too long'
            else:
                self._pu.init()
                self._printer.qr(content, size=5)
                self._printer.text('\n\n')
                self._pu.init()
                return 'ok'
        except:
            return 'failed'
