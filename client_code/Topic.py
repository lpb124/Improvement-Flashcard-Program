import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .Set import Set
from .Statistics import Statistics

class Topic:
    def __init__(self,name, reconstruct = False, id = -1):
        self.name = name
        self.sets = {}
        self.id = id
        if not reconstruct:
          self.create_row_db()
        
    def selection_sort(self):
      #Selection sort to sort the set dictionary scores from highest to lowest
      #Converts the set dictionary to list
      setlist = list(self.sets.values())
      #iterates through each element in the setlist
      for i in range(len(setlist)):
        maxindex = i 
        for j in range(i+1, len(setlist)):
          #Compares the highest score of the currently checked set with the selected assumed maximum
          if setlist[j].statistics.highest_score > setlist[maxindex].statistics.highest_score:
            #Updates the maximum if a larger score is found
            maxindex = j

        #Sways the maximum element with the first element of the unsorted array
        setlist[i], setlist[maxindex] = setlist[maxindex], setlist[i]
        #Returns the sorted array
        return setlist

    #Example in Topic class
    def create_set(self, set_name):
        # create the set 
        # make set name lower case 
        set_name_lower = set_name.lower()
        if (self.sets.get(set_name_lower)== None):
            # make all set names 
            set = Set(set_name_lower)
            self.sets[set_name_lower] = set
            # Saving to database
            topic_row = app_tables.topic.get(ID = self.id)
            set_row = app_tables.set.get(ID = set.id)
            if topic_row['Sets'] == None:
              topic_row['Sets'] = [set_row]
            else:
              topic_row['Sets'] += [set_row]
        else:
          raise ValueError(f"set with name {set_name_lower} already exists.")

    def get_set(self,set_name):
      #Method for retrieving a specified set
        set_name = set_name.lower()
        #Converts name to lowercase to make sure no sets are missing
        self.name = set_name
        #Retrieves specified set the sets dictionary and specifies as the target set
        target_set = self.sets.get(set_name)
        #Error handling if the target does not exist 
        if (target_set == None):
            raise ValueError(f"set with name {set_name} doesnt exist.")
          #Returns the targeted set if it does exist
        else:
            return target_set
    
    def remove_set(self,set_name):
      #Method to delete specifed set
        set_name = set_name.lower()
      #Converts name to lowercase to make sure no sets are missing
        try:
            del self.sets[set_name]
            #Tries to delete specified set from the sets dictionary
            return True
        except KeyError: 
            #Error handling if the set does not exist
            return False

    def create_row_db(self):
      #  method for creating new row in database 
      #gets the row in the id manager table containing the latest unique id number for each object
        id_row = app_tables.id_manager_.get(Key = 'ID_manager')
        current_id = id_row['Topic']
        self.id = current_id
        app_tables.topic.add_row(Name = self.name, ID = current_id)
        new_id = current_id + 1
        id_row.update(Topic = new_id)
