import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import numpy as np # Importing numpy to statistics class

class Statistics:
    def __init__(self, reconstruct = False, id = -1):
        self.total_sessions = 0 
        self.total_correct = 0
        self.total_incorrect = 0
        self.average_confidence = 0
        self.average_score = 0
        self.highest_score = 0
        self.lowest_score = 1000000000000
        self.current_score = 0
        self.current_high_streak = 0
        self.longest_streak = 0
        self.score_history = []
        self.confidence_history = [] # Confidence_history is an array
        self.id = id
        if reconstruct is False:
          self.create_row_db()

    def sorted_score_history(self):
      # Check if confidence_history is not empty and has at least one session
      if self.confidence_history and len(self.confidence_history[0]) > 0:
          total_entries = len(self.confidence_history[0])  # Number of entries in the first session
  
          # Calculate percentage for each score based on the number of entries in the first session
          indexed_scores = [(index, 100 * score / total_entries) for index, score in enumerate(self.score_history)]
      else:
          return ["No confidence data available or empty session"]  # Return message if no data
  
      # Bubble sort algorithm to sort the scores in descending order
      n = len(indexed_scores)
      for i in range(n):
          swapped = False
          for j in range(0, n - i - 1):
              if indexed_scores[j][1] < indexed_scores[j + 1][1]:
                  indexed_scores[j], indexed_scores[j + 1] = indexed_scores[j + 1], indexed_scores[j]
                  swapped = True
          if not swapped:
              break
  
      # Format the sorted scores with their original indices for output
      sorted_scores = [f"Score: {score:.2f}%, Original Index: {index + 1}" for index, score in indexed_scores]
      return sorted_scores

  
    def mean(self,values):
      return sum(values) / len(values) if values else 0
    def mean_2d(self,values):
      total = 0
      count = 0
      for sublist in values:
          for item in sublist:
              if isinstance(item, (int, float)):  # Checking if the item is a number
                  total += item
                  count += 1
              else:
                  raise ValueError("All elements must be int or float to calculate mean.")
      return total / count if count else 0

  
    def update(self,session):
        self.current_score = session.get_score()
        self.current_high_streak = session.get_longest_streak()
        
        self.total_sessions += 1 
        self.total_correct += session.get_correct()
        self.total_incorrect += session.get_incorrect()
 # histories
        self.score_history.append(self.current_score)
        #self.score_history.append(session.get_score())
        self.confidence_history.append(session.get_confidence_ratings()) # Appending Condifence ratings to store intire history
        # self.session_history.append(session)
        
        #Average statistics

        self.average_confidence = np.mean(self.confidence_history) # gets confidence history and averages it
        self.average_score = np.mean(self.score_history) # gets score history and averages it


        # Highest number stats
        if (self.current_score > self.highest_score):
            self.highest_score = self.current_score
        if (self.current_high_streak > self.longest_streak):
            self.longest_streak = self.current_high_streak



        # lowest number stats
        if (self.current_score < self.lowest_score):
            self.lowest_score = self.current_score
        self.update_db()
    #Getters
    def get_total_sessions(self):
        return self.total_sessions
    def get_total_correct(self):
        return self.total_correct
    def get_total_incorrect(self):
        return self.total_incorrect
    def get_average_confidence(self):
        return self.average_confidence
    def get_average_score(self):
        return self.average_score
    def get_highest_score(self):
        return self.highest_score
    def get_lowest_score(self):
        return self.lowest_score
    def get_current_score(self):
        return self.current_score
    def get_current_high_streak(self):
        return self.current_high_streak
    def get_longest_streak(self):
        return self.longest_streak
    def get_score_history(self):
        return self.score_history
    def get_confidence_history(self):
        return self.confidence_history
#Setters
    def set_total_sessions(self, total_sessions):
        self.total_sessions = total_sessions

    def set_total_correct(self, total_correct):
        self.total_correct = total_correct

    def set_total_incorrect(self, total_incorrect):
        self.total_incorrect = total_incorrect

    def set_average_confidence(self, average_confidence):
        self.average_confidence = average_confidence

    def set_average_score(self, average_score):
        self.average_score = average_score

    def set_highest_score(self, highest_score):
        self.highest_score = highest_score

    def set_lowest_score(self, lowest_score):
        self.lowest_score = lowest_score

    def set_current_score(self, current_score):
        self.current_score = current_score

    def set_current_high_streak(self, current_high_streak):
        self.current_high_streak = current_high_streak

    def set_longest_streak(self, longest_streak):
        self.longest_streak = longest_streak

    def set_score_history(self, score_history):
        self.score_history = score_history

    def set_confidence_history(self, confidence_history):
        self.confidence_history = confidence_history

    def create_row_db(self):
      id_row = app_tables.id_manager_.get(Key = 'ID_manager')
      cur_id = id_row['Statistics'] #get current statistic id
      self.id = cur_id # set stat id

      # create the row
      app_tables.statistics.add_row(
        ID = cur_id, Longest_streak = self.longest_streak,
        Average_confidence= self.average_confidence,Total_correct=self.total_correct,
        Average_score=self.average_score, Latest_longest_streak= self.current_high_streak,
        Score_history= self.score_history, Highest_score= self.highest_score,Total_incorrect = self.total_incorrect,
        Confidence_history= self.confidence_history, Lowest_score= self.lowest_score,Total_sessions= self.total_sessions,
        Current_score=self.current_score)

      # update id manager
      new_id = cur_id+1
      id_row.update(Statistics=new_id)

    def update_db(self):
     
      # get correct row
      stat_row = app_tables.statistics.get(ID = self.id)

     
      stat_row.update(Longest_streak= self.longest_streak) #1
      stat_row.update(Average_confidence= self.average_confidence)#2
      stat_row.update(Total_incorrect= self.total_incorrect) #3
      stat_row.update(Total_correct = self.total_correct) #4
      stat_row.update(Average_score=self.average_score) #5
      stat_row.update(Latest_longest_streak= self.current_high_streak) #6
      stat_row.update(Score_history= self.score_history) #7
      stat_row.update(Highest_score= self.highest_score) #8
      stat_row.update(Confidence_history= self.confidence_history)# 9
      stat_row.update(Lowest_score= self.lowest_score)#10
      stat_row.update(Total_sessions=self.total_sessions) #11
      stat_row.update(Current_score=self.current_score) #12



       
    
    

        