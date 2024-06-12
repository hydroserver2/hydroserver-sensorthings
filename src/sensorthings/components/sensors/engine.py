from abc import ABCMeta, abstractmethod
from typing import List, Dict


class SensorBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Sensors.

    This class defines the required methods for managing sensors. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_sensors(
            self,
            sensor_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve sensors based on provided parameters.

        Parameters
        ----------
        sensor_ids : List[str], optional
            List of sensor IDs to filter the results.
        pagination : dict, optional
            Pagination information to limit the number of results.
        ordering : dict, optional
            Ordering information to sort the results.
        filters : dict, optional
            Additional filters to apply to the query.
        expanded : bool, optional
            Whether to include expanded information in the results.

        Returns
        -------
        Dict[str, dict]
            A dictionary of sensors, keyed by their IDs.
        int
            The total number of sensors matching the query.
        """

        pass

    @abstractmethod
    def create_sensor(
            self,
            sensor
    ) -> str:
        """
        Create a new sensor.

        Parameters
        ----------
        sensor : dict
            The sensor data to be created.

        Returns
        -------
        str
            The ID of the newly created sensor.
        """

        pass

    @abstractmethod
    def update_sensor(
            self,
            sensor_id: str,
            sensor
    ) -> None:
        """
        Update an existing sensor.

        Parameters
        ----------
        sensor_id : str
            The ID of the sensor to update.
        sensor : dict
            The updated sensor data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_sensor(
            self,
            sensor_id: str
    ) -> None:
        """
        Delete a sensor.

        Parameters
        ----------
        sensor_id : str
            The ID of the sensor to delete.

        Returns
        -------
        None
        """

        pass
