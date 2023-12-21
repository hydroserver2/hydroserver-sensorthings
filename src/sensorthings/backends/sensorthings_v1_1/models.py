from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    encoding_type = models.CharField(max_length=100)
    location = models.JSONField()
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return self.name


class HistoricalLocation(models.Model):
    time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return f"{self.thing.name} - {self.location.name} - {self.time}"


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    encoding_type = models.CharField(max_length=100)
    metadata = models.TextField()
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return self.name


class ObservedProperty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    definition = models.CharField(max_length=100)
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return self.name


class Datastream(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    observation_type = models.CharField(max_length=100)
    unit_of_measurement = models.CharField(max_length=50)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    observed_property = models.ForeignKey(ObservedProperty, on_delete=models.CASCADE)
    properties = models.JSONField(blank=True, null=True)  # Additional properties field

    def __str__(self):
        return self.name


class FeatureOfInterest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    feature = models.JSONField()
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Observation(models.Model):
    phenomenon_time = models.DateTimeField()
    result = models.FloatField()
    result_time = models.DateTimeField()
    datastream = models.ForeignKey(Datastream, on_delete=models.CASCADE)
    feature_of_interest = models.ForeignKey(FeatureOfInterest, on_delete=models.CASCADE)
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.datastream.name} - {self.result} - {self.phenomenon_time}"
