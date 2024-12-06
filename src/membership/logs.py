import pandas as pd
import os

class LogManager:
    LOG_FILE = "log.csv"  # Default file path for the log

    def __init__(self, filepath=LOG_FILE):
        """
        Initialize the LogManager. Load existing data or create an empty DataFrame.
        
        Parameters:
        filepath (str): Path to the log file.
        """
        self.filepath = filepath
        if os.path.exists(filepath):
            self.df = pd.read_csv(filepath)
        else:
            self.df = pd.DataFrame(columns=['date', 'processed', 'is_empty', 'pushed_to_drive'])

    def save(self):
        """
        Save the DataFrame to the file.
        """
        self.df.to_csv(self.filepath, index=False)

    def push_row(self, date, processed, is_empty):
        """
        Add a new row to the DataFrame and save it.

        Parameters:
        date (str): The date to add.
        processed (bool): Whether the item is processed.
        is_empty (bool): Whether the item is empty.
        """
        new_row = pd.DataFrame([{'date': date, 'processed': processed, 'is_empty': is_empty, 'pushed_to_drive': False}])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.save()


    def is_date_in_df(self, date):
        """
        Check if a specific date exists in the DataFrame.

        Parameters:
        date (str): The date to check.

        Returns:
        bool: True if the date exists, False otherwise.
        """
        return not self.df[self.df['date'] == date].empty

    def get_row_stats(self, date):
        """
        Get 'processed' and 'is_empty' values for a specific date.

        Parameters:
        date (str): The date to retrieve values for.

        Returns:
        tuple: (processed, is_empty) if the date is found, otherwise None.
        """
        row = self.df[self.df['date'] == date]
        if not row.empty:
            return row.iloc[0]['processed'], row.iloc[0]['is_empty'], row.iloc[0]['pushed_to_drive']
        return None

    def mark_pushed_to_drive(self, date):
        """
        Mark the 'pushed_to_drive' column as True for a specific date and save the DataFrame.

        Parameters:
        date (str): The date to mark as pushed.
        """
        self.df.loc[self.df['date'] == date, 'pushed_to_drive'] = True
        self.save()
