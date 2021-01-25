# Disco

## Project in General

    connection = engine.connect()
    connection.execution_options(autocommit=True).execute(query)

### Tasks

PROD

- [ ] ...

DEV

- [ ] make sure engine (and session?) are created once and imported to different modules, see bc validation
- [ ] i have to implement arg parse and document the entry point with args

- [ ] create tests for db_functions (maybe rename), create package structure like blogpost medium
- [ ] write some kind of back-up files, one with the records in orig format, the other with the trx

- [ ] install dropdowns for the db_functions frontend
- [ ] if I 'update' an artist_country when updating a record, that country is not saved in the db

- [ ] Record label relationships exist, but are not properly displayed in table, because it is many-to-many (check how realpython does, change to one-to-many probably)
- [ ] How will I handle split recods? Multiple labels for a record? I could list them twice

- [ ] clear all input in app.py / create data validations before running add_record function
- [ ] install security check in create_anew()
- [ ] all files: check the many TODOs

- [ ] create ratings table
- [ ] Within update: if a rating is made, then I should write to the ratings table
- [ ] Within update:  also it should be possible ro re-add inactive records! (and to pay for it in credits!)
- [ ] create random button (discogs has one ;-))

- [ ] create proper initial data_ingestion function with df cleaning / assertions (at the moment a messy ipynb)
- [ ] On Updates the old relationship values are not overwritten in many to many relationships (-->Labels), see dev_stuff_2

### Prio 2

- [ ] When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.

### Meta Things

- [ ] Document the CreditTrx Table, which 4 TrxTypes are possible, the logic etc.
- [ ] Document the ingestion approach, that bulk insertion (with sqlachemy core) does only work for copying data into tables, without taking care of the relationships (this is not exacty true, see realpyhton table declaration)
- [ ] Document the connect.ipynb on github
- [ ] Set-up logging

If I use pd.to_sql, then obviously I do not insert in an existing table (?) but create a new, overwrite the schema. I have to check that
It would be better to bulk insert into the table instead of doing like I do now.

## To Do, OLD STUFF

- [ ] Print output summary of load (total loaded, total not loaded, load time etc.)
- [ ] How to regulary update the data without requesting all a new?

## Backlog

- [ ] How to handle albums not found on Spotify in the final version
- [ ] ...

## Notes

- [ ] ...
  