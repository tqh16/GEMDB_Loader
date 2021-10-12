import os
from . import setting
import json
import shutil
from tqdm import tqdm


def _check_market(market):
    if market in setting.market_list:
        return True
    else:
        raise ValueError(f'The market ({market}) is not in the support list!')


def _check_setting():
    if setting.path_root is None:
        raise ValueError('The GEMDB data directory path is not set!')


def _get_market_path(market):
    return os.path.join(setting.path_root, setting.path_market_relative[market])


def _get_market_abstract(market):
    _check_market(market)
    _check_setting()
    market_path = _get_market_path(market)

    try:
        with open(os.path.join(market_path, 'market_abstract.json'), 'r') as f:
            market_abstract = json.load(f)
    except:
        raise NotImplementedError(f'Market information does not exist!')
    return market_abstract


def _get_data_abstract(market, market_abstract, data):
    data_dir = market_abstract[data]['dir_name']

    try:
        with open(os.path.join(_get_market_path(market), data_dir, 'abstract.json'), 'r') as f:
            data_abstract = json.load(f)
    except:
        raise NotImplementedError(f'Data information does not exist!')
    return data_abstract


def set_GEMDB_dir(dir: str):
    setting.path_root = dir
    return


def list_market():
    return setting.market_list


# def list_market_data(market_name: str):
#     market_abstract = _get_market_abstract(market_name)
#     return market_abstract.keys()
def list_market_data(market_name: str):
    _check_market(market_name)
    _check_setting()
    market_path = _get_market_path(market_name)
    data_dirs = os.listdir(market_path)
    return data_dirs


# def list_data_range(market_name: str, data_name: str):
#     market_abstract = _get_market_abstract(market_name)
#     data_abstract = _get_data_abstract(market_name, market_abstract, data_name)
#     return (data_abstract['fr'], data_abstract['to'])
def list_data_range(market_name: str, data_name: str):
    _check_market(market_name)
    _check_setting()
    market_path = _get_market_path(market_name)
    data_dir = os.path.join(market_path,data_name)

    data_filenames = os.listdir(data_dir)
    data_filenames.sort()

    return (data_filenames[0], data_filenames[-1])


def copy_data(market_name: str, data_name: str, save_dir: str, fr: str = None, to: str = None):
    _check_market(market_name)
    _check_setting()
    market_path = _get_market_path(market_name)
    data_dir = os.path.join(market_path,data_name)
    data_filenames = os.listdir(data_dir)
    data_filenames.sort()

    if fr is None:
        fr = data_filenames[0]
    if to is None:
        to = data_filenames[-1]
    print(f'Copy data from {fr} to {to}...')
    print('It may take a long time, please wait.')

    data_filenames_selected = []    
    for filename in data_filenames:
        if fr <= filename < to:
            data_filenames_selected.append(filename)

    for filename in tqdm(data_filenames_selected):
        source_path = os.path.join(data_dir, filename)
        target_path = os.path.join(save_dir, filename)
        try:
            shutil.copy(source_path, target_path)
        except:
            raise RuntimeError(f'Copy Error when copy file {filename}')
    
    print('Finish!')
    return
