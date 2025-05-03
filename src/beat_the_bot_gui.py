# Frontend file for demo
import dearpygui.dearpygui as dpg
from beat_the_bot_backend import BeatTheBotGame


# Initialize the game context
dpg.create_context()

# Set up the global variables
game_active = False
beat_game = BeatTheBotGame("ai_blackjack/src/trained_blackjack_bot.pth")
player_wins = 0
bot_wins = 0

# Load font
with dpg.font_registry():
    big_font = dpg.add_font("/System/Library/Fonts/Supplemental/Arial.ttf", 24)

# Function just updates scoreboard text
def update_scoreboard():
    dpg.set_value("player_score_text", f"Player Wins: {player_wins}")
    dpg.set_value("bot_score_text", f"Bot Wins: {bot_wins}")

# Function to finish the round and display the results
def finish_round(state, bot_score, player_score):
    global player_wins, bot_wins

    dealer_score = state['dealer_score']

    # Calculate the winner
    def outcome(player_score, dealer_score):
        if player_score > 21:
            return "Bust! Lose."
        elif dealer_score > 21:
            return "Dealer Busts! Win!"
        elif player_score > dealer_score:
            return "Win!"
        elif player_score < dealer_score:
            return "Lose."
        else:
            return "Push."

    # Call the function for both player and bot
    player_outcome = outcome(player_score, dealer_score)
    bot_outcome = outcome(bot_score, dealer_score)

    final_message = f"You vs Dealer: {player_outcome}\nBot vs Dealer: {bot_outcome}"

    if player_score <= 21 and (player_score > dealer_score or dealer_score > 21):
        player_wins += 1

    if bot_score <= 21 and (bot_score > dealer_score or dealer_score > 21):
        bot_wins += 1

    update_scoreboard()

    # Update the scoreboard
    dpg.set_value("victory_message", final_message)
    dpg.configure_item("victory_banner", show=True)

    # Configure themes
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (200, 0, 0), category=dpg.mvThemeCat_Core)

    with dpg.theme() as text_theme:
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)

    dpg.bind_item_theme("victory_banner", window_theme)
    dpg.bind_item_theme("victory_message", text_theme)
    dpg.bind_item_font("victory_message", big_font)

    global game_active
    game_active = False

    dpg.configure_item("hit_button", enabled=False)
    dpg.configure_item("stand_button", enabled=False)
    dpg.configure_item("start_button", enabled=True)

# Function to draw the hands of the dealer, player, and bot
def draw_hand(group_tag, cards):
    value_map = {
        "1": "A", "11": "J", "12": "Q", "13": "K",
        "2": "2", "3": "3", "4": "4", "5": "5",
        "6": "6", "7": "7", "8": "8", "9": "9", "10": "10"
    }
    suit_map = {"h": "H", "d": "D", "c": "C", "s": "S"}

    dpg.delete_item(group_tag, children_only=True)
    dpg.add_spacer(width=100, parent=group_tag)

    # Configure themes for the cards
    for card in cards:
        with dpg.child_window(width=60, height=90, border=True, menubar=False, parent=group_tag) as card_window:
            if card == "HIDDEN":
                dpg.add_text("", pos=[15, 35])
            elif "-" in card:
                # Split into value and suit then display from the above maps
                value, suit = card.split("-")
                value_display = value_map.get(value.strip(), "?")
                suit_display = suit_map.get(suit.strip().lower(), "?")
                clean_card = f"{value_display}{suit_display}"
                dpg.add_text(clean_card)
            else:
                dpg.add_text(card, pos=[15, 35])

            with dpg.theme() as card_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (200, 0, 0), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.bind_item_theme(card_window, card_theme)

# All functionalities of the start button
def start_game_callback():
    global game_active
    game_active = True

    # Fresh game state and turn off banner
    dpg.configure_item("victory_banner", show=False)
    state = beat_game.start_game()

    dealer_hand_to_show = []
    # Helps handle hidden cards for the dealer
    if len(state["dealer_hand"]) >= 2:
        dealer_hand_to_show = [state["dealer_hand"][0], "HIDDEN"]
    else:
        dealer_hand_to_show = state["dealer_hand"]

    # Draw the hands
    draw_hand("dealer_hand_group", dealer_hand_to_show)
    draw_hand("player_hand_group", state["player_hand"])
    draw_hand("bot_hand_group", ["TBD"])

    # Set the scores
    dpg.set_value("dealer_current_score", f"{state['dealer_visible_score']}")
    dpg.set_value("player_current_score", f"{state['player_score']}")
    dpg.set_value("bot_current_score", "TBD")

    # Enable/disable buttons
    dpg.configure_item("hit_button", enabled=True)
    dpg.configure_item("stand_button", enabled=True)
    dpg.configure_item("start_button", enabled=False)

# Functionality for the hit and stand buttons
def hit_callback():
    # Call backend function to get the new state
    state = beat_game.player_hit()

    draw_hand("player_hand_group", state["player_hand"])
    dpg.set_value("player_current_score", f"{state['player_score']}")

    # Proceed to bot if the player is done
    if beat_game.player_done:
        proceed_to_bot()

def stand_callback():
    # Get the state and go straight to the bot
    beat_game.player_stand()
    proceed_to_bot()

# Functionality for the bot's turn
def proceed_to_bot():
    # Bot plays full turn
    bot_state = beat_game.bot_play()
    draw_hand("bot_hand_group", bot_state["player_hand"])
    dpg.set_value("bot_current_score", f"{bot_state['player_score']}")
    proceed_to_dealer(bot_state)

# Function for dealer to finish the round
def proceed_to_dealer(bot_state):
    # Dealer plays full turn
    dealer_final = beat_game.dealer_finish()
    draw_hand("dealer_hand_group", dealer_final["dealer_hand"])
    dpg.set_value("dealer_current_score", f"{dealer_final['dealer_score']}")

    player_score = beat_game.state['player_score']
    bot_score = bot_state['player_score']
    # Final outcomes back to finish round
    finish_round(dealer_final, bot_score, player_score)

# Main window and all the components
with dpg.window(label="Beat the Bot Blackjack", width=1000, height=750):
    # Bannner
    with dpg.child_window(width=400, height=80, pos=[600, 40], tag="victory_banner", show=False, border=False):
        dpg.add_spacer(width=500)
        dpg.add_text("", tag="victory_message", wrap=800)

    dpg.add_spacer(height=10)
    # All the different score text, windows/containers for hands etc.
    dpg.add_text("Dealer's Hand", tag="dealer_hand_text")
    dpg.add_text("", tag="dealer_current_score")

    dpg.add_spacer(height=10)
    with dpg.child_window(width=500, height=120, autosize_y=False, border=False):
        with dpg.group(horizontal=True, tag="dealer_hand_group"):
            pass

    dpg.add_spacer(height=30)
    dpg.add_text("Player's Hand", tag="player_hand_text")
    dpg.add_text("", tag="player_current_score")

    dpg.add_spacer(height=10)
    with dpg.child_window(width=1000, height=120, autosize_y=False, border=False):
        with dpg.group(horizontal=True, tag="player_hand_group"):
            pass

    dpg.add_spacer(height=30)
    dpg.add_text("Bot's Hand", tag="bot_hand_text")
    dpg.add_text("", tag="bot_current_score")

    dpg.add_spacer(height=10)
    with dpg.child_window(width=1000, height=120, autosize_y=False, border=False):
        with dpg.group(horizontal=True, tag="bot_hand_group"):
            pass

    dpg.add_spacer(height=30)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=100)
        dpg.add_button(label="Start Game", width=200, height=50, callback=start_game_callback, tag="start_button")
        dpg.add_spacer(width=50)
        dpg.add_button(label="Hit", width=200, height=50, callback=hit_callback, tag="hit_button", enabled=False)
        dpg.add_spacer(width=50)
        dpg.add_button(label="Stand", width=200, height=50, callback=stand_callback, tag="stand_button", enabled=False)

    with dpg.child_window(width=180, height=80, pos=[700, 200], border=True, tag="scoreboard"):
        dpg.add_text("Player Wins: 0", tag="player_score_text")
        dpg.add_text("Bot Wins: 0", tag="bot_score_text")

    # More themes
    with dpg.theme() as scoreboard_theme:
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 100, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255), category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)

    dpg.bind_item_theme("scoreboard", scoreboard_theme)

dpg.create_viewport(title='Beat the Bot Blackjack', width=1000, height=750)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
