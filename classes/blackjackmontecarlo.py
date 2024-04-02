from classes.blackjack import Blackjack_Game
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar
from io import BytesIO
import numpy as np
import seaborn as sns

class Blackjack_MonteCarlo():
    def __init__(self, n_rep=10000, starting_balance=100, bet=10, rounds=10, multiple_win=3):
        self.n_rep = n_rep
        self.starting_balance = starting_balance
        self.bet = bet
        self.rounds = rounds
        self.multiple_win = multiple_win
        self.blackjack_df = None
        self.pct_winning_money_mean = 0
        self.pct_losing_money_mean = 0
        self.pct_exchanged_money_mean = 0
        
    def simulate(self):
        results = []
        for _ in range(self.n_rep):
            game = Blackjack_Game(starting_balance=self.starting_balance, multiple_win=self.multiple_win, bet=self.bet)
            pct_result = game.play(rounds_to_play=self.rounds)
            results.append(pct_result) 
        self.blackjack_df = pd.DataFrame(columns=['n_win_rounds', 'n_lose_rounds', 'winning_money' , 'losing_money', 'final_balance' , 'starting_balance'],
                             data=results)
        self.transform_data()

    def transform_data(self):
        def win_determinator(win, lose):
            if win > lose :
                return "win"
            elif win < lose :
                return "lose"
            else:
                return "tie"
        self.blackjack_df['total_rounds'] = self.blackjack_df.apply(lambda row: row['n_win_rounds']+ row['n_lose_rounds'], axis=1)
        self.blackjack_df['pct_win_rounds'] = self.blackjack_df.apply(lambda row: row['n_win_rounds']/row['total_rounds'], axis = 1)
        self.blackjack_df['pct_lose_rounds'] = self.blackjack_df.apply(lambda row: row['n_lose_rounds']/row['total_rounds'], axis = 1)
        self.blackjack_df['total_exchanged_money'] = self.blackjack_df.apply(lambda row: row['winning_money']+row['losing_money'], axis = 1)
        self.blackjack_df['pct_win_money'] = self.blackjack_df.apply(lambda row: row['winning_money']/row['total_exchanged_money'], axis = 1)
        self.blackjack_df['pct_lose_money'] = self.blackjack_df.apply(lambda row: row['losing_money']/row['total_exchanged_money'], axis = 1)
        self.blackjack_df['result'] = self.blackjack_df[['n_win_rounds', 'n_lose_rounds']].apply(lambda row: win_determinator(row['n_win_rounds'], row['n_lose_rounds']), axis=1)
        self.pct_winning_money_mean = self.blackjack_df['pct_win_money'].mean()
        self.pct_losing_money_mean = self.blackjack_df['pct_lose_money'].mean()
        self.pct_exchanged_money_mean = self.blackjack_df['total_exchanged_money'].mean()
        

    def get_how_many_rounds_per_game_house_wins(self):
        pct_win_dealer = self.blackjack_df['n_lose_rounds'].mean()
        return pct_win_dealer
    
    def how_much_money_per_game_house_makes(self):
        pct_winning_money_mean = self.blackjack_df['pct_win_money'].mean()
        pct_losing_money_mean = self.blackjack_df['pct_lose_money'].mean()
        earnings = self.pct_exchanged_money_mean*(pct_losing_money_mean - pct_winning_money_mean)
        return round(earnings)
    
    def how_much_total_money_house_makes(self):
      game_earning = self.how_much_money_per_game_house_makes()
      return game_earning*self.n_rep
    
    def does_house_earn(self):
        earnings = self.how_much_money_per_game_house_makes()
        return earnings > 0
    
    def result_games_distribution_pct(self):
        result_counts_df = self.blackjack_df['result'].value_counts().reset_index()
        result_counts_df.set_index('index', inplace=True)
        result_counts_df = result_counts_df.rename(index={'win': 'lose', 'lose': 'win'}, columns={'result': 'counts'})
        total_games = result_counts_df['counts'].sum()
        # Correctly access the columns after renaming
        pct_win_games = result_counts_df.loc['win', 'counts'] / total_games
        pct_lose_games = result_counts_df.loc['lose', 'counts'] / total_games
        pct_tie_games = result_counts_df.loc['tie', 'counts'] / total_games
        return {'win': pct_win_games, 'tie': pct_tie_games, 'lose': pct_lose_games}

        
    
    def show_games_distribution_count(self):
        result_counts_df = self.blackjack_df['result'].value_counts().reset_index()
        result_counts_df.set_index('index', inplace=True)
        result_counts_df = result_counts_df.rename(index={'win': 'lose', 'lose': 'win'}, columns={'result': 'counts'})
        x_axis = list(result_counts_df.index)
        y_axis = list(result_counts_df.counts)
        b = (
    Bar()
    .add_xaxis(x_axis)
    .add_yaxis("Counts of Games", y_axis)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Games Distribution", subtitle="Count of Games"
        ),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
        return b
    

    def show_rounds_house_wins_per_game(self):
    # Create a new figure
        fig, ax = plt.subplots(figsize=(8, 6))
    
    # Get data
        x = self.blackjack_df['n_lose_rounds']
    
    # Plot histogram
        result = ax.hist(x, bins=10, color='c', edgecolor='k', alpha=0.65)
    
    # Add mean and median lines
        ax.axvline(x.mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
        ax.axvline(x.median(), color='blue', linestyle='dashed', linewidth=1, label="Median")
    
        # Add text annotations
        ax.text(x.mean(), max(result[0]) * 1, f' {x.mean():.2f}', color='red', verticalalignment='bottom', horizontalalignment='left')
        ax.text(x.median(), max(result[0]) * 1, f'{x.median():.2f}', color='blue', verticalalignment='bottom', horizontalalignment='right')
    
        # Set title and legend
        ax.set_title("Rounds Houses Wins Per Game")
        ax.legend()

        # Return the figure object
        return fig

    def show_percentage_money_house_gets(self):  
        # Create a new figure
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Get data
        x = self.blackjack_df['pct_lose_money']
    
        # Plot histogram
        result = ax.hist(x, bins=10, color='c', edgecolor='k', alpha=0.65)
    
        # Add mean and median lines
        ax.axvline(x.mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
        ax.axvline(x.median(), color='blue', linestyle='dashed', linewidth=1, label="Median")
    
        # Add text annotations
        ax.text(x.mean(), max(result[0]) * 1, f' {x.mean():.2f}', color='red', verticalalignment='bottom', horizontalalignment='left')
        ax.text(x.median(), max(result[0]) * .96, f'{x.median():.2f}', color='blue', verticalalignment='bottom', horizontalalignment='right')
    
        # Set title and legend
        ax.set_title('Percentage of Money House Gets')
        ax.legend()

        # Return the figure object
        return fig
