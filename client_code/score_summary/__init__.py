from ._anvil_designer import score_summaryTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class score_summary(score_summaryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = properties['user']
    self.set_name = properties['set_name']
    self.topic_name = properties['topic_name']
    self.statistics = self.user.get_topics()[self.topic_name].get_set(self.set_name).get_statistics()
    if self.statistics.get_score_history() == []:
      self.content_panel.visible = False
      self.label_3.visible = True
    self.confidence_label.text = self.statistics.get_average_confidence()
    self.label_6.text = str(self.statistics.get_average_score())+ " %"
    #self.sorted_label=self.statistics.sorted_score_history()
    #print(self.statistics.get_current_high_streak())
    #plot graph
    self.sorted_label.text = self.statistics.sorted_score_history()

    if self.statistics.confidence_history and len(self.statistics.confidence_history[0]) > 0:
        total_entries = len(self.statistics.confidence_history[0])  # Total entries in the first session

        # Fetch score history from the statistics object
        score_history = self.statistics.get_score_history()

        # Convert each score to a percentage of the total entries
        percentages = [100 * score / total_entries for score in score_history]
        session_numbers = list(range(1, len(percentages) + 1))

        # Update plot data with percentages
        self.plot_1.data = go.Scatter(x=session_numbers, y=percentages, mode='lines+markers')
        self.plot_1.layout.title = "Score History as Percentages Over Time"
        self.plot_1.layout.xaxis.title = "Session Number"
        self.plot_1.layout.yaxis.title = "Percentage of Total Entries (%)"
    #plot 2

    confidence_history = self.statistics.get_confidence_history()  # Fetch the data
    averages = [sum(session) / len(session) if session else 0 for session in confidence_history]  # Calculate averages
    session_numbers = list(range(1, len(averages) + 1))  # Generate session numbers

    # Plotting the results
    self.plot_2.data = go.Scatter(x=session_numbers, y=averages, mode='lines+markers')
    self.plot_2.layout.title = "Average Confidence Ratings Over All Sessions"
    self.plot_2.layout.xaxis.title = "Session Number"
    self.plot_2.layout.yaxis.title = "Average Confidence Rating"
    self.label_4.text = self.statistics.get_longest_streak()



  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def primary_color_1_click(self, **event_args):
    open_form('hub')
    """This method is called when the button is clicked"""
    pass
