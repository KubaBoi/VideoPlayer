
from Cheese.cheeseRepository import CheeseRepository

#@repository videos;
#@dbscheme (id, name, show_name, series, episode, description);
#@dbmodel Video;
class VideosRepository(CheeseRepository):
	
	#@query "select * from videos where show_name=:showName order by series, name ASC;";
	#@return array;
	@staticmethod
	def findByShowAndOrderByName(showName):
		return CheeseRepository.query(showName=showName)

	#@query "select * from videos order by episode, name ASC;";
	#@return array;
	@staticmethod
	def findAllOrderByEpisodeAndName():
		return CheeseRepository.query()

	#@query "select * from videos where show_name=:showName and series=:series and episode=:episode;";
	#@return one;
	@staticmethod
	def findByShowAndSeriesAndEpisode(showName, series, episode):
		return CheeseRepository.query(showName=showName, series=series, episode=episode)

