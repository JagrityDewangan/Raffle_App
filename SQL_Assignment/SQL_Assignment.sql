/*Write a SQL query to retrieve the top 10 most borrowed books, along with the number of times each book has been borrowed.*/

SELECT books.title, COUNT(borrowed_books.book_id) AS borrow_count
FROM books JOIN borrowed_books ON books.book_id = borrowed_books.book_id
GROUP BY books.title ORDER BY borrow_count DESC LIMIT 10;

/*Create a stored procedure that calculates the average number of days a book is borrowed before being returned. The procedure should take a book_id as input and return the average number of days.*/

DELIMITER //
CREATE PROCEDURE CalculateAverageBorrowDuration(IN p_book_id INT, OUT p_average_duration FLOAT)
BEGIN SELECT AVG(DATEDIFF(return_date, borrow_date)) INTO p_average_duration
FROM borrowed_books WHERE book_id = p_book_id;
END //
DELIMITER ;
CALL CalculateAverageBorrowDuration(1, @average_duration);
SELECT @average_duration AS average_duration;

/*Write a query to find the user who has borrowed the most books from the library.*/

SELECT users.user_id, users.first_name, users.last_name, COUNT(borrowed_books.book_id) AS books_borrowed_count
FROM users JOIN borrowed_books ON users.user_id = borrowed_books.user_id
GROUP BY users.user_id, users.first_name, users.last_name
ORDER BY books_borrowed_count DESC
LIMIT 1;

/*Create an index on the publication_year column of the books table to improve query performance.*/

CREATE INDEX index_publication_year ON books(publication_year);

/*Write a SQL query to find all books published in the year 2020 that have not been borrowed by any user.*/

SELECT books.book_id, books.title, books.author, books.publication_year
FROM books WHERE books.publication_year = 2020 AND books.book_id NOT IN (SELECT book_id FROM borrowed_books);

/*Design a SQL query that lists users who have borrowed books published by a specific author (e.g., "J.K. Rowling").*/

SELECT DISTINCT users.user_id, users.first_name, users.last_name
FROM users JOIN borrowed_books ON users.user_id = borrowed_books.user_id
JOIN books ON borrowed_books.book_id = books.book_id
WHERE books.author = 'John Green';

/*Create a trigger that automatically updates the return_date in the borrowed_books table to the current date when a book is returned.*/

DELIMITER //
CREATE TRIGGER update_return_date
BEFORE UPDATE ON borrowed_books
FOR EACH ROW
BEGIN
    IF NEW.return_date IS NOT NULL THEN
        SET NEW.return_date = CURRENT_DATE;
    END IF;
END //
DELIMITER ;


