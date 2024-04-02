import streamlit as st
from streamlit_echarts import st_pyecharts
from classes.blackjackmontecarlo import Blackjack_MonteCarlo

class StreamlitApp():
    def __init__(self):
        st.title('Blackjack Monte Carlo Simulation')

        st.sidebar.header('Simulation Parameters')
        n_rep = st.sidebar.number_input('Number of Simulations', value=10000)
        starting_balance = st.sidebar.number_input('Starting Balance', value=1000)
    
        # Set the maximum bet value to be less than the starting balance
        max_bet = starting_balance - 10  # Adjust the maximum bet limit if needed
        bet = st.sidebar.number_input('Bet Amount', value=100, min_value=1, max_value=max_bet)
    
        rounds = st.sidebar.number_input('Number of Rounds', value=10)
        multiple_win = st.sidebar.number_input('Multiple Win', value=3.0, step=0.1)

        st.sidebar.text('Simulating...')
        self.blackjack_simulator = Blackjack_MonteCarlo(n_rep=n_rep, starting_balance=starting_balance, bet=bet, rounds=rounds, multiple_win=multiple_win)
        self.blackjack_simulator.simulate()
        number_str = str(self.blackjack_simulator.how_much_money_per_game_house_makes())[::-1]
        symbol = "+"
        if number_str[-1] == "-":
            number_str = number_str[:-1]
            symbol = "-"

        st.header('Simulation Results')
    
        col1, col2, col3 = st.columns(3)
        
        col1.metric('House Wins Per Game', self.blackjack_simulator.get_how_many_rounds_per_game_house_wins())
        col2.metric('Money House Makes Per Game',f"{symbol}${formatted_number}")
        col3.metric('Does House earns?', self.blackjack_simulator.does_house_earn() )

        st.subheader('Games Distribution Percentage')
        st_pyecharts(
        self.blackjack_simulator.games_pie_base(), key="echarts-percentage"
    )  

        st.subheader('Games Distribution Count')
        st_pyecharts(
    self.blackjack_simulator.show_games_distribution_count(), key="echarts-count"
    )  
    
        st.subheader('Rounds House Wins Per Games')

        st.pyplot(self.blackjack_simulator.show_rounds_house_wins_per_game())
        st.subheader('Money Percentage House Gets')
        st.pyplot(self.blackjack_simulator.show_percentage_money_house_gets())

