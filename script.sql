CREATE DATABASE IF NOT EXISTS miproyecto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE miproyecto;

-- Creación de la tabla Usuario
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    contrasena VARCHAR(255),
    rol VARCHAR(50),
    UNIQUE (email)  -- Añadido para asegurar la unicidad de los correos electrónicos
);

-- Creación de la tabla Proyecto
CREATE TABLE Proyecto (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(50)
);

-- Creación de la tabla Cliente
CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    UNIQUE (email)  -- Añadido para asegurar la unicidad de los correos electrónicos
);

-- Creación de la tabla Tarea
CREATE TABLE Tarea (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT,
    titulo VARCHAR(255),
    descripcion TEXT,
    estado VARCHAR(50),
    fecha_inicio DATE,
    fecha_fin DATE,
    asignado_a INT,
    FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (asignado_a) REFERENCES Usuarios(id_usuario) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Creación de la tabla Asignacion
CREATE TABLE Asignacion (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT,
    id_usuario INT,
    FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) 
        ON DELETE CASCADE ON UPDATE CASCADE
);


-- Inserción de datos en la tabla Usuarios
INSERT INTO Usuarios (nombre, email, contrasena, rol) VALUES
('Juan Perez', 'juan@example.com', 'password1', 'admin'),
('Maria Lopez', 'maria@example.com', 'password2', 'user'),
('Carlos Gomez', 'carlos@example.com', 'password3', 'user');

-- Inserción de datos en la tabla Proyecto
INSERT INTO Proyecto (id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado) VALUES
(1, 'Proyecto A', 'Descripcion del Proyecto A', '2023-01-01', '2023-12-31', 'En progreso'),
(2, 'Proyecto B', 'Descripcion del Proyecto B', '2023-02-01', '2023-12-31', 'Pendiente'),
(3, 'Proyecto C', 'Descripcion del Proyecto C', '2023-03-01', '2023-12-31', 'Completado');

-- Inserción de datos en la tabla Cliente
INSERT INTO Cliente (nombre, email, telefono, direccion) VALUES
('Cliente 1', 'cliente1@example.com', '1234567890', 'Dirección del Cliente 1'),
('Cliente 2', 'cliente2@example.com', '0987654321', 'Dirección del Cliente 2'),
('Cliente 3', 'cliente3@example.com', '1122334455', 'Dirección del Cliente 3');

-- Inserción de datos en la tabla Tarea
INSERT INTO Tarea (id_proyecto, titulo, descripcion, estado, fecha_inicio, fecha_fin, asignado_a) VALUES
(1, 'Tarea 1 del Proyecto A', 'Descripcion de la Tarea 1 del Proyecto A', 'Pendiente', '2023-01-01', '2023-02-01', 1),
(1, 'Tarea 2 del Proyecto A', 'Descripcion de la Tarea 2 del Proyecto A', 'En progreso', '2023-01-15', '2023-03-01', 2),
(2, 'Tarea 1 del Proyecto B', 'Descripcion de la Tarea 1 del Proyecto B', 'Completada', '2023-02-01', '2023-02-15', 3),
(3, 'Tarea 1 del Proyecto C', 'Descripcion de la Tarea 1 del Proyecto C', 'Pendiente', '2023-03-01', '2023-04-01', 1);

-- Inserción de datos en la tabla Asignacion
INSERT INTO Asignacion (id_proyecto, id_usuario) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 1);
