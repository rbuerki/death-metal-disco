# Disco

## Project in General

...

### Tasks

PROD

- ...

DEV - FRONTEND

- [x] STATS: get stats directy from DB (halfway done, still some issues there ...)

- [ ] CRUD: Refactor completely (also check None, nan etc )
- [ ] CRUD UPDATE: filter by ID alternatively
- [ ] CRUD UPDATE: either dropdown for title or contains filtering
- [ ] CRUD UPDATE BUG (probably): if I update the title or artist, the record is not found ...
- [ ] CRUD: clear all input in crud_app.py ... see [here](https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941)
- [ ] RECS: for every displayed record have a direct link to the update page, passing record and artist - if possible ...
  
  ```python  
    from src import SessionState
    st_session_sate = SessionState.get(run_id=0)
    st_session_state.run_id += 1
  ```

DEV - MODEL / DB_FUNCTIONS

- [ ] BUG: On Updates the old relationship values are not overwritten in many to many relationships: possible solution: you have to do this in the update formula "for l in labels_existing if l not in labels_new delete relationship ..."
- [ ] test delete cascade on other relations, without the all maybe ... cannot be that it works that way ... ONLY DECLARE Relationships IN ONE PLACE!

- [ ] implement relationships for ratings table:
  - ... in db_declaration
  - ... in db_functions add_ / udpate_ and export
  - ... frontend crud (add, update)

- [ ] Think about that: When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.
- [ ] db_functions: check the TODOs (actually you should refactor the whole thing)
- [ ] Within update: it should also be possible ro re-add inactive records! (and to pay for it in credits!)

DEV - MISC

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

- _Deletion of faulty DB entries_: First, using the frontend you can only deactivate records. When you do this the relations are not touched and all child entries remain unchanged. If there are faulty entries in the DB that have to be deleted, please note, that deletion cascades are only implemented on the `Record` side of relationships. So, if you delete a record the artist or trx relations for that instance are deleted too. For the other model classes there are no deletion cascades as I don't want records to be deleted if the related label has to be deleted for example.

- ...
  