import os
from pprint import pprint

class DeckComparer():
    def __init__(self, file_names):
        # File paths:
        self.mainboard_path = [".\Your deck\Mainboard.txt"]
        self.considering_path = [".\Your deck\Considering.txt"]
        self.inventory_path = [os.path.join(subdir, current_file) for subdir, dirs, files in os.walk(".\Sellers") for current_file in files]
        
        # Store text data as object data:
        self.inventory_data = self.get_data_from_file(self.inventory_path)
        self.mainboard_data = self.get_data_from_file(self.mainboard_path)["Mainboard"]
        self.considering_data = self.get_data_from_file(self.considering_path)["Considering"]

        # Finnished comparisons:
        self.mainboard_cards_compared = self.card_comparer(self.inventory_data, self.mainboard_data)
        self.considering_cards_compared = self.card_comparer(self.inventory_data, self.considering_data)

        # Missing cards:
        self.missing_cards_mainboard = self.get_missing_cards(self.mainboard_data, self.mainboard_cards_compared)
        self.missing_cards_considering = self.get_missing_cards(self.considering_data, self.considering_cards_compared)
        
        # Sellers with most cards:
        self.mainboard_sellers_most_cards = self.seller_card_counter(self.mainboard_cards_compared)
        self.considering_sellers_most_cards = self.seller_card_counter(self.considering_cards_compared)

        # Buylists:
        self.mainboard_buylist = self.create_buylist(self.mainboard_cards_compared)
        self.considering_buylist = self.create_buylist(self.considering_cards_compared)

        # Print elements:
        self.border = "-" * 40
        self.spacing = "\n" * 3

        
    def get_data_from_file(self, file_names):
        """
            Gets the data from each text file, 
            removes basic lands
            and convents it into object data
        """
        cards_data = {}
        basic_lands = ["plains", "island", "swamp", "mountain", "forest"]
        for file_name in file_names:
            cards_data_name = str(file_name.split("\\")[-1][0:-4])
            cards_data[cards_data_name] = {}
            with open(file_name, "r") as current_file:
                for card in current_file:
                    current_card = (card.rstrip("\n")).split(" ", 1)
                    if current_card[1].lower() not in basic_lands:
                        cards_data[cards_data_name][current_card[1]] = int(current_card[0])
        return cards_data


    def card_comparer(self, inventory_list, deck):
        """
            compares cards from Mainboard and Considering
            to find out which seller has the cards and 
            how many they have in stock and returns an object
            with the output data
        """
        cards_data = {}
        for seller_name in inventory_list:
            for card in deck:
                if card in inventory_list[seller_name]:
                    if card in cards_data:
                        cards_data[card].append([seller_name, inventory_list[seller_name][card]])
                    else:
                        cards_data[card] = [[seller_name, inventory_list[seller_name][card]]]
        return cards_data

    def get_missing_cards(self, board, board_compared):
        """ Finds each card which no seller has for sale """
        return [card for card in board if card not in board_compared]
    

    def seller_card_counter(self, board_compared):
        """
            Returns a sorted list of sellers who has the most of the requested cards
            to the sellers who have the least of the requested cards
        """
        card_counter_data = []
        for seller_name in self.inventory_data:
            seller_card_counter = 0
            for card in board_compared:
                if seller_name in sum(board_compared[card], []):
                    seller_card_counter += 1
            card_counter_data.append([seller_name, seller_card_counter])
        sorted_card_counter_data = sorted(card_counter_data, key=lambda l:l[1], reverse=True)
        return sorted_card_counter_data

    
    def create_buylist(self, board):
        """
            Finds the seller with the most available cards from your buy list,
            saves those cards to your buylist. Updates the sellers who now have the most cards
            and buy all the cards from the current seller with the most cards from you buylist.
            This process is repeated untill all cards from you want which a seller has is broght.
        """
        data = {}
        added_cards = []
        cards_compared = board.copy()
        while cards_compared != {}:
            board_counter = self.seller_card_counter(cards_compared)
            best_buyer_name = board_counter[0][0]
            for card in board:
                for i in range(len(board[card])):
                    seller_data = board[card][i]
                    if best_buyer_name in seller_data and card not in added_cards:
                        card_in_stock = [card, seller_data[1]]
                        if best_buyer_name in data:
                            data[best_buyer_name].append(card_in_stock)
                        else:
                            data[best_buyer_name] = [card_in_stock]
                        added_cards.append(card)
                        cards_compared.pop(card)
        return data
            

if __name__ == "__main__":
    # List of file names:
    
    deck_comparer = DeckComparer(file_names="test") 
    
    # -------------------------------------------------------------------- Mainboard data --------------------------------------------------------------------
    # Mainboard collectively cards count:
    print(deck_comparer.border, "Mainboard data", deck_comparer.border)
    print("Sellers has collectively", len(deck_comparer.mainboard_cards_compared), "/", len(deck_comparer.mainboard_data), "cards from Mainboard", "\n")

    # Mainboard data:
    print("Mainboard data:")
    pprint(deck_comparer.mainboard_cards_compared)
    print(deck_comparer.spacing)
    
    # Missing missing cards:
    print("Missing cards in Mainboard:")
    pprint(deck_comparer.missing_cards_mainboard)
    print(deck_comparer.spacing)

    # Mainboard sellers with most cards:
    print("Sellers with the most Mainboard cards:")
    pprint(deck_comparer.mainboard_sellers_most_cards)
    print(deck_comparer.spacing)

    # Mainboard buylist:
    print("Mainboard buylist:")
    pprint(deck_comparer.mainboard_buylist)
    print(deck_comparer.spacing)
    

    # ------------------------------------------------------------------- Considering prints -------------------------------------------------------------------
    # Considering collectively cards count:
    print(deck_comparer.border, "Considering cards", deck_comparer.border)
    print("Sellers has collectively", len(deck_comparer.considering_cards_compared), "/", len(deck_comparer.considering_data), "cards from Considering", "\n")

    # Considering data:
    print("Considering data:")
    pprint(deck_comparer.considering_cards_compared)
    print(deck_comparer.spacing)
    
    # Considering missing cards:
    print("Missing cards in Considering:")
    pprint(deck_comparer.missing_cards_considering)
    print(deck_comparer.spacing)

    # Considering sellers with most cards:
    print("Sellers with the most Considering cards:")
    pprint(deck_comparer.mainboard_sellers_most_cards)
    print(deck_comparer.spacing)

    # Considering buylist:
    print("Considering buylist:")
    pprint(deck_comparer.considering_buylist)