import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from CardFace import CardFace
# inheriting from superclass cardface
class Definition(CardFace): 
  #id set to -1 by default because it gets dynamically filled based on the current unique id number of that class type (when creating a new object )- 
  #but it when reconstructing an object from table it gets entered in constructor 
    def __init__(self,content,id = -1, reconstruct = False):
        super().__init__(content,id) #Explicitly call superclass constructor 
        #Checking if we are reconstructing an object from the database or creating a new one
        if not reconstruct:
          self.create_row_db() # if new one create a row in the db 
          


# OVeride from superclass method 
  #Overriding method from superclass 
    def display(self):
        return self.content #Only content needs to be returned as the back of the flashcard does not need an image.
    #Sets content to new content and then saves new content to database
    def edit_content(self, new_content):
        self.content = new_content
        self.save_content_to_db()
      

    def create_row_db(self):
      # method for creating new row in database 
    
        id_row = app_tables.id_manager_.get(Key = 'ID_manager') # gets the row in the id manager table containing the latest unique id number for each object
        current_id = id_row['Definition'] # get the current id number for definition object
        self.id = current_id # set id 
      
        app_tables.definition.add_row(Content = self.content, ID = current_id) # add row containing definition attributes to definition table 

        #increment id number and save it back to the row
        new_id = current_id + 1
        id_row.update(Definition = new_id)

    def save_content_to_db(self):
      # method to save new content to databse 
      #Tries to change content of a row based on its updated value (if no row with that id raises exception)
      try:
        row = app_tables.definition.get(ID = self.id) # get row 
        row.update(Content = self.content) # save content 
      except:
        raise ValueError(f"No such row in table")
    