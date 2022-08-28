import logging
import sys
from os import path
import json


class LoggerFactory(object):
    _LOG = None
    _log_config = json.load(open('config.json', 'r', encoding='UTF-8'))['logging']

    @staticmethod
    def __create_logger(log_file: str, log_level: str, name: str, enabled: bool):
        log_format = "%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s"

        LoggerFactory._LOG = logging.getLogger(name)

        selected_level = logging.INFO
        if log_level == "INFO":
            selected_level = logging.INFO
        elif log_level == "ERROR":
            selected_level = logging.ERROR
        elif log_level == "DEBUG":
            selected_level = logging.ERROR
        else:
            print(f'Warning: {log_level} is not defined. Using log_level=INFO')
            selected_level = logging.INFO

        LoggerFactory._LOG.setLevel(selected_level)

        logging_handlers = []
        if enabled:
            stream_handler = logging.StreamHandler(sys.stdout)
            # stream_handler.setLevel(selected_level)
            # stream_handler.setFormatter(logging.Formatter(log_format))
            # stream_handler.set_name(name)
            logging_handlers.append(stream_handler)

            file_handler = logging.FileHandler(log_file, encoding='UTF-8')
            file_handler.setLevel(selected_level)
            file_handler.setFormatter(logging.Formatter(log_format))
            file_handler.set_name(name)
            logging_handlers.append(file_handler)

        for handler in logging_handlers:
            LoggerFactory._LOG.handlers.clear()
            LoggerFactory._LOG.addHandler(handler)

        logging.basicConfig(level=selected_level, format=log_format, datefmt="%Y-%m-%d %H:%M:%S",
                            handlers=logging_handlers)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(name: str = 'Satyr'):
        log_file = LoggerFactory._log_config['path']
        log_level = LoggerFactory._log_config['level'].upper()
        log_enabled = LoggerFactory._log_config['enabled']

        if log_level == "INFO":
            selected_level = logging.INFO
        elif log_level == "ERROR":
            selected_level = logging.ERROR
        elif log_level == "DEBUG":
            selected_level = logging.DEBUG
        else:
            print(f'Warning: {log_level} is not defined. Using log_level=INFO')
            selected_level = logging.INFO

        # TODO: Fix logger

        logging.basicConfig(level=selected_level,
                                      format='%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s',
                                      datefmt="%Y-%m-%d %H:%M:%S", filename=log_file)
        # logger = logging.getLogger(name)  # LoggerFactory.__create_logger(log_file, log_level, name, log_enabled)

        return logging.getLogger(name)
