SELECT(SELECT SUM(energy) FROM (SELECT energy FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Post Malone')))/(SELECT COUNT(*) FROM (SELECT energy FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Post Malone')));