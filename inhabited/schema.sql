DROP TABLE IF EXISTS habit;
DROP TABLE IF EXISTS completion;

/*
  The period of a habit is an integer value of days that specifies how often the
  habit should be completed. For now, it's just a simple day count but in the
  future it might be expanded to cover more complex recurrences.
*/
CREATE TABLE habit (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT NOT NULL,
  period          INTEGER NOT NULL
);

/*
  The timestamp of a completion is a unix timestamp.
*/
CREATE TABLE completion (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp       INTEGER NOT NULL,
  habit_id        INTEGER NOT NULL,
  FOREIGN KEY (habit_id) REFERENCES habit(id)
);
