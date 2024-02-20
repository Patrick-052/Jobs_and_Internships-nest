#!/usr/bin/env python3
import asyncio
import textwrap
from PIL import Image
import customtkinter as ctk
from Toplevel import TopLevelWindow

Description = ["Jobs", "Internships"]
Engines = ["Indeed", "LinkedIn", "Glassdoor", "Monster", "SimplyHired",
           "ZipRecruiter", "CareerBuilder", "Snagajob"]


class ImageFrame(ctk.CTkFrame):
    """ Class that creates the image frame and the app usage instructions """
    def __init__(self, master):
        super().__init__(master)

        # Top level window
        self.toplevel_window = None

        # Image Manipulation and Display
        self.image = Image.open("./Images/logo.jpeg")
        self.photo = ctk.CTkImage(self.image, size=(360, 350))
        self.Image_label = ctk.CTkLabel(self, image=self.photo,
                                        text="J & I NEST")
        self.Image_label.grid(row=0, column=0, padx=10, pady=(10, 0),
                              sticky="nw")

        # App Usage Instructions
        self.instructions = ctk.CTkButton(self, text="App Usage",
                                          corner_radius=10, border_spacing=10,
                                          height=40, fg_color="blue",
                                          hover_color="green", anchor="center",
                                          command=self.show_instructions)
        self.instructions.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def show_instructions(self):
        """ Function that displays a top level window with instructions on
            how to use the app"""
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.display_instructions()
        self.toplevel_window.lift()
        self.toplevel_window.focus()


class DescriptionFrame(ctk.CTkFrame):
    """ Class that creates the description and engine frame """
    def __init__(self, master):
        super().__init__(master)

        # Top level window
        self.toplevel_window = None

        # Create the Description OptionMenu
        self.description_optionmenu = ctk.CTkOptionMenu(self,
                                                        values=Description,
                                                        width=168)
        self.description_optionmenu.set("Description")
        self.description_optionmenu.grid(row=0, column=1, padx=(5, 0), pady=10,
                                         sticky="w")

        # Create the Engines OptionMenu
        self.engine_optionmenu = ctk.CTkOptionMenu(self, values=Engines,
                                                   width=168)
        self.engine_optionmenu.set("Engine")  # Set the default value
        self.engine_optionmenu.grid(row=0, column=2, padx=(0, 5), pady=10,
                                    sticky="w")

        # Retrieving saved details
        self.pull_button = ctk.CTkButton(self, text="PULL", width=50,
                                         command=self.pull_details)
        self.pull_button.grid(row=1, column=1, padx=(5, 5), pady=(20, 10),
                              sticky="w")

        # Label "last"
        self.last_label = ctk.CTkLabel(self, text="Last", height=40, width=50)
        self.last_label.grid(row=1, column=1, padx=(55, 2), pady=(20, 10),
                             sticky="w")

        # Number of deatils to retrieve
        self.number_of_details = ctk.CTkEntry(self, width=50)
        self.number_of_details.grid(row=1, column=1, padx=(105, 0),
                                    pady=(20, 10), sticky="w")

        # Label "saved"
        self.saved_label = ctk.CTkLabel(self, text="saved", height=40,
                                        width=50)
        self.saved_label.grid(row=1, column=1, padx=(160, 0),
                              pady=(20, 10), sticky="w")

        # Details menu
        self.detail_menu = ctk.CTkOptionMenu(self, values=Description)
        self.detail_menu.grid(row=1, column=2, padx=(5, 0), pady=(20, 10),
                              sticky="w")

        # # Label "details"
        self.details_label = ctk.CTkLabel(self, text="Details")
        self.details_label.grid(row=2, column=1, padx=(65, 10),
                                pady=(0, 10), sticky="w")

    def obtain_query_details(self):
        """ Function that obtains the details to use in the query """
        description = self.description_optionmenu.get()
        engine = self.engine_optionmenu.get()
        no_details = self.number_of_details.get()
        details = self.detail_menu.get()
        query_dict = {"description": description, "engine": engine,
                      "no_details": no_details, "details": details}
        return query_dict

    def pull_details(self):
        """ Function that pulls the saved details from the selected
            description """
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.pull_details()
        self.toplevel_window.lift()
        self.toplevel_window.focus()


class UserInputFrame(ctk.CTkFrame):
    """ Class that creates the user input frame """
    def __init__(self, master, results_frame, **kwargs):
        super().__init__(master, **kwargs)

        # Top level window
        self.toplevel_window = None

        # Frame to be used to display the results
        self.results_frame = results_frame

        # User Input
        self.user_input = ctk.CTkEntry(self, width=230, height=40)
        self.user_input.grid(row=0, column=0, padx=10, pady=(30, 10),
                             sticky="ew")

        self.search_button = ctk.CTkButton(self, text="Search",
                                           corner_radius=10, border_spacing=10,
                                           height=30, fg_color="blue",
                                           hover_color="green",
                                           anchor="center",
                                           command=self.populate_results)
        self.search_button.grid(row=0, column=1, padx=10, pady=(30, 10),
                                sticky="e")

        self.choice_checkbox = ctk.CTkCheckBox(self, text="Remote")
        self.choice_checkbox.grid(row=1, column=0, padx=(50, 10),
                                  pady=(10, 20), sticky="w")

        self.country_choice = ctk.CTkOptionMenu(self, values=["USA", "Canada"],
                                                width=10)
        self.country_choice.set("COUNTRY")
        self.country_choice.grid(row=1, column=1, padx=10, pady=(10, 20),
                                 sticky="w")

    def obtain_user_input(self):
        """ Function that obtains the user input """
        user_in_dict = {}
        if self.user_input.get() != "":
            if self.choice_checkbox.get() == 1 and self.country_choice.get()\
                    != "COUNTRY":
                self.error_window()
            else:
                user_input = self.user_input.get()
                if self.choice_checkbox.get() == 1 and\
                        self.country_choice.get() == "COUNTRY":
                    remote = "Remote"
                    user_in_dict = {"user_input": user_input, "remote": remote}
                elif self.choice_checkbox.get() == 0 and\
                        self.country_choice.get() != "COUNTRY":
                    country = self.country_choice.get()
                    user_in_dict = {"user_input": user_input,
                                    "country": country}
                return user_in_dict

        self.missing_input()

    def missing_input(self):
        """ Function that displays an error message when the user does not
            enter any input """
        self.results_frame.clear_results()
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.error_missing_input()
        self.toplevel_window.lift()
        self.toplevel_window.focus()

    def error_window(self):
        """ Function that displays an error message when the user selects
            both remote and country """
        self.results_frame.clear_results()
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.error_input_details()
        self.toplevel_window.lift()
        self.toplevel_window.focus()

    def populate_results(self):
        """ Function that populates the results frame with the
            search results """
        self.results_frame.clear_results()
        query_details = []
        user_input = self.obtain_user_input()
        if user_input is not None:
            for k in user_input:
                query_details.append(user_input[k])
        self.results_frame.display_results(query_details)


class ResultsFrame(ctk.CTkScrollableFrame):
    """ Class that creates the results frame """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Top level window
        self.toplevel_window = None

    def display_results(self, results):
        """ Function that displays the results of the search """
        for i, result in enumerate(results):
            wrapped_text = textwrap.fill(result, width=20)
            result_label = ctk.CTkLabel(self, text=wrapped_text)
            result_label.grid(row=i, column=0, padx=(10, 80), pady=10,
                              sticky="w")

            button = ctk.CTkButton(self, text="Details",
                                   command=self.show_details)
            button.grid(row=i, column=1, padx=(10, 0), pady=10, sticky="e")

    def show_details(self):
        """ Function that displays the details of the search result """
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.display_details()
        self.toplevel_window.lift()
        self.toplevel_window.focus()

    def clear_results(self):
        """ Function that clears the results frame """
        for widget in self.winfo_children():
            widget.destroy()


class App(ctk.CTk):
    """ Class that creates the main app window """
    def __init__(self):
        super().__init__()

        # Main App Window configuration
        self.title("J & I NEST")
        self.geometry("800x650")
        self.resizable(False, False)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Image and Instructions Frame
        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=0, column=0, sticky="nsw")

        # Description and Engine Frame
        self.DE_Frame = DescriptionFrame(self)
        self.DE_Frame.grid(row=1, column=0, pady=(10, 10), padx=(0, 5),
                           sticky="nsw")

        # Results Frame
        self.results_frame = ResultsFrame(self)
        self.results_frame.grid(row=0, column=1, sticky="nsew",
                                pady=(150, 10), padx=(2, 3), rowspan=2)

        # User Input Frame
        self.user_input = UserInputFrame(self,
                                         results_frame=self.results_frame,
                                         height=150)
        self.user_input.grid(row=0, column=1, sticky="new")


if __name__ == "__main__":
    app = App()
    app.mainloop()
