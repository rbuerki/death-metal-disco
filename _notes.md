# Disco

## Project in General

...

### Tasks

PROD

- [ ] ...

DEV - PRIO 1

- [ ] CRUD UPDATE BUG (probably): if I update the title or artist, the record is not found for insertion ... that's gonna be hard - maybe set record_id aside then.
- [ ] CRUD: Artist Country often (always?) taken from previous record (updates) / sometimes Label (if the same artist, at least, see Tomb Mold)
- [ ] STATS: % of total per Rating
- [ ] RATINGS app

DEV - PROBLEMS NOT SOLVED

- [ ] RECS: for every displayed record have a direct link to the update page, passing record and artist - if possible ...
- [ ] CRUD: clear all input in crud_app.py ... see [here](https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941)
- [ ] CRUD: Purchase - fill in artist country if artist exists

  ```python  
    from src import SessionState
    st_session_sate = SessionState.get(run_id=0)
    st_session_state.run_id += 1
  ```

DEV - PRIO 2

- [x] STATS: get stats directy from DB (halfway done, still some issues there ...)

- [ ] implement relationships for ratings table:
  - ... in db_declaration
  - ... in db_functions add_ / udpate_ and export
  - ... frontend crud (add, update)

- [ ] Think about that: When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.
- [ ] Within update: it should also be possible ro re-add inactive records (and to pay for it in credits)

DEV - MAYBE

- [ ] integrate export in reset function, true by default, can be deactivated
- [ ] implement arg parse for main and document the entry point with args
- [ ] create tests for db_functions (maybe rename), create package structure like blogpost medium

### Meta Things

- [ ] Document the CreditTrx Table, which 4 TrxTypes are possible, the logic etc.
- [ ] Document the ingestion approach, that bulk insertion (with sqlachemy core) does only work for copying data into tables, without taking care of the relationships (this is not exacty true, see realpyhton table declaration)
- [ ] Document the connect.ipynb on github

## To Do, OLD STUFF

- [ ] Print output summary of load (total loaded, total not loaded, load time etc.)
- [ ] How to regulary update the data without requesting all a new?

## Backlog

- [ ] How to handle albums not found on Spotify in the final version
- [ ] ...

## Notes

- _Session Handling_: A scoped Session object is created in the main app. The scoping is necessary to make it threadsafe. Because the main app is rerun at every change, it is also cached, see [here](https://docs.streamlit.io/en/latest/caching.html#example-1-pass-a-database-connection-around) for more information. To have a separate session for each thread a session is then instantiated in the individual apps. Some links with infos on this are in the docstring for the `create_scoped_session` function, see `db_connect.py`.

- _Deletion of faulty DB entries_: First, using the frontend you can only deactivate records. When you do this the relations are not touched and all child entries remain unchanged. If there are faulty entries in the DB that have to be deleted, please note, that deletion cascades are only implemented on the `Record` side of relationships for the many-to-one relations (CreditTrx, Ratings). This means pretty much stuff is untouched even if records are gone, see DEV notebook for the problematic. I have not found if there is a better solution. Adding delete cascades on many-to-many or one-to-many relationships has caused havoc in my DB (e.g. delete one DM record and the whole DM genre is gone ...).

- ...
  