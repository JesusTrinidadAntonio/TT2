const controller={};

//Iniciamos la configuración de la conexion a la base de datos
controller.list= (req,res) => {
    req.getConnection((err, conn) => {
        conn.query('select * from usuario', (err, usuarios) => {
            if(err){
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('usuarios_adm',{
                data: usuarios
            });
        });
    });
};

//Guardar datos en la base de datos
controller.save=(req,res)=>{
    const data= req.body;
    req.getConnection((err,conn)=>{
        conn.query('INSERT INTO usuario set ?', [data], (err,usuario)=>{
            console.log(usuario);
            res.redirect('/login');
            console.log(data);
        });
    });
    
};

controller.guardarCalculo = (req, res) => {
    const data = req.body;

    // Extraemos los datos del formulario
    const nombreCuerpoAgua = data.nombre_cuerpo_agua;  // Nombre del cuerpo de agua
    const fecha = data.fecha;  // Fecha del cuerpo de agua (campo deshabilitado)
    const area = data.area;  // Área del cuerpo de agua
    const perimetro = data.perimetro;  // Perímetro del cuerpo de agua
    const fechaFoto = data.fecha_foto;  // Fecha de la foto (fecha ingresada por el usuario)

    // Ruta de las imágenes
    const imagenCuerpoAguaUrl = data.imagen_url_cuerpo_agua;  // URL de la imagen Cuerpo_Agua
    const imagenBinarizadaUrl = data.imagen_url_binarizada;  // URL de la imagen binarizada

    // 1. Guardar el cuerpo de agua en la tabla "cuerpo_agua"
    req.getConnection((err, conn) => {
        if (err) {
            console.error("Error en la conexión:", err);
            return res.status(500).send("Error en la conexión con la base de datos");
        }

        // Guardar los datos en la tabla cuerpo_agua
        const cuerpoAguaData = {
            nombre_cuerpo_a: nombreCuerpoAgua,
            fecha_cuerpo_a: fecha,
            area_cuerpo_a: area,
            perimetro_cuerpo_a: perimetro,
        };

        conn.query('INSERT INTO cuerpo_agua SET ?', [cuerpoAguaData], (err, result) => {
            if (err) {
                console.error("Error al insertar en cuerpo_agua:", err);
                return res.status(500).send("Error al insertar los datos en la tabla cuerpo_agua");
            }

            // 2. Guardar la imagen Cuerpo_Agua en la tabla "imagen"
            const imagenData = {
                url_imagen: imagenCuerpoAguaUrl,
                fecha_imagen: fechaFoto,  // Usamos la fecha ingresada por el usuario
            };

            conn.query('INSERT INTO imagen SET ?', [imagenData], (err, result) => {
                if (err) {
                    console.error("Error al insertar en imagen:", err);
                    return res.status(500).send("Error al insertar los datos en la tabla imagen");
                }

                // 3. Guardar la imagen binarizada en la tabla "imagen_editada"
                const imagenEditadaData = {
                    url_imagen: imagenBinarizadaUrl,  // URL de la imagen binarizada
                };

                conn.query('INSERT INTO imagen_editada SET ?', [imagenEditadaData], (err, result) => {
                    if (err) {
                        console.error("Error al insertar en imagen_editada:", err);
                        return res.status(500).send("Error al insertar los datos en la tabla imagen_editada");
                    }

                    // Todo ha ido bien, redirigir a la página de login
                    console.log("Datos insertados correctamente:");
                    console.log({
                        cuerpoAguaData,
                        imagenData,
                        imagenEditadaData
                    });

                    // Redirigir después de insertar todo
                    res.redirect('/login');
                });
            });
        });
    });
};

//Eliminar datos en la base de datos
controller.delete=(req,res)=>{   
    const { id_usuario }=req.params;
    req.getConnection((err,conn)=>{
        conn.query('DELETE FROM usuario where id_usuario = ? ',[id_usuario],(err,rows)=>{
            res.redirect('/');
            
        });
    });
};

controller.edit=(req,res)=>{
    const { id_usuario }=req.params;
    req.getConnection((err,conn)=>{
        conn.query('SELECT * FROM usuario where id_usuario=?',[id_usuario],(err,usuario)=>{
            res.render('usuarios_adm_mod',{
                data: usuario[0]
            });
        });
    });
};

controller.update=(req,res)=>{
    const { id_usuario }=req.params;
    const nuevoUsuario= req.body;
    req.getConnection((err,conn)=>{
        conn.query('UPDATE usuario set ? where id_usuario = ?' , [nuevoUsuario,id_usuario], (err,rows)=>{
            res.redirect('/');
        });
    });
};


controller.home=(req,res)=>{
    res.render('home');
};

controller.instrucciones=(req,res)=>{
    res.render('instrucciones');
};

controller.resultados=(req,res)=>{
    res.render('Resultados');
};

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

                // Verificamos si encontramos registros
                if (registros.length === 0) {
                    return res.status(404).send('No se encontraron registros para este usuario');
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
        res.redirect('/login');
    }
};
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
        res.redirect('/login');
    }
};


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
        res.redirect('/login');
    }
};


//Actualizar los datos del cuerpo de agua
controller.cambioReg = (req, res) => {
        // Verificamos si existe la propiedad id_usuario en la sesión
        if (req.session && req.session.id_usuario) {
            // Si existe, la sesión está activa y podemos acceder a la ruta
            const id_usuario = req.session.id_usuario;
            const {id_cuerpo_a}= req.params;
            // Conectamos a la base de datos y obtenemos los registros
            req.getConnection((err, conn) => {
                if (err) {
                    console.error('Error al conectar a la base de datos:', err);
                    return res.status(500).send('Error en la conexión');
                }
    
                // Realizamos la consulta para obtener los registros relacionados con id_usuario
                conn.query('SELECT * FROM cuerpo_agua WHERE id_cuerpo_a = ?', [id_cuerpo_a], (err, registros) => {
                    if (err) {
                        console.error('Error en la consulta:', err);
                        return res.status(500).send('Error en la consulta');
                    }
    
                    // Verificamos si encontramos registros
                    if (registros.length === 0) {
                        return res.status(404).send('No se encontraron registros para este usuario');
                    }
    
                    // Pasamos el id_usuario y los registros a la vista
                    res.render('cambio_cuerpo_a', {
                        id_usuario,       // También podemos pasar el id_usuario si es necesario
                        data: registros[0]         // Pasamos los registros obtenidos
                    });
                });
            });
        } else {
            // Si no existe, redirigimos al login
            res.redirect('/login');
        }
};

//Actualizar los datos
controller.cambio_datos = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const nuevoUsuario= req.body;
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('UPDATE usuario set ? where id_usuario = ?' , [nuevoUsuario,id_usuario], (err,rows) => {
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
        res.redirect('/login');
    }
};

//Actualizar los datos
controller.cambio_datos_ca = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const {id_cuerpo_a}=req.params;
        const nuevoCuerpo= req.body;
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('UPDATE cuerpo_agua set ? where id_cuerpo_a = ?' , [nuevoCuerpo,id_cuerpo_a], (err,rows) => {
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
        res.redirect('/login');
    }
};

controller.delReg = (req, res) => {
    // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const {id_cuerpo_a}=req.params;
        const nuevoCuerpo= req.body;
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }

            // Realizamos la consulta para obtener los registros relacionados con id_usuario
            conn.query('DELETE FROM cuerpo_agua where id_cuerpo_a = ? ',[id_cuerpo_a],(err,rows) => {
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
        res.redirect('/login');
    }
};

//Ver Registro del cuerpo de agua de manera detallada
controller.verRegistro = (req,res)=>{

       // Verificamos si existe la propiedad id_usuario en la sesión
    if (req.session && req.session.id_usuario) {
        // Si existe, la sesión está activa y podemos acceder a la ruta
        const id_usuario = req.session.id_usuario;
        const {id_cuerpo_a}= req.params;
        console.log(id_cuerpo_a);
        // Conectamos a la base de datos y obtenemos los registros
        req.getConnection((err, conn) => {
            if (err) {
                console.error('Error al conectar a la base de datos:', err);
                return res.status(500).send('Error en la conexión');
            }
            conn.query('SELECT * FROM cuerpo_agua WHERE id_cuerpo_a = ?', [id_cuerpo_a], (err, registros) => {
                if (err) {
                    console.error('Error en la consulta:', err);
                    return res.status(500).send('Error en la consulta');
                }
                // Pasamos el id_usuario y los registros a la vista
                res.render('mod_cuerpo_a', {
                    id_cuerpo_a, 
                    id_usuario,
                    data: registros[0]         // Pasamos los registros obtenidos
                });
            });
        });
    } else {
        // Si no existe, redirigimos al login
        res.redirect('/login');
    }
};

//Pantalla de sugerencias
controller.sug=(req,res)=>{
    res.render('sugerencias');
};

controller.reg=(req,res)=>{
    req.getConnection((err, conn) => {
        conn.query('select * from cuerpo_agua', (err, registros) => {
            if(err){
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('registros',{
                data: registros
            });
        });
    });
};

controller.sugg=(req,res)=>{
    const data= req.body;
    req.getConnection((err,conn)=>{
        conn.query('INSERT INTO sugerencias set ?', [data], (err,sugerencias)=>{
            console.log(sugerencias);
            res.redirect('/');
            console.log(data);
        });
    });
    
};

module.exports=controller;