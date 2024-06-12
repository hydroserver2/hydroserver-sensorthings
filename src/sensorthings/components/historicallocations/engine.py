from abc import ABCMeta, abstractmethod
from typing import List, Dict


class HistoricalLocationBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Historical Locations.

    This class defines the required methods for managing historical locations. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_historical_locations(
            self,
            historical_location_ids: List[str] = None,
            thing_ids: List[str] = None,
            location_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve historical locations based on provided parameters.

        Parameters
        ----------
        historical_location_ids : List[str], optional
            List of historical location IDs to filter the results.
        thing_ids : List[str], optional
            List of thing IDs to filter the results.
        location_ids : List[str], optional
            List of location IDs to filter the results.
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
            A dictionary of historical locations, keyed by their IDs.
        int
            The total number of historical locations matching the query.
        """

        pass

    @abstractmethod
    def create_historical_location(
            self,
            historical_location
    ) -> str:
        """
        Create a new historical location.

        Parameters
        ----------
        historical_location : dict
            The historical location data to be created.

        Returns
        -------
        str
            The ID of the newly created historical location.
        """

        pass

    @abstractmethod
    def update_historical_location(
            self,
            historical_location_id: str,
            historical_location
    ) -> None:
        """
        Update an existing historical location.

        Parameters
        ----------
        historical_location_id : str
            The ID of the historical location to update.
        historical_location : dict
            The updated historical location data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_historical_location(
            self,
            historical_location_id: str
    ) -> None:
        """
        Delete a historical location.

        Parameters
        ----------
        historical_location_id : str
            The ID of the historical location to delete.

        Returns
        -------
        None
        """

        pass
