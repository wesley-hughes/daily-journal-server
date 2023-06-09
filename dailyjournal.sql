CREATE TABLE `Entries` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`  TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	`moodId` INTEGER NOT NULL,
	`date` DATE NOT NULL,
	FOREIGN KEY(`moodId`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

INSERT INTO 'Entries'
VALUES (null, 'Javascript', 'I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', 1, 'Wed Sep 15 2021 10:10:47');
INSERT INTO 'Entries'
VALUES (null, 'Python', 'Python is named after the Monty Python comedy group from the UK. Im sad because I thought it was named after the snake', 4, 'Wed Sep 15 2021 10:11:33');
INSERT INTO 'Entries'
VALUES (null, 'Python', 'Why did it take so long for python to have a switch statement? Its much cleaner than if/elif blocks', 3, 'Wed Sep 15 2021 10:13:11');
INSERT INTO 'Entries'
VALUES (null, 'Javascript', 'Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.', 3, 'Wed Sep 15 2021 10:14:05');

INSERT INTO 'Moods' VALUES (null, 'Happy');
INSERT INTO 'Moods' VALUES (null, 'Sad');
INSERT INTO 'Moods' VALUES (null, 'Angry');
INSERT INTO 'Moods' VALUES (null, 'Ok');

SELECT
    e.id,
    e.concept,
    e.entry,
    e.moodId,
    e.date
FROM Entries e;