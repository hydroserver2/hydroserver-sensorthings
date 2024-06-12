from abc import ABCMeta, abstractmethod
from typing import List, Dict


class LocationBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Locations.

    This class defines the required methods for managing locations. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_locations(
            self,
            location_ids: List[str] = None,
            thing_ids: List[str] = None,
            historical_location_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve locations based on provided parameters.

        Parameters
        ----------
        location_ids : List[str], optional
            List of location IDs to filter the results.
        thing_ids : List[str], optional
            List of thing IDs to filter the results.
        historical_location_ids : List[str], optional
            List of historical location IDs to filter the results.
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
            A dictionary of locations, keyed by their IDs.
        int
            The total number of locations matching the query.
        """

        pass

    @abstractmethod
    def create_location(
            self,
            location
    ) -> str:
        """
        Create a new location.

        Parameters
        ----------
        location : dict
            The location data to be created.

        Returns
        -------
        str
            The ID of the newly created location.
        """

        pass

    @abstractmethod
    def update_location(
            self,
            location_id: str,
            location
    ) -> None:
        """
        Update an existing location.

        Parameters
        ----------
        location_id : str
            The ID of the location to update.
        location : dict
            The updated location data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_location(
            self,
            location_id: str
    ) -> None:
        """
        Delete a location.

        Parameters
        ----------
        location_id : str
            The ID of the location to delete.

        Returns
        -------
        None
        """

        pass
