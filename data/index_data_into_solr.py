import sys
sys.path.insert(0, '..')

from clients.solr_client import SolrClient
from configs.solr_configs import SOLR_CORE_NAME
from data.data_manager import DataManager


solr = SolrClient(core_name=SOLR_CORE_NAME)
data_manager = DataManager()
solr.clear_docs()
data_manager.import_from_csv('amzn_with_embeddings_and_polarity.csv', 1)