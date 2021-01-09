# Disco

## Project in General

    connection = engine.connect()
    connection.execution_options(autocommit=True).execute(query)

### Tasks

- [ ] WARNING: make sure dev and app.py (!!!) works on a dev DB

- [ ] make sure engine (and session?) are created once and imported to different modules
- [ ] clear all in app.py
- [ ] install security check in create_anew()
- [ ] insert_record, see TODOs
- [ ] insert_record: ask for update
- [ ] write some kind of back-up files, one with the records in orig format, the other with the trx
- [ ] create proper initial data_ingestion function with df cleaning / assertions
- [ ] create remove_record function (-> set status to inactive)
- [ ] How will I handle split recods? Multiple labels for a record? I could list them twice (with credit worth of 0.5)

- [ ] create ratings table
- [ ] create random button (discogs has one ;-))

### Meta Things

- [ ] Document the CreditTrx Table, which TrxTypes are possible, the logic etc.
- [ ] Document the ingestion approach, that bulk insertion (with sqlachemy core) does only work for copying data into tables, without taking care of the relationships
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
  