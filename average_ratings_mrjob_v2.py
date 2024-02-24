	from mrjob.job import MRJob
	from mrjob.step import MRStep
	
	class MoviesTittles(MRJob):
	
	    def configure_args(self):
	        super(MoviesTittles, self).configure_args()
	        self.add_file_arg('--movies', help='Path to the movies.csv')
	
	    def steps(self):
	        return [
	            MRStep(
	                mapper=self.mapper_get_ratings,
	                reducer=self.reducer_get_average_rating
	            ),
	            MRStep(
	                mapper=self.mapper_get_titles,
	                reducer=self.reducer_output
	            )
	        ]
	
	    def mapper_get_ratings(self, _, line):
	        fields = line.split(',')
	        if len(fields) == 4 and fields[2] != 'rating':
	            movie_id = fields[1]
	            rating = float(fields[2])
	            yield movie_id, (rating, 1)
	
	    def reducer_get_average_rating(self, movie_id, values):
	        total_rating = 0
	        total_count = 0
	        for rating, count in values:
	            total_rating += rating
	            total_count += count
	        yield movie_id, (total_rating / total_count, total_count)
	
	    def mapper_get_titles(self, movie_id, rating_data):
	        with open(self.options.movies, 'r', encoding='utf-8') as f:
	            for line in f:
	                if not line.startswith('movieId'):
	                    fields = line.split(',')
	                    if fields[0] == movie_id:
	                        title = fields[1]
	                        yield None, (title, rating_data[0])
	
	    def reducer_output(self, _, title_rating_pairs):
	        for title, rating in title_rating_pairs:
	            yield title, rating
	
	if __name__ == '__main__':
	    MoviesTittles s.run()
