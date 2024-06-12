from abc import ABCMeta, abstractmethod
from typing import List, Dict


class DatastreamBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Datastreams.

    This class defines the required methods for managing datastreams. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_datastreams(
            self,
            datastream_ids: List[str] = None,
            observed_property_ids: List[str] = None,
            sensor_ids: List[str] = None,
            thing_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve datastreams based on the given criteria.

        Parameters
        ----------
        datastream_ids : List[str], optional
            List of datastream IDs to filter by.
        observed_property_ids : List[str], optional
            List of observed property IDs to filter by.
        sensor_ids : List[str], optional
            List of sensor IDs to filter by.
        thing_ids : List[str], optional
            List of thing IDs to filter by.
        pagination : dict, optional
            Pagination options.
        ordering : dict, optional
            Ordering options.
        filters : dict, optional
            Additional filtering options.
        expanded : bool, optional
            Whether to include expanded related entities.

        Returns
        -------
        tuple
            A tuple containing a dictionary of datastreams and the total count.
        """

        pass

    @abstractmethod
    def create_datastream(
            self,
            datastream
    ) -> str:
        """
        Create a new datastream.

        Parameters
        ----------
        datastream : Any
            The datastream object to create.

        Returns
        -------
        str
            The ID of the newly created datastream.
        """

        pass

    @abstractmethod
    def update_datastream(
            self,
            datastream_id: str,
            datastream
    ) -> None:
        """
        Update an existing datastream.

        Parameters
        ----------
        datastream_id : str
            The ID of the datastream to update.
        datastream : Any
            The updated datastream object.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_datastream(
            self,
            datastream_id: str
    ) -> None:
        """
        Delete an existing datastream.

        Parameters
        ----------
        datastream_id : str
            The ID of the datastream to delete.

        Returns
        -------
        None
        """

        pass
