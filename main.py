from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
import pandas as pd

class SayHello(App):
    def build(self):        
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8,0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 5
        self.window.add_widget(Image(source="EnD.jpg"))
        self.welcome = Label(
                       text="Encrypt or Decrypt Texts",
                       font_size=20,
                       size_hint = (0.3,0.2)
                       )
        self.window.add_widget(self.welcome)
        
        self.user = TextInput(
                    multiline=False,                    
                    size_hint = (0.2,0.2),
                    )
        self.window.add_widget(self.user)
        
        self.output = Label(
                      text="",
                      padding_y = (20,20),
                      size_hint = (0.2,0.2),                                           
                      )
        self.window.add_widget(self.output)

        self.button = Button(
                      text="Encrypt",
                      size_hint = (0.3,0.2)
                      )
        self.button.bind(on_press=self.encrypt)
        self.window.add_widget(self.button)

        self.button = Button(
                      text="Decrypt",
                      size_hint = (0.3,0.2)
                      )
        self.button.bind(on_press=self.decrypt)
        self.window.add_widget(self.button)

        self.button = Button(
                      text="Copy",
                      size_hint = (0.3,0.2)
                      )
        self.button.bind(on_press=self.copy)
        self.window.add_widget(self.button)

        self.button = Button(
                      text="Exit",
                      size_hint = (0.3,0.2)                      
                      )
        self.button.bind(on_press=self.exit)
        self.window.add_widget(self.button)

        #add widgets to window        
        
        return self.window

    def copy(self, text):
        Clipboard.copy(self.output.text)


    def decrypt(self, agent):
        encryptionkey = pd.read_csv("encryptionkey.csv",
                                    sep=',', names=['Character', 'Byte'], header=None, skiprows=[0])

        df = pd.DataFrame(data=encryptionkey)

        df['Character'] = df['Character'].astype(str)
        df['Byte'] = df['Byte'].astype(str)

        message = self.user.text
        new_word = ''
        decoded_message = []

        for i in range(0, len(message), 3):
            j = message[i:i + 3]
            index_nb = df[df.eq(j).any(1)]                

            df2 = index_nb['Character'].tolist()        

            s = [str(x) for x in df2]
            decoded_message = decoded_message + s        

        new_word = ''.join(decoded_message)
        self.output.text = new_word

               
    
    def exit(self, agent):
        exit()

    def encrypt(self, agent):
        encryptionkey = pd.read_csv("encryptionkey.csv",
                                    sep=',', names=['Character', 'Byte'], header=None, skiprows=[0])

        df = pd.DataFrame(data=encryptionkey)

        df['Character'] = df['Character'].astype(str)
        df['Byte'] = df['Byte'].astype(str)

        message = self.user.text        

        def split(message):
            return [char for char in message]        

        message_split = split(message)

        def code_message():
            coded_message = ""

            for i in range(len(message_split)):
                j = message_split[i]
                try:
                    coded_char = encryptionkey.loc[encryptionkey['Character'] == j, 'Byte'].iloc[0]

                except:
                    print('unrecognized character')
                    coded_char = '@@@'

                coded_message = coded_message + coded_char
            return coded_message

        encoded = code_message()
        self.output.text = encoded
        


if __name__ == "__main__":
    SayHello().run()