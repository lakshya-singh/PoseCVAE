import os

# os.makedirs('./final_mse',exist_ok=True)
# os.makedirs('./mse_plots',exist_ok=True)


os.makedirs('./final_mse')
os.makedirs('./mse_plots')

chpk = input("Enter full checkpoint name: ")
os.system(f'python test-var_conv_ood_7.py {chpk}')
os.system('python concat_max.py')
os.system('python auc_avenue.py')