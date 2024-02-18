from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import json
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(), logging.FileHandler('nasa_neows_assignment.log')],
)

class Analysis():

    def __init__(self, analysis_config: str) -> None:
        ''' Load config into an Analysis object

        Load system-wide configuration from `configs/system_config.yml`, user configuration from
        `configs/user_config.yml`, and the specified analysis configuration file

        Parameters
        ----------
        analysis_config : str
            Path to the analysis/job-specific configuration file

        Returns
        -------
        analysis_obj : Analysis
            Analysis object containing consolidated parameters from the configuration files
        '''
        
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]
        logging.info(f'Loading Configs from and sequentially from {paths}')
        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config

    def load_data(self) -> None:
        ''' Retrieve data from NASA's Near Earth Object Web Service (NeoWs) API

        This function makes an HTTPS request to the NeoWs API and retrieves your selected data. 
        The data is stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''
        start_date = self.config["start_date"]
        end_date = self.config["end_date"]
        
        try:
            raw_data = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={self.config["API_KEY"]}').json()
            if raw_data.get("code") == 400:
                print(raw_data["http_error"],raw_data["error_message"])
            data = []
            for (date, value_list) in raw_data["near_earth_objects"].items():
                data += value_list
            self.dataset = pd.DataFrame(data)
            logging.info(f"Data from {start_date} to {end_date} succesfully loaded.")
        except Exception as e:
            logging.error(f"Error while loading data: {e}")
        
        

    def compute_analysis(self) -> float:
        '''Analyze previously-loaded data.

        This function runs an analytical measure computing
        the mean of the absolute_magnitude_h of the asteroids in the loaded dataset
        and returns the statistics in float.

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : float

        '''
        try:
            mean = self.dataset["absolute_magnitude_h"].mean()
            logging.info(f"Mean of absolute_magnitude_h: {mean}")
            return mean
        except Exception as e:
            logging.error(f"Error when computing mean: {e}")

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        ''' Analyze and plot data

        Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
        the path from the configuration file if not specified.

        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure

        Returns
        -------
        fig : matplotlib.Figure

        '''
        fig, ax = plt.subplots(figsize=(self.config["plot_size_h"], self.config["plot_size_w"]))  
        scatter = ax.scatter(self.dataset['id'], self.dataset['absolute_magnitude_h'],c=self.config["plot_color"])  
        ax.set_title(self.config["plot_title"])  
        ax.set_xlabel(self.config["plot_xlabel"])  
        ax.set_ylabel(self.config["plot_ylabel"])  
        plt.xticks(rotation=self.config["plot_xtick_rotation"], fontsize=self.config["plot_xtick_size"])
        if save_path:
            plt.savefig(save_path)
        else:
            plt.savefig(self.config["plot_default_save_path"])  
        plt.show()
        return fig

    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Parameters
        ----------
        message : str
        Text of the notification to send

        Returns
        -------
        None

        '''
        topic = self.config["nfty-topic"]
        message = message

        # send a message through ntfy.sh
        requests.post(
            'https://ntfy.sh/' + topic,
            data=message.encode('utf-8'),
        )
    
nasa_neows = Analysis("configs/job_file.yml")
nasa_neows.load_data()
nasa_neows.compute_analysis()
nasa_neows.plot_data()