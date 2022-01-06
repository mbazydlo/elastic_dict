class ElasticKeyError(Exception):
    """Base Exception for ElasticKey module"""


class DuplicatedKeyError(ElasticKeyError):
    """Exception being raised when dictionary would potentially has non unique keys"""

