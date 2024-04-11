"""
streamlitapp.py
This file contains the class that builds
the Streamlit app.
Author: Karen Sarai Morales Montiel
Creation date: April 5, 2024
"""
import streamlit as st
from streamlit_echarts import st_pyecharts
from classes.blackjackmontecarlo import Blackjack_MonteCarlo

class StreamlitApp():
    def __init__(self):
        #Setting the title to the App
        st.title('Blackjack Monte Carlo Simulation')

        #Setting the sidebar
        st.sidebar.header('Simulation Parameters')
        #Setting the entry box for the number of reputitions.
        n_rep = st.sidebar.number_input('Number of Simulations', value=10000)
        #Setting the entry box for the starting balance in the sidebar
        starting_balance = st.sidebar.number_input('Starting Balance', value=1000)
    
        # Set the maximum bet value to be less than the starting balance
        max_bet = starting_balance - 10  # Adjust the maximum bet limit if needed
        bet = st.sidebar.number_input('Bet Amount', value=100, min_value=1, max_value=max_bet)

        #Set the number of rounds
        rounds = st.sidebar.number_input('Number of Rounds', value=10)
        #Set the multiple win
        multiple_win = st.sidebar.number_input('Multiple Win', value=3.0, step=0.1)
        #Setting the Simulating Texxt
        #st.sidebar.text('Simulating...')
        self.blackjack_simulator = None
        @st.cache_data
        def load_data():
            #Calling the simulation with the parameters given
        
            self.blackjack_simulator = Blackjack_MonteCarlo(n_rep=n_rep, starting_balance=starting_balance, bet=bet, rounds=rounds, multiple_win=multiple_win)
        #Simulate 
            self.blackjack_simulator.simulate()
        load_data()
        #Set header
        st.header('Simulation Results')
        #Set columns to put the numeric data we got
        col1, col2, col3 = st.columns(3)
        #Set first metric, how many rounds does the dealer win per game
        col1.metric('Dealers Wins Per Game', self.blackjack_simulator.get_how_many_rounds_per_game_dealer_wins())
        #Set second metric, the average on how much money the dealers makes per game
        # Get how much money per game the dealer makes
        number_str = str(self.blackjack_simulator.how_much_money_per_game_dealer_makes())
        #Structurate the data so it's easier to visualize
        symbol = "+"
        if number_str[0] == "-":
            number_str = number_str[1:]
            symbol = "-"
        col2.metric('Money Dealers Makes Per Game',f"{symbol}${number_str}")
        #Set third metric, if the dealer has wins or loses
        col3.metric('Does Dealer earns?', self.blackjack_simulator.does_dealer_earn() )

        #Set nex header, how many wins, ties or loses are there in the games
        st.subheader('Games Distribution Percentage')
        st_pyecharts(
        self.blackjack_simulator.games_pie_base(), key="echarts-percentage"
    )  
    #Set nex header, how many wins, ties or loses are there in the games but in bar chart

        st.subheader('Games Distribution Count')
        st_pyecharts(
    self.blackjack_simulator.show_games_distribution_count(), key="echarts-count"
    )  
    #Set next data how many rounds dealer wins
        st.subheader('Rounds Dealer Wins Per Games')

        st.pyplot(self.blackjack_simulator.show_rounds_dealer_wins_per_game())
    #Set the percentage of the money exchanged the dealer gets
        st.subheader('Money Percentage Dealer Gets')
        st.pyplot(self.blackjack_simulator.show_percentage_money_dealer_gets())
        if st.sidebar.button('Run Simulation'):
            self.reset_simulation()

    def reset_simulation(self):
        # Reset simulation parameters
        st.sidebar.text('Simulating...')
        self.blackjack_simulator.simulate()

