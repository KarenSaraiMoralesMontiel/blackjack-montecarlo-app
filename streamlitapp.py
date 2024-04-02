import streamlit as st
from streamlit_echarts import st_pyecharts
from classes.blackjackmontecarlo import Blackjack_MonteCarlo

class StreamlitApp():
    def __init__(self):
        st.title('Blackjack Monte Carlo Simulation')

        st.sidebar.header('Simulation Parameters')
        n_rep = st.sidebar.number_input('Number of Simulations', value=10000)
        starting_balance = st.sidebar.number_input('Starting Balance', value=100)
    
        # Set the maximum bet value to be less than the starting balance
        max_bet = starting_balance - 10  # Adjust the maximum bet limit if needed
        bet = st.sidebar.number_input('Bet Amount', value=10, min_value=1, max_value=max_bet)
    
        rounds = st.sidebar.number_input('Number of Rounds', value=10)
        multiple_win = st.sidebar.number_input('Multiple Win', value=3.0, step=0.1)

        st.sidebar.text('Simulating...')
        self.blackjack_simulator = Blackjack_MonteCarlo(n_rep=n_rep, starting_balance=starting_balance, bet=bet, rounds=rounds, multiple_win=multiple_win)
        self.blackjack_simulator.simulate()

        st.header('Simulation Results')
    
        col1, col2, col3 = st.columns(3)
        col1.metric('House Wins Per Game', self.blackjack_simulator.get_how_many_rounds_per_game_house_wins())
        col2.metric('Total Money House Makes', self.blackjack_simulator.how_much_total_money_house_makes())
        col3.metric('Does House earns?', self.blackjack_simulator.does_house_earn() )

        st.subheader('Games Distribution Percentage')
        games_distribution = self.blackjack_simulator.result_games_distribution_pct()
        st.write(f"Win Percentage: {games_distribution['win']:.2%}")
        st.write(f"Lose Percentage: {games_distribution['lose']:.2%}")
        st.write(f"Tie Percentage: {games_distribution['tie']:.2%}")

        st.subheader('Games Distribution Count')
        st_pyecharts(
    self.blackjack_simulator.show_games_distribution_count(), key="echarts"
    )  
    
    #st.pyplot(blackjack_simulator.show_games_distribution())
        st.subheader('Rounds House Wins Per Games')

        st.pyplot(self.blackjack_simulator.show_rounds_house_wins_per_game())
        st.subheader('Money Percentage House Gets')
        st.pyplot(self.blackjack_simulator.show_percentage_money_house_gets())
