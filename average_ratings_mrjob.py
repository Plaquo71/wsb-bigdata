from mrjob.job import MRJob
from mrjob.step import MRStep

class MRAverageRating(MRJob):

    def mapper(self, _, line):
        # Split the line into fields
        fields = line.split(',')
        if len(fields) == 4:
            try:
                # Extract movieId and rating
                movie_id = fields[1]
                rating = float(fields[2])
                yield (movie_id, rating)
            except ValueError:
                pass  # Skip lines with parsing errors

    def reducer_init(self):
        self.movie_count = 0
        self.total_rating = 0

    def reducer(self, key, values):
        # Calculate average rating for each movie
        total = 0
        count = 0
        for value in values:
            total += value
            count += 1
        yield key, (total / count)

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer_init=self.reducer_init, reducer=self.reducer)]

if __name__ == '__main__':
    MRAverageRating.run()
