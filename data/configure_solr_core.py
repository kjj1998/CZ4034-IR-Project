import sys
sys.path.insert(0, '..')

from clients.solr_client import SolrClient
from configs.solr_configs import SOLR_CORE_NAME

solr = SolrClient(core_name=SOLR_CORE_NAME)

# Add vector field type
solr.add_vector_field_type()

# Add field types
solr.add_field("amazon_image_url", "string")
solr.add_field("asin", "text_general")
solr.add_field("information", "text_general")
solr.add_field("name", "text_general")
solr.add_field("price", "pfloat")
solr.add_field("rating", "pfloat")
solr.add_field("review", "text_general")
solr.add_field("review_rating", "pint")
solr.add_field("subjectivity", "text_general")
solr.add_field("vector", "knn_vector")
solr.add_field("prediction", "text_general")

# Add copy fields
solr.add_copy_field("name", "_text_")
solr.add_copy_field("information", "_text_")

