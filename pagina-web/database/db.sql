create database 2024_b049;

use 2024_b049;

create table imagen_editada(
	id_imagen_ed int(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   	nombre_imagen_ed VARCHAR(100) NOT NULL,
    fecha_imagen_ed DATE NOT NULL,
    url_imagen_ed VARCHAR(255) NOT NULL
);

create table usuario(
    id_usuario int(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombres_usuario VARCHAR(100) NOT NULL,
    apellidos_usuario VARCHAR(100) NOT NULL,
    correo_usuario VARCHAR(100) NOT NULL,
    contraseña_usuario VARCHAR(50) NOT NULL,
    tipo_usuario INT(2) NOT NULL
);

CREATE TABLE direccion(
    id_dir INT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    estado_dir VARCHAR(50) NOT NULL,
    entidad_federativa_dir VARCHAR(50) NOT NULL,
    codigo_postal_dir INT(5),
    coordenadas_dir VARCHAR(100) NOT NULL 
);

CREATE TABLE imagen(
    id_imagen INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_imagen VARCHAR(100) NOT NULL,
    fecha_imagen DATE NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    id_imagen_ed_fk int(5) UNSIGNED NOT NULL,
    id_usuario_fk int(5) UNSIGNED NOT NULL,
    FOREIGN KEY(id_imagen_ed_fk) REFERENCES imagen_editada(id_imagen_ed),
    FOREIGN KEY(id_usuario_fk) REFERENCES usuario(id_usuario)
);

CREATE TABLE cuerpo_agua(
    id_cuerpo_a int(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_cuerpo_a VARCHAR(100) NOT NULL,
    fecha_cuerpo_a DATE NOT NULL,
    area_cuerpo_a FLOAT NOT NULL,
    perimetro_cuerpo_a FLOAT NOT NULL,
    publicado_cuerpo_a VARCHAR(5) NOT NULL,
    id_dir_fk int(5) UNSIGNED NOT NULL,
    id_imagen_fk int(5) UNSIGNED NOT NULL,
    id_usuario_fk int(5) UNSIGNED NOT NULL,
    FOREIGN KEY (id_dir_fk) REFERENCES direccion(id_dir),
    FOREIGN KEY (id_imagen_fk) REFERENCES imagen(id_imagen),
    FOREIGN KEY (id_usuario_fk) REFERENCES usuario(id_usuario)    
);


CREATE TABLE sugerencias(
    id_sugerencia int  AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);
describe cuerpo_agua;
describe direccion; 
describe imagen;
describe imagen_editada;
describe usuario;   
describe sugerencias;