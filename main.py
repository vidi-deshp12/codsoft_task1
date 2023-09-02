from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivymd.uix.list import MDList, OneLineAvatarIconListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty,ObjectProperty

class DialogContent(MDBoxLayout):
    pass

class MainApp(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dialog=None

    task_input_text = StringProperty("")
    
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                tasks = f.read().splitlines()
                for task in reversed(tasks):
                    new_task = Factory.MyItem(text=task)
                    self.root.ids.task_list.add_widget(new_task)
        except FileNotFoundError:
            pass

    def build(self):
        self.theme_cls.primary_palette="Teal"
        self.load_tasks()
        self.task_list = self.root.ids.task_list  # Get a reference to the task list
        return self.root

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for item in self.root.ids.task_list.children:
                f.write(f"{item.text}\n")
        
    def add_task(self):
        task_text = self.root.ids.task_input.text.strip()
        if task_text:
            new_task = Factory.MyItem(text=task_text)
            self.root.ids.task_list.add_widget(new_task)
            self.root.ids.task_input.text = ""
            self.save_tasks()

    def show_dialog(self):
        if not self.dialog:
            self.dialog=MDDialog(
                title="Warning",
                text="Delete selected items?",
                type="custom",
                content_cls=DialogContent()
            )
        self.dialog.open()


    def close_dialog(self,obj):
        self.dialog.dismiss()


    def delete_tasks(self):
        tasks_to_delete=[]
        for item in list(self.root.ids.task_list.children):
            if isinstance(item,Factory.MyItem):
                if item.ids.checkbox.active:
                    tasks_to_delete.append(item)
        for task in tasks_to_delete:
            self.root.ids.task_list.remove_widget(task)
        self.save_tasks()











    '''def add_task(self):
        task_text = self.root.ids.task_input.text  # Get text from MDTextField
        if task_text.strip():  # Make sure the text is not empty or just spaces
            new_task=Builder.load_string('MyItem:')
            self.root.ids.task_list.add_widget(new_task)

            #task_item = MyItem(text=task_text)
            #self.task_list.add_widget(task_item)

            #task_item = MyItem(text=task_text)  # Create a new list item
            #self.root.ids.task_list.add_widget(task_item)  # Add the item to the list
            
            self.root.ids.task_input.text = ""  #clear the text field
'''
   
MainApp().run()