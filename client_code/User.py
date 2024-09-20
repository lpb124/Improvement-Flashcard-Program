import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from Topic import Topic
class User:

    def __init__(self, id = -1, reconstruct = False):
        self.topics = {}
        self.id = id
        if not reconstruct:
         self.create_row_db()

   #Example in User class
    def create_topic(self,topic_name):
        topic_name = topic_name.lower() #Setting topic name to lowercase for convention incase another topic with the same name but uppercase is missed

        if (self.topics.get(topic_name)== None): #Checks if there is another topic with the same name
            # make all set names 
            topic = Topic(topic_name)
            self.topics[topic_name] = topic
          # Saving to database
            user_row = app_tables.user.get(ID = self.id)
            topic_row = app_tables.topic.get(ID = topic.id)
            if user_row['Topics'] == None: # Checks if there are any rows in the topic database
              user_row['Topics'] = [topic_row] 
            else:
              user_row['Topics'] += [topic_row]#If there is a new topic row is added next to the already added topics
        else:
            raise anvil.alert(f"Topic with name {topic_name} already exists.")# If there is already a topic with the same name as the one entered, a error message is returned to let the user know

    def create_row_db(self):
        id_row = app_tables.id_manager_.get(Key = 'ID_manager')
        current_id = id_row['User']
        self.id = current_id
        app_tables.user.add_row(ID = current_id )
        new_id = current_id + 1
        # app_tables.user.add_row(ID = current_id + 1)
        # new_id = current_id + 1
        id_row.update(User = new_id)

    def get_topics(self):
      return self.topics


