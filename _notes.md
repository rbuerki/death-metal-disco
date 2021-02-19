# Disco

## Project in General

...

### Tasks

PROD

- ...

DEV - FRONTEND

- [ ] STATS: get stats directy from DB

- [ ] CRUD: Refactor completely
- [ ] CRUD: clear all input in crud_app.py ... see [here](https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941)
  
```python  
  from src import SessionState
  st_session_sate = SessionState.get(run_id=0)
  st_session_state.run_id += 1
```

- [ ] RECS: for every displayed record have a direct link to the update page, passing record and artist - if possible ...

DEV - MODEL

- [ ] BUG: On Updates the old relationship values are not overwritten in many to many relationships: possible solution: delete record first with cascade

- [ ] implement relationships for ratings table:
  - ... in db_declaration
  - ... in db_functions add_ / udpate_ and export
  - ... frontend crud (add, update)

- [ ] Within update: it should also be possible ro re-add inactive records! (and to pay for it in credits!)
- [ ] Think about that: When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.
- [ ] db_functions: check the TODOs (actually you should refactor the whole thing)

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
- ...
  