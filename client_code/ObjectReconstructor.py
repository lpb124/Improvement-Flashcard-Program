import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .User import User
from .Topic import Topic
from .Flashcard import Flashcard
from .Set import Set
from .Statistics import Statistics
from .Term import Term
from .Definition import Definition


class ObjectReconstructor:
  # on initialization of the program - all objects are reinitialized from the rows in the database- 
  # the structure of the classes are all encapsulated within each other that is User contains a Topic, topic contains sets... so on that they cascaded down 
  # only method that needs to be called is reconstruct user and the rest get called in its wake 
    def __init__(self):
      # constructor doesnt do anything - nothing needs to be set
      pass 
    # notice that all reconstruct methods initialize the object with its appropriate id, and reconstruct set to true 
  # reconstruct set to true ensures that you arent duplicating rows each time you reconstruct an object 
  # notice that each reconstruct object gets fed in a row that they are to reconstruct based on the contents of that rwo 
    def reconstruct_def(self, row): # from def row reconstruct a def object 
      return Definition(row['Content'],row['ID'], reconstruct = True)

    def reconstruct_term(self, row): #from term row reconstruct term object 
      image = row['Image'] # extract image column content 
    
      if image is not None:# if image is set return an object with an image url 
        return Term(row['Content'], id = row["ID"], image_url = image, reconstruct = True)
      return Term(row['Content'],id =  row["ID"], reconstruct = True) # if image is none return object without image 
      
    

    def reconstruct_flashcard(self,row):
      # exctract the front row and the back row from their respective tables 
      definition_row = row['Back'] 
      term_row = row['Front']
      ID = row['ID'] # get the id 
      definition = self.reconstruct_def(definition_row)# reconstruct the definition object by calling the reconstruct def row 
      term = self.reconstruct_term(term_row)# same as above 
      return Flashcard(term, definition, id = ID, reconstruct = True) # init Flashcard and return it 

    def reconstruct_statistic(self,row):
  #construct statistic - setting reconstruct as true so it doesnt create new db row
      id = row["ID"]
      statistic = Statistics(reconstruct = True, id = id) # create a statistic object 
      # set all its attributes 
      statistic.id = id
      statistic.set_average_confidence(row["Average_confidence"]) #1
      statistic.set_average_score(row["Average_score"])#2
      statistic.set_confidence_history(row["Confidence_history"])#3
      statistic.set_current_high_streak(row["Latest_longest_streak"])#4
      statistic.set_current_score(row["Current_score"]) #5
      statistic.set_highest_score(row["Highest_score"]) #6
      statistic.set_longest_streak(row["Longest_streak"])#7
      statistic.set_lowest_score(row["Lowest_score"]) #8
      statistic.set_score_history(row["Score_history"])#9
      statistic.set_total_correct(row["Total_correct"])#10
      statistic.set_total_incorrect(row["Total_incorrect"]) #11
      statistic.set_total_sessions(row["Total_sessions"])#12
      return statistic # return statistic 

    def reconstruct_set(self,row):
      # extract information needed from row 
      flashcard_rows = row['Flashcards']
      stat_row = row['Statistics']
      name = row['Name']
      ID = row['ID']

      # reconstruct stat object 
      stat = self.reconstruct_statistic(stat_row)
      set = Set(name = name, id = ID, reconstruct = True) # init set 
    
    
      set.set_statistics(stat) # set the stat object 
      # if there are flashcard rows 
      if flashcard_rows is not None: # iterate through each flashcard row and call reconstruct flashcard on each 
        for flashcard_row in flashcard_rows:
          flashcard = self.reconstruct_flashcard(flashcard_row)
          set.flashcards.insert_tail(flashcard) # add each flashcard to flashcard linked list in set 
      return set # return set 
        
    def reconstruct_topic(self,row):
      # Extract all needed info from row 
      set_rows = row['Sets']
      name = row['Name']
      ID = row['ID']
      # init topic 
      topic = Topic(name = name, id = ID, reconstruct = True)
      if set_rows == None:
       pass
      else: # if set rows are not empty iterate through each set row in the set rows , call resconstruct set on them and then add them to the sets dictionary
       for set_row in set_rows:
        set = self.reconstruct_set(set_row)
        topic.sets[set.name] = set
      return topic # return reconstructed topic 
      
        
    def reconstruct_user(self,row):
      # Extract id from user row 
      ID = row['ID']
      user = User(id = ID, reconstruct = True) # init user with id and reconstruct true so it doesnt create new row 
      topic_rows = row['Topics'] # extract topic rows 
      for topic_row in topic_rows: # for each topic row in topic rows, reconstruct topic and save topic to topics dictionary 
        topic = self.reconstruct_topic(topic_row)
        user.topics[topic.name] = topic
      return user # return reconstructed user object 