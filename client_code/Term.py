import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from CardFace import CardFace

class Term(CardFace): #inheritance, the term class is inherting from CardFace class
    # default param to make image optional 
  #id set to -1 by default because it gets dynamically filled based on the current unique id number of that class type (when creating a new object )- 
  #but it when reconstructing an object from table it gets entered in constructor 
    def __init__(self, content, image_url =" ", id = -1, reconstruct = False): # RECONSTRUCT ID ADDED
        super().__init__(content,id)
        self.image_url = image_url # set image if there is an image 
        if not reconstruct:# THIS ADDS TO DB IF OBJECT NOT BEING RECONSTRUCTED FROM DATABASE
          self.create_row_db()
        

    #Overiding display of cardface
    def display(self):
        return self.content, self.image_url # polymorphism used, the display method from term and def return different things 
    
 # overiding cardface method
    def edit_content(self, new_content):
        self.content = new_content 
        self.save_content_to_db()
 # methods specific to term subclass
  # getter method 
    def get_image_url(self):
        return self.image_url
    #method to edit the image url 
    def edit_image_url(self, new_image_url):
        self.image_url = new_image_url
        self.save_image_to_db() # save to db 

    def create_row_db(self):
       # method for creating new row in database 
      # gets the row in the id manager table containing the latest unique id number for each object
      # set id 
        id_row = app_tables.id_manager_.get(Key = 'ID_manager')
        current_id = id_row['Term']
        self.id = current_id
      
        if self.image_url == " ": #if object has no image -then dont save image to row 
          app_tables.term.add_row(Content = self.content, ID = current_id)
  
        else:# if object has image save image to row
          app_tables.term.add_row(Content = self.content, ID= current_id, Image = self.image_url)
        #increment id and save new incremented id 
        new_id = current_id + 1 
        id_row.update(Term = new_id)

    def save_content_to_db(self):
      # saving content to db - tries (works if there is a row created witht id, throws value error if there isnt )
      try:
        row = app_tables.term.get(ID = self.id)
        row.update(Content = self.content)
      except:
        raise ValueError(f"No such row in table")
    def save_image_to_db(self):
      # saving content to db - tries (works if there is a row created witht id, throws value error if there isnt )
      try:
        row = app_tables.term.get(ID = self.id)
        row.update(Image = self.image_url)
      except:
        raise ValueError(f"No such row in table")