# Disco

## Project in General

    connection = engine.connect()
    connection.execution_options(autocommit=True).execute(query)

- [ ] Document the ipynb on github
- [ ] Set-up logging config

If I use pd.to_sql, then obviously I do not insert in an existing table (?) but create a new, overwrite the schema. I have to check that
It would be better to bulk insert into the table instead of doing like I do now.

It might be better to use sqlalchemy instead of sqlite so I can easily switch between DBs.

## To Do, OLD STUFF

- [ ] Print Output summary of load (total loaded, total not loaded, load time etc.)
- [ ] How to regulary update the data without requesting all a new?

## Backlog

- [ ] How to handle albums not found on Spotify in the final version
- [ ] ...

## Notes

- [ ] ...
  