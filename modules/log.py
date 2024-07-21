import logging
import pprint

def create_logger(name="FAI_Node", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(console_formatter)
    
    def pprint_data(data, indent=4):
        pp = pprint.PrettyPrinter(indent=indent)
        if isinstance(data, str):
            logger.info(data)
        else:
            data_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s\n%(message)s')
            handler.setFormatter(data_formatter)
            logger.info(pp.pformat(data))
            handler.setFormatter(console_formatter)
    
    logger.data = pprint_data
    return logger
