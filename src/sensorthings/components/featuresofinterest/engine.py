from abc import ABCMeta, abstractmethod
from typing import List, Dict


class FeatureOfInterestBaseEngine(metaclass=ABCMeta):
    """
    Abstract base class for handling Features of Interest.

    This class defines the required methods for managing features of interest. These methods must be implemented
    to allow the SensorThings API to interface with an underlying database.
    """

    @abstractmethod
    def get_features_of_interest(
            self,
            feature_of_interest_ids: List[str] = None,
            observation_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (Dict[str, dict], int):
        """
        Retrieve features of interest based on the given criteria.

        Parameters
        ----------
        feature_of_interest_ids : List[str], optional
            List of feature of interest IDs to filter by.
        observation_ids : List[str], optional
            List of observation IDs to filter by.
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
            A tuple containing a dictionary of features of interest and the total count.
        """

        pass

    @abstractmethod
    def create_feature_of_interest(
            self,
            feature_of_interest
    ) -> str:
        """
        Create a new feature of interest.

        Parameters
        ----------
        feature_of_interest : Any
            The feature of interest object to create.

        Returns
        -------
        str
            The ID of the newly created feature of interest.
        """

        pass

    @abstractmethod
    def update_feature_of_interest(
            self,
            feature_of_interest_id: str,
            feature_of_interest
    ) -> None:
        """
        Update an existing feature of interest.

        Parameters
        ----------
        feature_of_interest_id : str
            The ID of the feature of interest to update.
        feature_of_interest : Any
            The updated feature of interest object.

        Returns
        -------
        None
        """

        pass

    @abstractmethod
    def delete_feature_of_interest(
            self,
            feature_of_interest_id: str
    ) -> None:
        """
        Delete an existing feature of interest.

        Parameters
        ----------
        feature_of_interest_id : str
            The ID of the feature of interest to delete.

        Returns
        -------
        None
        """

        pass
