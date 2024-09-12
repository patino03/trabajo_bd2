USE employee_data;

-- Crear la tabla employee_table si no existe
CREATE TABLE IF NOT EXISTS employee_table (
    ID INT NOT NULL PRIMARY KEY,
    Age INT NOT NULL,
    Income DECIMAL(10, 2) NOT NULL,
    Expenses DECIMAL(10, 2) NOT NULL,
    Weekly_Hours INT NOT NULL
);
