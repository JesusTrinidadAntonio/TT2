const { render } = require("ejs");

const controller = {};


/**
 * 
 * Datos personales del usuario 
 * 
*/
controller.datosPersonales = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;

        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('SELECT * FROM usuario WHERE id_usuario = ?', [id_usuario], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }

                // Verificamos si encontramos registros
                if (registros.length === 0) {
                    return res.status(404).send('No se encontraron registros para este usuario');
                }

                // Pasamos el id_usuario y los registros a la vista
                res.render('datos_usuario', {
                    id_usuario,       // También podemos pasar el id_usuario si es necesario
                    data: registros[0]         // Pasamos los registros obtenidos
                });
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};

/**
 * 
 * Pantalla de modificacion de datos del usuario
 * 
 */

controller.modificar_datos = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;

        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('SELECT * FROM usuario WHERE id_usuario = ?', [id_usuario], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }

                // Verificamos si encontramos registros
                if (registros.length === 0) {
                    return res.status(404).send('No se encontraron registros para este usuario');
                }

                // Pasamos el id_usuario y los registros a la vista
                res.render('mod_datos_usuario', {
                    id_usuario,       // También podemos pasar el id_usuario si es necesario
                    data: registros[0]         // Pasamos los registros obtenidos
                });
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};
/**
 *
 * Actualización en la base de datos (Funcionalidad)
 * 
 */
controller.cambio_datos = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const nuevoUsuario = req.body;
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('UPDATE usuario set ? where id_usuario = ?', [nuevoUsuario, id_usuario], (err, rows) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }
                // Pasamos el id_usuario y los registros a la vista
                res.redirect('/datos_personales');
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};



/*

    Aqui comienza la sección de los códigos relacionados a la visualizacion y modificación
    de los datos del cuerpo de agua en la base de datos


*/

/**
 * 
 * Visualizacion de los cuerpos de agua ingresados por el usuario
 * 
 */
controller.dashboard = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;

        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('SELECT * FROM cuerpo_agua WHERE id_usuario_fk = ?', [id_usuario], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }



                // Pasamos el id_usuario y los registros a la vista
                res.render('user_view', {
                    id_usuario,       // También podemos pasar el id_usuario si es necesario
                    data: registros         // Pasamos los registros obtenidos
                });
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};



/**
 * 
 * Visualizamos el registro del cuerpo de agua de manera detallada
 * 
 */
// Ver Registro del cuerpo de agua de manera detallada
controller.verRegistro = (req, res) => {
    // Verifica que la sesión esté activa
    if (req.session && req.session.id_usuario && req.session.id_cuerpo_a) {
        const id_usuario = req.session.id_usuario;
        const id_cuerpo_a = req.session.id_cuerpo_a; // Obtén el ID desde la sesión

        console.log(`ID de usuario: ${id_usuario}, ID de cuerpo de agua: ${id_cuerpo_a}`);

        // Conectamos a la base de datos
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Consulta para obtener datos del cuerpo de agua
            conn.query('SELECT * FROM cuerpo_agua WHERE id_cuerpo_a = ?', [id_cuerpo_a], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta de cuerpo_agua:', err);
                    return res.status(500).send('Error en la consulta');
                }

                if (registros.length === 0) {
                    return res.status(404).send('No se encontró el cuerpo de agua.');
                }

                const cuerpoAgua = registros[0];
                const id_dir_fk = cuerpoAgua.id_dir_fk;
                const id_imagen_fk = cuerpoAgua.id_imagen_fk;

                // Consulta para obtener datos de la imagen
                conn.query('SELECT * FROM imagen WHERE id_imagen = ?', [id_imagen_fk], (err, imagenRegistros) => {
                    if (err) {
                        console.error('Error en la consulta de imagen:', err);
                        return res.status(500).send('Error en la consulta de imagen');
                    }

                    const imagen = imagenRegistros[0] || null; // Si no hay imagen, usa null

                    // Consulta para obtener datos de la dirección
                    conn.query('SELECT * FROM direccion WHERE id_dir = ?', [id_dir_fk], (err, direccionRegistros) => {
                        if (err) {
                            console.error('Error en la consulta de direccion:', err);
                            return res.status(500).send('Error en la consulta de direccion');
                        }

                        if (direccionRegistros.length === 0) {
                            return res.status(404).send('No se encontró la dirección.');
                        }

                        const direccion = direccionRegistros[0];

                        // Renderizamos la vista con los datos obtenidos
                        res.render('mod_cuerpo_a', {
                            id_usuario,    // ID del usuario
                            cuerpoAgua,    // Datos del cuerpo de agua
                            direccion,     // Datos de la dirección correspondiente
                            imagen         // Datos de la imagen correspondiente
                        });

                        // Limpia el ID de la sesión después de usarlo (opcional)
                        delete req.session.id_cuerpo_a;
                    });
                });
            });
        });
    } else {
        // Si no hay sesión activa, redirigimos al login
        res.redirect('/');
    }
};
/**
 * 
 * Eliminar el registro del cuerpo de agua seleccionado con el boton "ver detalles"
 *  
 */
controller.delReg = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const { id_cuerpo_a } = req.params;
        const nuevoCuerpo = req.body;
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('DELETE FROM cuerpo_agua where id_cuerpo_a = ? ', [id_cuerpo_a], (err, rows) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }
                // Pasamos el id_usuario y los registros a la vista
                res.redirect('/dashboard');
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};


/**
 * 
 *  Visualización de la pantalla con los datos del cuerpo de agua(inputs), aqui se ingresan los cambios al cuerpo de agua 
 * 
 */
controller.cambioReg = (req, res) => {
    // Verificamos si la sesión está activa
    if (req.session && req.session.id_usuario && req.session.id_cuerpo_a) {
        const id_usuario = req.session.id_usuario;
        const id_cuerpo_a = req.session.id_cuerpo_a; // Obtenemos el ID desde la sesión

        // Conectamos a la base de datos
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Consulta para obtener datos del cuerpo de agua
            conn.query('SELECT * FROM cuerpo_agua WHERE id_cuerpo_a = ?', [id_cuerpo_a], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta de cuerpo_agua:', err);
                    return res.status(500).send('Error en la consulta');
                }

                // Si se encuentra el cuerpo de agua, obtenemos el id_dir_fk para consultar la tabla direccion
                const cuerpoAgua = registros[0];
                const id_dir_fk = cuerpoAgua.id_dir_fk;

                // Consulta para obtener datos de la dirección
                conn.query('SELECT * FROM direccion WHERE id_dir = ?', [id_dir_fk], (err, direccion) => {
                    if (err) {
                        console.error('Error en la consulta de direccion:', err);
                        return res.status(500).send('Error en la consulta de direccion');
                    }

                    // Renderizamos la vista con los datos obtenidos
                    res.render('cambio_cuerpo_a', {
                        id_usuario,           // ID del usuario
                        cuerpoAgua,           // Datos del cuerpo de agua
                        direccion: direccion[0]  // Datos de la dirección correspondiente
                    });

                    // Limpia el ID de la sesión después de usarlo (opcional)
                    delete req.session.id_cuerpo_a;
                });
            });
        });
    } else {
        // Si no hay sesión activa, redirigimos al login
        res.redirect('/');
    }
};

/**
 * 
 *  Funcionalidad de actualizar los datos del cuerpo de agua en la base de datos (tablas: cuerpo_agua y direccion)
 * 
 */

controller.cambio_datos_ca = (req, res) => {
    if (req.session && req.session.id_usuario && req.session.id_cuerpo_a) {
        const id_usuario = req.session.id_usuario;
        const id_cuerpo_a = req.session.id_cuerpo_a;

        // Obtenemos los datos enviados desde el formulario
        const {
            nombre_cuerpo_a,
            fecha_cuerpo_a,
            pais_dir,
            estado_dir,
            ciudad_dir
        } = req.body;



        // Conectamos a la base de datos
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Actualizamos la tabla cuerpo_agua
            conn.query(
                'UPDATE cuerpo_agua SET nombre_cuerpo_a = ?, fecha_cuerpo_a = ? WHERE id_cuerpo_a = ?',
                [nombre_cuerpo_a, fecha_cuerpo_a, id_cuerpo_a],
                (err, result) => {
                    if (err) {
                        console.error('Error al actualizar cuerpo_agua:', err);
                        return res.status(500).send('Error al actualizar cuerpo de agua');
                    }

                    // Obtenemos el id_dir_fk para actualizar direccion
                    conn.query(
                        'SELECT id_dir_fk FROM cuerpo_agua WHERE id_cuerpo_a = ?',
                        [id_cuerpo_a],
                        (err, registros) => {
                            if (err) {
                                console.error('Error al obtener id_dir_fk:', err);
                                return res.status(500).send('Error al obtener datos de dirección');
                            }

                            if (registros.length === 0) {
                                console.error('No se encontró id_dir_fk asociado');
                                return res.status(404).send('No se encontró el cuerpo de agua');
                            }

                            const id_dir_fk = registros[0].id_dir_fk;

                            // Actualizamos la tabla direccion
                            conn.query(
                                'UPDATE direccion SET pais_dir = ?, estado_dir = ?, ciudad_dir = ? WHERE id_dir = ?',
                                [pais_dir, estado_dir, ciudad_dir, id_dir_fk],
                                (err, result) => {
                                    if (err) {
                                        console.error('Error al actualizar direccion:', err);
                                        return res.status(500).send('Error al actualizar dirección');
                                    }

                                    console.log('Actualización exitosa');
                                    // Redirigimos al detalle del registro
                                    res.redirect(`/ver_registro/${id_cuerpo_a}`);
                                }
                            );
                        }
                    );
                }
            );
        });
    } else {
        res.redirect('/');
    }
};
/**
 * 
 * Fin de la sección de los cuerpos de agua 
 * 
 * */

/**
*
*  Inicio de la sección de para el desarrollo de la funcionalidad "realizar medicion" 
*
*/
controller.instrucciones=(req,res)=>{
    res.render('instrucciones');
};

controller.resultados=(req,res)=>{
    res.render('resultados');
};

controller.descartarCalculo=(req,res)=>{
    res.render('home');
};


controller.guardarCalculo = (req, res) => {
    const id_usuario = req.session.id_usuario; // ID del usuario autenticado
    const data = req.body;

    req.getConnection((err, conn) => {
        if (err) {
            console.error("Error de conexión:", err);
            return res.status(500).send("Error de conexión con la base de datos.");
        }

        try {
            // Insertar dirección primero
            const direccion = {
                pais_dir: data.pais_dir,
                estado_dir: data.estado_dir,
                ciudad_dir: data.ciudad_dir,
            };

            conn.query('INSERT INTO direccion SET ?', [direccion], (err, resultDireccion) => {
                if (err) {
                    console.error("Error al insertar la dirección:", err);
                    return res.status(500).send("Error al insertar la dirección.");
                }

                const id_dir = resultDireccion.insertId; // ID de la dirección recién insertada

                console.log("Dirección insertada correctamente con ID:", id_dir);

                // Insertar imagen original
                const imagen = {
                    url_imagen: data.url_imagen,
                    fecha_imagen: data.fecha_imagen,
                    id_usuario_fk: id_usuario,
                };

                conn.query('INSERT INTO imagen SET ?', [imagen], (err, resultImagen) => {
                    if (err) {
                        console.error("Error al insertar la imagen:", err);
                        return res.status(500).send("Error al insertar la imagen.");
                    }

                    const id_imagen = resultImagen.insertId; // ID de la imagen recién insertada

                    console.log("Imagen insertada correctamente con ID:", id_imagen);

                    // Insertar imagen editada
                    const imagen_editada = {
                        url_imagen_ed: data.url_imagen_ed,
                        id_imagen_fk: id_imagen,
                    };

                    conn.query('INSERT INTO imagen_editada SET ?', [imagen_editada], (err, resultImagenEditada) => {
                        if (err) {
                            console.error("Error al insertar la imagen editada:", err);
                            return res.status(500).send("Error al insertar la imagen editada.");
                        }

                        console.log("Imagen editada insertada correctamente con ID:", resultImagenEditada.insertId);

                        const areaNumerica = parseFloat(data.area_cuerpo_a.replace('m²', '').trim());
                        const perimetroNumerico = parseFloat(data.perimetro_cuerpo_a.replace('m', '').trim());

                        const cuerpoAguaData = {
                            nombre_cuerpo_a: data.nombre_cuerpo_a,
                            fecha_cuerpo_a: data.fecha_cuerpo_a,
                            area_cuerpo_a: areaNumerica, // Sin las unidades
                            perimetro_cuerpo_a: perimetroNumerico, // Sin las unidades
                            publicado_cuerpo_a: 'NO',
                            pendpub_cuerpo_a: 'NO',
                            id_dir_fk: id_dir, // Relacionar con la dirección
                            id_imagen_fk: id_imagen, // Relacionar con la imagen original
                            id_usuario_fk: id_usuario, // Asociar con el usuario
                        };

                        conn.query('INSERT INTO cuerpo_agua SET ?', [cuerpoAguaData], (err, resultCuerpoAgua) => {
                            if (err) {
                                console.error("Error al insertar cuerpo de agua:", err);
                                return res.status(500).send("Error al insertar el cuerpo de agua.");
                            }

                            console.log("Cuerpo de agua insertado correctamente con ID:", resultCuerpoAgua.insertId);
                            res.redirect('/dashboard');
                        });
                    });
                });
            });
        } catch (error) {
            console.error(error);
            res.status(500).send('Hubo un error al guardar los datos.');
        }
    });
};




/**
 * 
 * Fin de la sección "Realizar medición"
 * 
 * */


/*Pagina de ¿Quienes somos */

controller.somos = (req, res) => {
    res.render('quienes_somos');
}



/*Página de "Registros públicos"  */

controller.registros_pub = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const pub_cuerpo_a = 'Si';
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('SELECT * FROM cuerpo_agua WHERE publicado_cuerpo_a = ?', [pub_cuerpo_a], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }



                // Pasamos el id_usuario y los registros a la vista
                res.render('registros_pub', {
                    id_usuario,       // También podemos pasar el id_usuario si es necesario
                    data: registros         // Pasamos los registros obtenidos
                });
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/');
    }
};


/**Código generico */

//Iniciamos la configuración de la conexion a la base de datos
controller.list = (req, res) => {
    req.getConnection((err, conn) => {
        conn.query('select * from usuario', (err, usuarios) => {
            if (err) {
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('usuarios_adm', {
                data: usuarios
            });
        });
    });
};

//Guardar datos en la base de datos
controller.save = (req, res) => {
    const data = req.body;
    req.getConnection((err, conn) => {
        conn.query('INSERT INTO usuario set ?', [data], (err, usuario) => {
            console.log(usuario);
            res.redirect('/');
            console.log(data);
        });
    });

};

//Eliminar datos en la base de datos
controller.delete = (req, res) => {
    const { id_usuario } = req.params;
    req.getConnection((err, conn) => {
        conn.query('DELETE FROM usuario where id_usuario = ? ', [id_usuario], (err, rows) => {
            res.redirect('/adm_usuarios');

        });
    });
};

controller.edit = (req, res) => {
    const { id_usuario } = req.params;
    req.getConnection((err, conn) => {
        conn.query('SELECT * FROM usuario where id_usuario=?', [id_usuario], (err, usuario) => {
            res.render('adm_mod_usuario', {
                data: usuario[0]
            });
        });
    });
};

controller.update = (req, res) => {
    const { id_usuario } = req.params;
    const nuevoUsuario = req.body;
    req.getConnection((err, conn) => {
        conn.query('UPDATE usuario set ? where id_usuario = ?', [nuevoUsuario, id_usuario], (err, rows) => {
            res.redirect('/adm_usuarios');
        });
    });
};

controller.home = (req, res) => {
    res.render('home');
};

//Pantalla de sugerencias
controller.sug = (req, res) => {
    res.render('sugerencias');
};

controller.reg = (req, res) => {
    req.getConnection((err, conn) => {
        conn.query('select * from cuerpo_agua', (err, registros) => {
            if (err) {
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('registros', {
                data: registros
            });
        });
    });
};
/**
 * Pantallas de adm
 *
 */

controller.admHome = (req, res) => {
    res.render('adminHome');
};

controller.admPend = (req, res) => {
    const pendpub_cuerpo_a = 'Si';

    // Conectar a la base de datos
    req.getConnection((err, conn) => {
        if (err) {
            console.error('Error al conectar a la base de datos:', err);
            return res.status(500).send('Error en la conexión a la base de datos');
        }

        // Consulta para obtener los cuerpos de agua pendientes
        conn.query('SELECT * FROM cuerpo_agua WHERE pendpub_cuerpo_a = ?', [pendpub_cuerpo_a], (err, cuerpoAgua) => {
            if (err) {
                console.error('Error en la consulta de cuerpo_agua:', err);
                return res.status(500).send('Error en la consulta de cuerpo_agua');
            }

            if (!cuerpoAgua.length) {
                return res.render('adm_pendientes', { registrosCombinados: [] });
            }

            // Obtener direcciones asociadas
            const idDirFks = cuerpoAgua.map((c) => c.id_dir_fk);
            conn.query('SELECT * FROM direccion WHERE id_dir IN (?)', [idDirFks], (err, direccion) => {
                if (err) {
                    console.error('Error en la consulta de direccion:', err);
                    return res.status(500).send('Error en la consulta de direccion');
                }

                // Obtener imágenes asociadas
                const idImagenFks = cuerpoAgua.map((c) => c.id_imagen_fk);
                conn.query('SELECT * FROM imagen WHERE id_imagen IN (?)', [idImagenFks], (err, imagen) => {
                    if (err) {
                        console.error('Error en la consulta de imagen:', err);
                        return res.status(500).send('Error en la consulta de imagen');
                    }

                    // Obtener usuarios asociados
                    const idUsuarioFks = cuerpoAgua.map((c) => c.id_usuario_fk);
                    conn.query('SELECT * FROM usuario WHERE id_usuario IN (?)', [idUsuarioFks], (err, usuario) => {
                        if (err) {
                            console.error('Error en la consulta de usuario:', err);
                            return res.status(500).send('Error en la consulta de usuario');
                        }

                        // Crear un arreglo combinado
                        const registrosCombinados = cuerpoAgua.map((c) => ({
                            cuerpoAgua: c,
                            direccion: direccion.find((d) => d.id_dir === c.id_dir_fk) || null,
                            imagen: imagen.find((i) => i.id_imagen === c.id_imagen_fk) || null,
                            usuario: usuario.find((u) => u.id_usuario === c.id_usuario_fk) || null,
                        }));

                        // Renderizar la vista con los datos combinados
                        res.render('adm_pendientes', { registrosCombinados });
                    });
                });
            });
        });
    });
};

controller.aceptarPub=(req,res)=>{
    const { id_cuerpo_a } = req.params;
    const publicado_cuerpo_a = 'Si';
    const pendpub_cuerpo_a='No';
    req.getConnection((err, conn) => {
        conn.query('UPDATE cuerpo_agua set publicado_cuerpo_a = ?, pendpub_cuerpo_a= ? where id_cuerpo_a = ?', [publicado_cuerpo_a,pendpub_cuerpo_a, id_cuerpo_a], (err, rows) => {
            res.redirect('/adm_pendientes');
        });
    });
};

controller.rechazarPub=(req,res)=>{
    const { id_cuerpo_a } = req.params;
    const publicado_cuerpo_a = 'No';
    const pendpub_cuerpo_a='No';
    req.getConnection((err, conn) => {
        conn.query('UPDATE cuerpo_agua set publicado_cuerpo_a = ?, pendpub_cuerpo_a= ? where id_cuerpo_a = ?', [publicado_cuerpo_a,pendpub_cuerpo_a, id_cuerpo_a], (err, rows) => {
            res.redirect('/adm_pendientes');
        });
    });
};


controller.pub_reg=(req,res)=>{
    const { id_cuerpo_a } = req.params;
    const pendpub_cuerpo_a='Si';
    req.getConnection((err, conn) => {
        conn.query('UPDATE cuerpo_agua set pendpub_cuerpo_a= ? where id_cuerpo_a = ?', [pendpub_cuerpo_a, id_cuerpo_a], (err, rows) => {
            res.redirect('/dashboard');
        });
    });
};


controller.admBugs=(req,res)=>{
    req.getConnection((err, conn) => {
        conn.query('select * from sugerencias', (err, sugerencias) => {
            if (err) {
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('adm_bugs', {
                data: sugerencias
            });
        });
    });
    
};

controller.admUsuarios=(req,res)=>{
  
    req.getConnection((err, conn) => {
            conn.query('select * from usuario', (err, usuarios) => {
                if (err) {
                    res.json(err);
                }
                res.render('adm_usuarios', {
                    data: usuarios
                });
            });
        });
};


controller.sugg = (req, res) => {
    const data = req.body;
    req.getConnection((err, conn) => {
        conn.query('INSERT INTO sugerencias set ?', [data], (err, sugerencias) => {
            console.log(sugerencias);
            res.redirect('/');
            console.log(data);
        });
    });

};

module.exports = controller;