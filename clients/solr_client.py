import requests

from configs.solr_configs import SOLR_BASE_URL, SOLR_CORE_NAME


class SolrClient:
    """
    HTTP REST client for Solr
    """

    def __init__(self, core_name):
        self.__base_url = SOLR_BASE_URL
        self.__core_name = core_name

    def __get(self, endpoint, params=None) -> requests:
        return requests.get(url=self.__base_url + endpoint, params=params)

    def __post(self, endpoint, data: dict) -> requests:
        return requests.post(url=self.__base_url + endpoint, json=data)

    def search_query(self, query: dict) -> requests:
        return self.__get(endpoint=f"/solr/{self.__core_name}/query", params=query)

    def get_fields(self):
        """Get all fields in the Solr core's schema."""
        return self.__get(f"/solr/{self.__core_name}/schema/fields/")

    def add_fields(self, fields: dict):
        """Add field(s) to a Solr core's schema."""
        return self.__post(f"/solr/{self.__core_name}/schema", {"add-field": fields})

    def update_fields(self, fields):
        """Update field(s) in a Solr core's schema."""
        return self.__post(
            f"/solr/{self.__core_name}/schema", {"replace-field": fields}
        )

    def add_docs(self, doc: dict):
        """Add a single document to a Solr core."""
        return self.__post(
            f"/solr/{self.__core_name}/update/json/docs?commit=true", doc
        )

    def add_multiple_docs(self, docs: list):
        """Add multiple documents to a Solr core."""
        return self.__post(
            f"/solr/{self.__core_name}/update/json/docs?commit=true", docs
        )

    def delete_docs(self, field, value):
        """Delete documents from a Solr core."""
        return self.__post(
            f"/solr/{self.__core_name}/update?commit=true",
            {"delete": {"query": f"{field}:{value}"}},
        )

    def clear_docs(self):
        """Delete all documents from a Solr core."""
        return self.__post(
            f"/solr/{self.__core_name}/update?commit=true", {"delete": {"query": "*:*"}}
        )
