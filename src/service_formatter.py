import logging

class ServiceFormatter(logging.Formatter):
    def __init__(self, format_str, datefmt):
        super().__init__()
        self.format_str = format_str
        self.datefmt= datefmt
        self.escape_chars = ''.join([chr(i) for i in range(1, 32)])

    def format(self, record):
        record.message = record.msg.translate(str.maketrans('', '', self.escape_chars))
        record.asctime = self.formatTime(record, self.datefmt)
        formatted_msg  = self.format_str.format(
            levelname=record.levelname,
            message=record.msg,
            time=record.asctime,
            name=record.name
            # Add more placeholders as needed
        )
        return formatted_msg