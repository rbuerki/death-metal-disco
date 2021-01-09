# Disco

## Project in General

    connection = engine.connect()
    connection.execution_options(autocommit=True).execute(query)

### Tasks

- [ ] WARNING: make sure dev and app.py (!!!) works on a dev DB --> it will not yet
- [ ] create remove_record function frontend
- [ ] create update_record function (no trx is created), but if a rating is made, then I sould write to the ratings table
- [ ] ... then It has to be possible ro re-add inactive records! (and to pay for it in credits!)
- [ ] make sure engine (and session?) are created once and imported to different modules
- [ ] clear all input in app.py / create data validations before running add_record function
- [ ] install security check in create_anew()
- [ ] insert_record, see TODOs

- [ ] write some kind of back-up files, one with the records in orig format, the other with the trx
- [ ] create proper initial data_ingestion function with df cleaning / assertions

- [ ] create ratings table
- [ ] create random button (discogs has one ;-))

### Prio 2

- [ ] When I set a record to inactive, the artist / label / genre etc. are not touched, set to inactive.
- [ ] How will I handle split recods? Multiple labels for a record? I could list them twice (with credit worth of 0.5)

### Meta Things

- [ ] Document the CreditTrx Table, which 4 TrxTypes are possible, the logic etc.
- [ ] Document the ingestion approach, that bulk insertion (with sqlachemy core) does only work for copying data into tables, without taking care of the relationships (this is not exacty true, see realpyhton table declaration)
- [ ] Document the connect.ipynb on github
- [ ] Set-up logging

If I use pd.to_sql, then obviously I do not insert in an existing table (?) but create a new, overwrite the schema. I have to check that
It would be better to bulk insert into the table instead of doing like I do now.

### Prio 2

- [ ] Artist country is set to all NULL yet

## To Do, OLD STUFF

- [ ] Print output summary of load (total loaded, total not loaded, load time etc.)
- [ ] How to regulary update the data without requesting all a new?

## Backlog

- [ ] How to handle albums not found on Spotify in the final version
- [ ] ...

## Notes

- [ ] ...
  