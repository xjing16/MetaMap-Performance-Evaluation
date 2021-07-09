import pubmed_parser as pp
class process_pubmed_raw_xml:
    def __init__(self, output_dir='/zfs/dzrptlab/CDSS/data/pubmed_data/processed_data/'):
        self.pubmed_xml_version='''<?xml version="1.0" encoding="UTF-8" ?>\n'''
        self.pubmed_xml_doctype='''<!DOCTYPE PubmedArticleSet>\n'''
        self.pubmed_xml_articleset_start='''<PubmedArticleSet>\n'''
        self.pubmed_xml_articleset_end="</PubmedArticleSet>"
        self.pubmed_delete_lines = {'''<?xml version="1.0" ?>''', 
                        '''<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">''',
                       '''<PubmedArticleSet>''', '''</PubmedArticleSet>''', '''</PubmedArticleSet><?xml version="1.0" ?>''', '''<?xml version="1.0" encoding="UTF-8" ?>''',
                       '''<!DOCTYPE PubmedArticleSet>'''}
        self.output_dir = output_dir
        self.symbols={'&ge;':'&gt;=', '&le;': '&lt;='}
    
    def convert_pubmed_out_to_xml(self,file):
        
        file_name = file.split('/')[-1].split('.')[0]

        processed_file=self.output_dir+'processed_'+ file_name + '.xml'

        with open(file , encoding="utf8") as file, open(processed_file, 'w', encoding="utf8") as newfile:
            file_str=file.read()
            file_list = file_str.split('\n')

            newfile.write(self.pubmed_xml_version)
            newfile.write(self.pubmed_xml_doctype)
            newfile.write(self.pubmed_xml_articleset_start)
            for line in file_list:
                if line in self.pubmed_delete_lines:
                    continue
                for k in self.symbols.keys():
                    line = line.replace(k,self.symbols[k])

                newfile.write(line+"\n")
            newfile.write(self.pubmed_xml_articleset_end)

        return processed_file 
