#!/usr/bin/env python3
import customtkinter as ctk


class TopLevelWindow(ctk.CTkToplevel):
    """ Class that creates the top level windows for the app"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.geometry("400x300")
        self.resizable(False, False)

    def display_instructions(self):
        """ Function that displays the instructions for using the app """
        self.title("App Usage")
        instructions = ctk.CTkLabel(self, text="Instructions")
        instructions.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def pull_details(self):
        """ Function that displays the details of the search result """
        self.title("Saved Details")
        details = ctk.CTkLabel(self, text="Pulled Details")
        details.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def display_details(self):
        """ Function that displays the details of the search result """
        self.title("Details")
        details = ctk.CTkLabel(self, text="Details")
        details.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def error_input_details(self):
        """ Function that displays an error message when the user selects
            both remote and country """
        self.title("Error")
        self.geometry("300x100")
        error_message = ctk.CTkLabel(self, text="Please select either remote"
                                     " or country, not both")
        error_message.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def error_missing_input(self):
        """ Function that displays an error message when the user does not
            enter any input """
        self.title("Error")
        self.geometry("300x100")
        error_message = ctk.CTkLabel(self, text="Please enter a search input")
        error_message.grid(row=0, column=0, padx=10, pady=10, sticky="w")
