# Disco

## Project in General

...

### Tasks

PROD

- [ ] ...

DEV - MODEL

- [ ] Export data to csv with proper function

- [ ] add datachecks in db model
- [ ] rename acitve column to is_active
- [ ] create ArtistRecordLink, adapt relations
- [ ] create ratings table
- [ ] - [ ] Think about that: When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.

- [ ] Adapt Export to handle m-t-m artists
- [ ] Import data with proper function

``` python
    string = "Witch Vomit; Coffins"
    l = string.split("/")
    for a in l:
        print(a.strip())
```

- [ ] Within update: if a rating is made, then I should write to the ratings table
- [ ] Within update:  also it should be possible ro re-add inactive records! (and to pay for it in credits!)
- [ ] On Updates the old relationship values are not overwritten in many to many relationships (-->Labels), see dev_stuff_2
- [ ] ... they are also not deleted, because I have not set a delete (cascade) option in the db model, probably ...

DEV - FRONTEND

- [ ] clear all input in crud_app.py ... see [here](https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941)
- [ ] install dropdowns for the db_functions frontend (?)
- [ ] create random button (discogs has one ;-))

- [ ] i have to implement arg parse and document the entry point with args
- [ ] create tests for db_functions (maybe rename), create package structure like blogpost medium
- [ ] write some kind of back-up files, one with the records in orig format, the other with the trx

- [ ] create data validations before running add_record function ...
- [ ] install security check in create_anew()
- [ ] all files: check the many TODOs

### Prio 2

- [ ] - [ ] create proper initial data_ingestion function with df cleaning / assertions (at the moment a messy ipynb)

### Meta Things

- [ ] Document the CreditTrx Table, which 4 TrxTypes are possible, the logic etc.
- [ ] Document the ingestion approach, that bulk insertion (with sqlachemy core) does only work for copying data into tables, without taking care of the relationships (this is not exacty true, see realpyhton table declaration)
- [ ] Document the connect.ipynb on github


If I use pd.to_sql, then obviously I do not insert in an existing table (?) but create a new, overwrite the schema. I have to check that
It would be better to bulk insert into the table instead of doing like I do now.

## To Do, OLD STUFF

- [ ] Print output summary of load (total loaded, total not loaded, load time etc.)
- [ ] How to regulary update the data without requesting all a new?

## Backlog

- [ ] How to handle albums not found on Spotify in the final version
- [ ] ...

## Notes

- _Session Handling_: A scoped Session object is created in the main app. The scoping is necessary to make it threadsafe. Because the main app is rerun at every change, it is also cached, see [here](https://docs.streamlit.io/en/latest/caching.html#example-1-pass-a-database-connection-around) for more information. To have a separate session for each thread a session is then instantiated in the individual apps. Some links with infos on this are in the docstring for the `create_scoped_session` function, see `db_connect.py`.
- ...
  