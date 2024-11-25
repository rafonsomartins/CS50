SELECT DISTINCT people.name FROM people, stars WHERE people.id = stars.person_id AND stars.movie_id IN (SELECT DISTINCT id FROM movies, stars WHERE movies.id = stars.movie_id AND stars.person_id = (SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958)) AND people.id != (SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958);