-- Create the employee table
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    employment_status VARCHAR(20),
    age INT,
    hourly_salary DECIMAL(10, 2)
);

-- Insert some sample data
INSERT INTO employee (name, employment_status, age, hourly_salary)
VALUES
    ('John Doe', 'Full Time', 45, 25.00),
    ('Jane Smith', 'Full Time', 42, 25.00),
    ('Alice Johnson', 'Full Time', 50, 25.00),
    ('Bob Williams', 'Full Time', 33, 25.00),
    ('Michael Brown', 'Full Time', 53, 25.00),
    ('Emily Davis', 'Part Time', 41, 15.00),
    ('David Miller', 'Part Time', 43, 15.00),
    ('Sarah Wilson', 'Part Time', 52, 15.00),
    ('Daniel Taylor', 'Part Time', 49, 15.00),
    ('Olivia Martinez', 'Part Time', 30, 15.00);