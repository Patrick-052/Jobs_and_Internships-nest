#!/usr/bin/env python3
import asyncio
import textwrap
from PIL import Image
import customtkinter as ctk
from APIs.Jobs import Serp as sp
from APIs.Jobs import Findwork as fw
from Toplevel import TopLevelWindow

Description = ["Description", "Jobs", "Internships"]
Engines = ["Engine", "Findwork", "Serp", "USA Jobs"]


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
        self.engine_optionmenu.set("Engine")
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
        self.detail_menu.set("Description")
        self.detail_menu.grid(row=1, column=2, padx=(5, 0), pady=(20, 10),
                              sticky="w")

        # # Label "details"
        self.details_label = ctk.CTkLabel(self, text="Details")
        self.details_label.grid(row=2, column=1, padx=(65, 10),
                                pady=(0, 10), sticky="w")

    def obtain_dec_details(self):
        """ Function that obtains the details to use in the query """
        desc = self.description_optionmenu.get()
        engine = self.engine_optionmenu.get()
        if desc == "Description" or engine == "Engine" or \
                desc == "Description" and engine == "Engine":
            self.wrong_input()
        dec_dict = {"description": desc, "engine": engine}
        return dec_dict

    def obtain_pull_details(self):
        """ Function that obtains the details to use in the query """
        no_details = self.number_of_details.get()
        details = self.detail_menu.get()
        if no_details == "" and details == "Description" or details !=\
                "Description" and no_details == "" or details == "Description"\
                and no_details != "":
            self.error_window()
        elif no_details != "" and details != "Description":
            pull_dict = {"no_details": no_details, "details": details}
            return pull_dict

    def pull_details(self):
        """ Function that pulls the saved details from the selected
            description """
        Query = self.obtain_pull_details()
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.pull_details(Query)
        self.toplevel_window.lift()
        self.toplevel_window.focus()

    def error_window(self):
        """ Function that displays an error message when the user does not
            enter any input """
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.error_missing_query()
        self.toplevel_window.lift()
        self.toplevel_window.focus()

    def wrong_input(self):
        """ Function that displays an error message when the user does not
            select any input/selects a single wrong input """
        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.error_wrong_input()
        self.toplevel_window.lift()
        self.toplevel_window.focus()


class UserInputFrame(ctk.CTkFrame):
    """ Class that creates the user input frame """
    def __init__(self, master, app_instance,
                 results_frame, DE_Frame, **kwargs):
        super().__init__(master, **kwargs)

        # Top level window
        self.toplevel_window = None

        # Frame to be used to display the results
        self.app_instance = app_instance
        self.results_frame = results_frame
        self.DE_Frame = DE_Frame

        # User Input
        self.user_input = ctk.CTkEntry(self, width=230, height=40)
        self.user_input.grid(row=0, column=0, padx=10, pady=(30, 10),
                             sticky="ew")

        self.search_button = ctk.CTkButton(self, text="Search",
                                           corner_radius=10, border_spacing=10,
                                           height=30, fg_color="blue",
                                           hover_color="green",
                                           anchor="center",
                                           command=self.search_button_clicked)
        self.search_button.grid(row=0, column=1, padx=10, pady=(30, 10),
                                sticky="e")

        self.choice_checkbox = ctk.CTkCheckBox(self, text="Remote")
        self.choice_checkbox.grid(row=1, column=0, padx=(50, 10),
                                  pady=(10, 20), sticky="w")

        self.country_label = ctk.CTkLabel(self, text="Country/City")
        self.country_label.grid(row=1, column=0, padx=(190, 0), pady=(10, 20),
                                sticky="w")

        self.country_choice = ctk.CTkEntry(self, width=110, height=30)
        self.country_choice.grid(row=1, column=1, padx=10, pady=(10, 20),
                                 sticky="w")

    def obtain_user_input(self):
        """ Function that obtains the user input """
        user_in_dict = {}
        if self.user_input.get() != "":
            if self.choice_checkbox.get() == 1 and self.country_choice.get()\
                    != "":
                self.error_window()
            else:
                user_input = self.user_input.get()
                if self.choice_checkbox.get() == 1 and\
                        self.country_choice.get() == "":
                    remote = "True"
                    user_in_dict = {"user_input": user_input, "remote": remote}
                elif self.choice_checkbox.get() == 0 and\
                        self.country_choice.get() != "":
                    country = self.country_choice.get()
                    user_in_dict = {"user_input": user_input,
                                    "location": country}
                elif self.choice_checkbox.get() == 0 and\
                        self.country_choice.get() == "":
                    user_in_dict = {"user_input": user_input}
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

    def search_button_clicked(self):
        """ Function called when the search button is clicked """
        self.app_instance.populate_results()


class ResultsFrame(ctk.CTkScrollableFrame):
    """ Class that creates the results frame """
    def __init__(self, master, DE_frame, **kwargs):
        super().__init__(master, **kwargs)

        # Top level window
        self.toplevel_window = None

        # Description and Engine Frame
        self.DE_Frame = DE_frame

    def display_results(self, results):
        """ Function that displays the results of the search """
        if results and isinstance(results, list):
            for i, result in enumerate(results):
                wrapped_text = textwrap.fill(result, width=20)
                result_label = ctk.CTkLabel(self, text=wrapped_text)
                result_label.grid(row=i, column=0, padx=(10, 80), pady=10,
                                  sticky="w")

                button = ctk.CTkButton(self, text="Details",
                                       command=lambda label=result_label:
                                       self.show_details(label))
                button.grid(row=i, column=1, padx=(10, 0), pady=10, sticky="e")
        else:
            no_results = ctk.CTkLabel(self, text="No results found")
            no_results.grid(row=0, column=1, padx=(120, 80),
                            pady=10, sticky="ew")

    def show_details(self, label):
        """ Function that displays the details of the search result """
        wrapped = label.cget("text")
        detail = wrapped.replace("\n", " ")
        engine = self.DE_Frame.obtain_dec_details().get("engine")
        job_id = ""

        if engine == "Findwork":
            results = fw.populate()
            for res in results:
                if res.get("role") == detail:
                    job_id = res.get("job_id")
                    break
        elif engine == "Serp":
            results = sp.populate()
            for res in results:
                if res.get("role") == detail:
                    job_id = res.get("job_id")
                    break

        if self.toplevel_window is None or not\
                self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self)
            self.toplevel_window.display_details(detail, engine, job_id)
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
        self.results_frame = ResultsFrame(self, DE_frame=self.DE_Frame)
        self.results_frame.grid(row=0, column=1, sticky="nsew",
                                pady=(150, 10), padx=(2, 3), rowspan=2)

        # User Input Frame
        self.user_input = UserInputFrame(self,
                                         app_instance=self,
                                         results_frame=self.results_frame,
                                         DE_Frame=self.DE_Frame,
                                         height=150)
        self.user_input.grid(row=0, column=1, sticky="new")

    def populate_results(self):
        """ Function that populates the results frame
            with the search results """
        self.results_frame.clear_results()
        search_query = self.user_input.obtain_user_input()
        dec_details = self.DE_Frame.obtain_dec_details()
        dec, engine = dec_details.get("description", "Description"), \
            dec_details.get("engine", "Engine")
        if search_query and dec_details:
            if dec == "Internships":
                pass
            elif dec == "Jobs":
                if engine != "Engine":
                    if engine == "Indeed":
                        pass
                    elif engine == "Findwork":
                        asyncio.run(fw.main(search_query))
                        filtered_results = []
                        results = fw.populate()
                        for res in results:
                            filtered_results.append(
                                res.get("role"))
                        self.results_frame.display_results(
                            filtered_results)
                    elif engine == "Serp":
                        asyncio.run(sp.main(search_query))
                        filtered_res = []
                        res = sp.populate()
                        for r in res:
                            filtered_res.append(r.get("role"))
                        self.results_frame.display_results(filtered_res)
                    else:
                        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
