from pokemontcgsdk import Card
from typing import List
import pandas as pd


class CardsInfo:
    """
    A class for managing and retrieving information about pokemon TCG cards using the pokemontcgsdk.
    """
    @staticmethod
    def _recursive_getattr(obj, prop):
        """
        Recursively retrieves attributes from an object based on a dot-separated property string

        :param obj: an object
        :param prop: property of the object
        :return: The value of the specified property or None if not found.
        """
        if '.' in prop:
            first, rest = prop.split('.', 1)
            return CardsInfo._recursive_getattr(getattr(obj, first), rest)
        else:
            return getattr(obj, prop, None)


    @staticmethod
    def _append_cards_to_df(cards: List[Card], df: pd.DataFrame, cards_properties: List[str]) -> pd.DataFrame:
        """
        Append the pokemontcgsdk Card object properties (cards_properties) of the card list (param cards)
        to the df (param) and returns it

        :param cards: list of pokemontcgsdk Card object
        :param df: Dataframe of cards info
        :param cards_properties: list of properties of the pokemontcgsdk Card object
        :return: Dataframe of cards info
        """
        data = {prop: [CardsInfo._recursive_getattr(card, prop) for card in cards] for prop in cards_properties}
        df_cards = pd.DataFrame(data)
        return pd.concat([df, df_cards], ignore_index=True)

    @staticmethod
    def get_all_sets(cards_properties: List[str]) -> pd.DataFrame:
        """
        Get cards info (defined in the cards_properties param) from all pokemon TCG collections

        :param cards_properties: list of properties of the pokemontcgsdk Card object
        :return: Dataframe with all the cards info (cards_properties) from all pokemon TCG collections
        """
        df_all_collections_cards = pd.DataFrame()
        cards = Card.all()
        return CardsInfo._append_cards_to_df(cards, df_all_collections_cards, cards_properties)

    @staticmethod
    def get_by_sets(list_collections_id: List[str], cards_properties: List[str]) -> pd.DataFrame:
        """
        Get cards info (defined in the cards_properties param) from the pokemon TCG collections specified
        (list_collections_id)

        :param list_collections_id: list of ids of pokemon TCG collections
        :param cards_properties: list of properties of the pokemontcgsdk Card object
        :return: Dataframe with all the cards info (cards_properties) from the pokemon TCG collections specified
        (list_collections_id)
        """
        df_all_collections_cards = pd.DataFrame()

        for collection in list_collections_id:
            cards = Card.where(q=f'set.id:{collection}')
            df_all_collections_cards = CardsInfo._append_cards_to_df(cards, df_all_collections_cards, cards_properties)

        return df_all_collections_cards
