from django.db import models

# Create your models here.
class Endpoint(models.Model):
    """
    The Endpoint object represents ML API endpoint.

    Attributes:
        name: the name of the endpoint, it will be used in API URL,
        owner: the string with owner name,
        created_at: the date when the endpoint was created
    '''
    """
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class MLAlgorithm(models.Model):
    """
    The MLAlgorithm object represents the ML Algorithms.

    Attributes:
        name: name of the ML algorithm,
        description: a short description of the ML algorithm,
        code: code of the ML algorithm,
        version: version of the ML algorithm,
        owner: name of owner,
        created_at: the date when the ML algorithm was created,
        parent_endpoint: the reference to the endpoint
    """
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    code = models.TextField(max_length=50000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)


class MLAlgorithmStatus(models.Model):
    """
    The MLAlgorithmStatus object represents the status of the ML algorithm which can change over time.

    Attributes:
        status: the status of the algorithm in the endpoint.
                Can be [testing, staging, production, ab_testing]
        active: boolean flag to point to current active status,
        created_by: name of the creator,
        created_at: the date when the status was created,
        parent_mlalgorithm: the reference to the corresponding MLAlgorithm
    """
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm,
                                           on_delete=models.CASCADE, related_name="status")


class MLRequest(models.Model):
    """
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        full_response: The response of the ML algorithm.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
    """
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
