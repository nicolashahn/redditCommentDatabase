# nuke the database of any reddit material
use iac;
delete from posts where dataset_id = 6;
delete from authors where dataset_id = 6;
delete from basic_markup where dataset_id = 6;
delete from texts where dataset_id = 6;
delete from discussions where dataset_id = 6;
delete from subreddits where dataset_id = 6;
