'''
In this section,aim to git patch from MSI dataset.
all_wsi 最开始位置 ；classes返回的类的列表名
'''
import config
from utils_split import split
from pathlib import Path
print("\n\n+++++ Running 1_split.py +++++")

config.args.all_wsi = Path('G:/mars/dataset/')
# config.args.keep_orig_copy

config.args.labels_test = Path('G:/mars/result_exp/label/')
config.args.labels_train = Path('G:/mars/result_exp/label/')
config.args.labels_val = Path('G:/mars/result_exp/label/')
# config.args.test_wsi_per_class
# config.args.val_wsi_per_class

config.args.wsi_test = Path('G:/mars/data/test/')
config.args.wsi_train = Path('G:/mars/data/train/')
config.args.wsi_val =Path('G:/mars/data/val/')

split(all_wsi=config.args.all_wsi,
      classes=config.classes,
      keep_orig_copy=config.args.keep_orig_copy,
      labels_test=config.args.labels_test,
      labels_train=config.args.labels_train,
      labels_val=config.args.labels_val,
      test_wsi_per_class=config.args.test_wsi_per_class,
      val_wsi_per_class=config.args.val_wsi_per_class,
      wsi_test=config.args.wsi_test,
      wsi_train=config.args.wsi_train,
      wsi_val=config.args.wsi_val)
print("+++++ Finished running 1_split.py +++++\n\n")
