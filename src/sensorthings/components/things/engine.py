from abc import ABCMeta, abstractmethod
from typing import List, Dict


class ThingBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Things.

    This class defines the required methods for managing things. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_things(
            self,
            thing_ids: List[str] = None,
            location_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve things based on provided parameters.

        Parameters
        ----------
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
            A dictionary of things, keyed by their IDs.
        int
            The total number of things matching the query.
        """

        pass

    @abstractmethod
    def create_thing(
            self,
            thing
    ) -> str:
        """
        Create a new thing.

        Parameters
        ----------
        thing : dict
            The thing data to be created.

        Returns
        -------
        str
            The ID of the newly created thing.
        """

        pass

    @abstractmethod
    def update_thing(
            self,
            thing_id: str,
            thing
    ) -> None:
        """
        Update an existing thing.

        Parameters
        ----------
        thing_id : str
            The ID of the thing to update.
        thing : dict
            The updated thing data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_thing(
            self,
            thing_id: str
    ) -> None:
        """
        Delete a thing.

        Parameters
        ----------
        thing_id : str
            The ID of the thing to delete.

        Returns
        -------
        None
        """

        pass
