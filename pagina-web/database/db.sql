create database db_b049;

use db_B049;

create table usuario(
    id_usuario int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombres_usuario VARCHAR(100) NOT NULL,
    apellidos_usuario VARCHAR(100) NOT NULL,
    institucion_usuario VARCHAR(100) NOT NULL,
    telefono_usuario varchar(20) not null,
    ocupacion_usuario VARCHAR(50) not null,
    pais_usuario varchar(50) not null,
    estado_usuario varchar(50) not null,
    ciudad_usuario varchar(50) not null,
    correo_usuario VARCHAR(100) NOT NULL,
    contraseña_usuario VARCHAR(50) NOT NULL,
    tipo_usuario INT DEFAULT 1
);

CREATE TABLE direccion(
    id_dir INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    pais_dir VARCHAR(50) NOT NULL,
    estado_dir VARCHAR(50) NOT NULL,
    ciudad_dir varchar(50) NOT NULL
);

CREATE TABLE imagen(
    id_imagen INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_imagen DATE NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    id_usuario_fk int UNSIGNED NOT NULL,
    FOREIGN KEY(id_usuario_fk) REFERENCES usuario(id_usuario)
);

create table imagen_editada(
    id_imagen_ed int UNSIGNED AUTO_INCREMENTPRIMARY KEY,
    url_imagen_ed VARCHAR(255) NOT NULL,
    id_imagen_fk int UNSIGNED NOT NULL,
    FOREIGN KEY(id_imagen_fk) REFERENCES imagen(id_imagen)
);

CREATE TABLE cuerpo_agua(
    id_cuerpo_a int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_cuerpo_a VARCHAR(100) NOT NULL,
    fecha_cuerpo_a DATE NOT NULL,
    area_cuerpo_a FLOAT NOT NULL,
    perimetro_cuerpo_a FLOAT NOT NULL,
    publicado_cuerpo_a VARCHAR(3) DEFAULT 'NO',
    pendpub_cuerpo_a VARCHAR(3) DEFAULT 'NO',
    id_dir_fk int UNSIGNED NOT NULL,
    id_imagen_fk int UNSIGNED NOT NULL,
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