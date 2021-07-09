import itertools
from multiprocessing import Pool
import subprocess

class metamap_different_combinations:
    def __init__(self, input_file, out_path='/zfs/dzrptlab/CDSS/data/metamap_data/metamap_different_options/test_5_21/', metamap_path='/zfs/dzrptlab/CDSS/src/metamap/public_mm/bin/metamap', pool_size=5):
        self.default_options = ['--JSONf 2']
        self.experimental_options = ['--conj', '--prune 10','--no_prune', '--no_tagging', '--no_derivational_variants', 
                                     '--all_derivational_variants', '-a', '-u', '-l', '-r 700', '-i', '-y']
        self.input_file = input_file
        self.out_path = out_path
        self.metamap_path = metamap_path
        self.pool_size = pool_size
        
        
    def f(self, i):
        command = self.metamap_path
        options=''
        for opt in self.default_options:
            options = options+opt+' '
        options = options+ ' '.join(i)+' '
        out_file_name = '_'.join(i).replace(' ','_').replace('-','')
        options = options + self.input_file + ' '+ self.out_path + out_file_name

        command = command + ' ' + options
        print(command)
        #p = subprocess.call([command], shell=True)
        p = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        p.wait()
    
    def run(self):
        comb = itertools.combinations(self.experimental_options, 2)
        with Pool(self.pool_size) as p:
            p.map(self.f, comb)
