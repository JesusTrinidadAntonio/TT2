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