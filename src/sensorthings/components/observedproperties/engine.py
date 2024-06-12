from abc import ABCMeta, abstractmethod
from typing import List, Dict


class ObservedPropertyBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Observed Properties.

    This class defines the required methods for managing observed properties. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_observed_properties(
            self,
            observed_property_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve observed properties based on provided parameters.

        Parameters
        ----------
        observed_property_ids : List[str], optional
            List of observed property IDs to filter the results.
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
            A dictionary of observed properties, keyed by their IDs.
        int
            The total number of observed properties matching the query.
        """

        pass

    @abstractmethod
    def create_observed_property(
            self,
            observed_property
    ) -> str:
        """
        Create a new observed property.

        Parameters
        ----------
        observed_property : dict
            The observed property data to be created.

        Returns
        -------
        str
            The ID of the newly created observed property.
        """

        pass

    @abstractmethod
    def update_observed_property(
            self,
            observed_property_id: str,
            observed_property
    ) -> None:
        """
        Update an existing observed property.

        Parameters
        ----------
        observed_property_id : str
            The ID of the observed property to update.
        observed_property : dict
            The updated observed property data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_observed_property(
            self,
            observed_property_id: str
    ) -> None:
        """
        Delete an observed property.

        Parameters
        ----------
        observed_property_id : str
            The ID of the observed property to delete.

        Returns
        -------
        None
        """

        pass
