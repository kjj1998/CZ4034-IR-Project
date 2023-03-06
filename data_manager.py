import csv

from solr_configs import SOLR_BASE_URL, SOLR_CORE_NAME
from solr_client import SolrClient

class DataManager:

    def __init__(self):
        self.solr = SolrClient(core_name=SOLR_CORE_NAME)
    
    def import_from_csv(self, file_path, start=0):
        """
        Import cleaned data from CSV and load into Solr
        :return: Nothing
        """

        with open(file_path, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
        
            for i in range(start):  # start is the row to start to reading from
                next(csv_reader)
            
            docs = []
                
            for product in csv_reader:
                line_count += 1
                print(f'At line {line_count}.')
                
                # Product details
                product_id = product[0]
                asin = product[1]
                name = product[2]
                price = product[3]
                information = product[4]
                rating = product[5]
                review = product[6]
                review_rating = int(float(product[7]))
                amazon_image_url = product[8]
                vector = [float(x) for x in ast.literal_eval(product[9])]
                
                doc = {
                    "id": product_id,
                    "asin": asin,
                    "name": name,
                    "price": price,
                    "information": information,
                    "rating": rating,
                    "review": review,
                    "review_rating": review_rating,
                    "amazon_image_url": amazon_image_url,
                    "vector": vector
                }
        
                docs.append(doc)
        
            # print(f'Processed {line_count} lines.')
        
        res = self.solr.add_multiple_docs(docs=docs)
            
        # print(res.text)