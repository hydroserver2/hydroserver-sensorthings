from abc import ABCMeta, abstractmethod
from typing import List, Dict


class ObservationBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Observations.

    This class defines the required methods for managing observations. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_observations(
            self,
            observation_ids: List[str] = None,
            datastream_ids: List[str] = None,
            feature_of_interest_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve observations based on provided parameters.

        Parameters
        ----------
        observation_ids : List[str], optional
            List of observation IDs to filter the results.
        datastream_ids : List[str], optional
            List of datastream IDs to filter the results.
        feature_of_interest_ids : List[str], optional
            List of feature of interest IDs to filter the results.
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
            A dictionary of observations, keyed by their IDs.
        int
            The total number of observations matching the query.
        """

        pass

    @abstractmethod
    def create_observation(
            self,
            observation
    ) -> str:
        """
        Create a new observation.

        Parameters
        ----------
        observation : dict
            The observation data to be created.

        Returns
        -------
        str
            The ID of the newly created observation.
        """

        pass

    @abstractmethod
    def update_observation(
            self,
            observation_id: str,
            observation
    ) -> None:
        """
        Update an existing observation.

        Parameters
        ----------
        observation_id : str
            The ID of the observation to update.
        observation : dict
            The updated observation data.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_observation(
            self,
            observation_id: str
    ) -> None:
        """
        Delete an observation.

        Parameters
        ----------
        observation_id : str
            The ID of the observation to delete.

        Returns
        -------
        None
        """

        pass
