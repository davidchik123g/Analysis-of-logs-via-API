import configparser

# Чтение настроек из файла
def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    log_path = config.get('logs', 'directory')
    log_file_mask = config.get('logs', 'file_mask')

    return log_path, log_file_mask