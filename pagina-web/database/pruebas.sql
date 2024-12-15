-- creacion de la base de datos
create database proyectott2;
-- utilizando la base de datos
use proyectott2;
-- creando una tabla

create table usuario(
    id int (5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    contraseña VARCHAR(50) NOT NULL);
-- enseñar tablas
show tables;

-- describir tabla
describe usuario;