import pubmed_parser as pp
from datetime import datetime
import glob
import psycopg2
import psycopg2.extras as extras
import subprocess

class parse_pubmed_xml_and_insert_raw_data:
    
    def __init__(self, conn, input_dir='/zfs/dzrptlab/CDSS/data/pubmed_data/processed_data/', done_dir='/zfs/dzrptlab/CDSS/data/pubmed_data/processed_data/done/', page_size=200):
        self.input_dir = input_dir
        self.done_dir = done_dir
        self.conn = conn
        self.page_size=page_size

    def parse_and_insert_raw_data(self):
        
        files = glob.glob(self.input_dir+'*.xml')
        
        values_list=[]
        
        sql="""Insert into raw_data (id, sys_creation_date, sys_update_date, app_id, other_id, title, authors, pubdate,
        journal, country, full_text, abstract, keywords, source) VALUES %s"""
        
        for file in files:
            dicts_out = pp.parse_medline_xml(file,
                                             year_info_only=False,
                                             nlm_category=False,
                                             author_list=False,
                                             reference_list=False)

            for item in dicts_out:

                inside_tuple=(item['pmid'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              'cdssadmin', None, item['title'], item['authors'], item['pubdate'], item['journal'],
                             item['country'], None, item['abstract'], item['mesh_terms'], 1 )
                values_list.append(inside_tuple)
        
        cursor = self.conn.cursor()
        
        try:
            extras.execute_values(cursor, sql, values_list, page_size = self.page_size)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1
        
        print("execute_values() done")
        cursor.close()
        
        #move all files to done
        for file in files:
            move_command='mv '+ file + ' '+self.done_dir+file.split('/')[-1]+'.done'
            p = subprocess.Popen([move_command], shell=True)
            out, err = p.communicate()
